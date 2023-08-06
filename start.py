import logging
import argparse
import time
from random import randint
import os

from modules.database import DataBase
from modules.bot import Bot
from modules.bargain import Bargain

if __name__ == '__main__':
    # init logging
    logging.basicConfig(format='%(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='../logbook.log',
                        force=True,
                        level=logging.INFO)

    db_structure = {
        'bot_data': {'alias': 'TEXT', 'bot_id': 'INTEGER', 'token': 'TEXT'},
        'message_history': {'user_id': 'INTEGER', 'dt': 'INTEGER', 'action': 'TEXT'},
        'links': {'user_id': 'INTEGER', 'add_dt': 'INTEGER', 'url': 'TEXT', 'url_id': 'INTEGER'},
        'results': {'url_id': 'TEXT', 'search_dt': 'INTEGER', 'departure_date': 'TEXT',
                    'to_departure': 'TEXT',
                    'to_arrival': 'TEXT',
                    'to_direct': 'TEXT',
                    'to_carrier': 'TEXT',
                    'price': 'INTEGER'
                    }
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()

    if args.install:
        with DataBase() as db:
            print('Installing bot database.')
            db.init_db(db_structure)
            print('Installation done. Running bot.')

    next_scrap = 0
    while True:
        with Bot() as operator:
            try:
                operator.answer_msg()
            except:
                logging.info('Start, unable to read messages.')

            if next_scrap <= 0:
                os.system('export DISPLAY=:0')
                os.system('xset dpms force on')
                os.system(f'python puppet.py')
                os.system('xset dpms force off')
                next_scrap = randint(3600 * 2, 3600 * 3)

                users = operator.cur.execute("""SELECT DISTINCT user_id FROM links""").fetchall()
                for u in users:
                    for msg in Bargain(u[0]).check_bargain():
                        already_sent = operator.cur.execute("""
                        SELECT action 
                        FROM message_history 
                        WHERE action = ?
                        AND dt >= (UNIXEPOCH() - (86400*2))
                        """, (msg[1],)).fetchall()
                        if not already_sent:
                            operator.send_msg(msg[0], msg[1], u[0], int(time.time()))

            else:
                next_scrap -= 5

        time.sleep(5)
