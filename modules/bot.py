import json
import requests
import uuid
import time

from .database import DataBase
from .bargain import Bargain

class Bot(DataBase):
    def __init__(self):
        super().__init__()
        self.token = self.read_token()
        self.url = 'https://api.telegram.org'

    def send_msg(self, msg, type_, user_id, msg_date):
        request_link = '{}/{}/sendMessage?chat_id={}&text={}'.format(self.url, self.token['token'], str(user_id), msg)
        response = requests.post(request_link)
        response_string = json.loads(response.text)

        if response_string['ok']:
            self.cur.execute("""
            INSERT INTO message_history (user_id, dt, action)
            VALUES (?, ?, ?)
            """, (user_id, msg_date, type_))
            self.conn.commit()

    def check_unread(self):
        response = requests.get('{}/{}/getUpdates'.format(self.url, self.token['token']))
        response_string = json.loads(response.text)
        if response_string['ok']:
            seen = self.cur.execute("""SELECT dt FROM message_history""").fetchall()
            seen_dt = [row[0] for row in seen]
            return [record for record in response_string['result']
                    if record['message']['date'] not in seen_dt]

    def answer_msg(self):
        message_to_answer = self.check_unread()

        for msg in message_to_answer:
            user_id = int(msg['message']['from']['id'])
            msg_date = int(msg['message']['date'])
            text = msg['message']['text']

            if text.startswith('https://www.esky.pl/flights'):
                url_id = str(uuid.uuid4()).replace('-', '')
                add_dt = int(time.time())

                check_links = [row[0] for row in
                               self.cur.execute("""SELECT url FROM links WHERE user_id=?""", (user_id,)).fetchall()]

                if text not in check_links:
                    self.cur.execute("""
                    INSERT INTO links (user_id, add_dt, url, url_id)
                    VALUES(?, ?, ?, ?)
                    """, (user_id, add_dt, text, url_id))

                    self.conn.commit()

                    self.send_msg('Link saved!', 'SAVE_LINK', user_id, msg_date)
                else:
                    self.send_msg('Link already saved!', 'REFUSE_DOUBLE_LINK', user_id, msg_date)

            elif text == 'links':
                links = [row[0] for row in self.cur.execute("""SELECT url FROM links WHERE user_id=? ORDER BY add_dt""",
                                                            (user_id,)).fetchall()]

                if links:
                    count = 1
                    return_string = ''
                    for l in links:
                        link_data = self.read_esky_link(l)
                        return_string += '{}. route: {}, departure: {}\n\n'.format(count, link_data['route'],
                                                                                   link_data['departureDate'])
                        count += 1

                    self.send_msg(return_string, 'LINKS_STATUS', user_id, msg_date)

                else:
                    self.send_msg('No links yet.', 'NO_LINKS_YET', user_id, msg_date)


            elif text.startswith('delete'):
                index_to_delete = int(text.split(' ')[1]) - 1
                links_id = [row[0] for row in
                            self.cur.execute("""SELECT url_id FROM links WHERE user_id=? ORDER BY add_dt""",
                                             (user_id,)).fetchall()]
                self.cur.execute("""DELETE FROM links WHERE url_id=?""", (links_id[index_to_delete],))
                self.send_msg('Link deleted.', 'DELETE_LINK', user_id, msg_date)

            elif text == 'status':
                status = Bargain(user_id).send_status()
                for s in status:
                    self.send_msg(s, 'STATUS', user_id, msg_date)
