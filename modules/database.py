import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('prod.db')
        self.cur = self.conn.cursor()

    def init_db(self, db_structure):
        check_tables_query = self.cur.execute(
            """
            SELECT name 
            FROM sqlite_schema 
            WHERE type = "table" 
            AND name NOT LIKE "sqlite_%"
            """).fetchall()

        if not check_tables_query:
            for table in db_structure:
                blueprint = db_structure[table]
                structure = ', '.join(['{} {}'.format(k, blueprint[k]) for k in blueprint])
                self.cur.execute('CREATE TABLE {}({})'.format(table, structure))

            full_token = input('Provide full Telegram token: ')
            bot_id = int(full_token.split(':')[0].replace('bot', ''))
            token = full_token.split(':')[1]

            self.cur.execute(
                """
                INSERT INTO bot_data (alias, bot_id, token)
                VALUES("root", ?, ?)
                """, (bot_id, token))

            self.conn.commit()

    def read_token(self):
        bot_data = self.cur.execute("""SELECT bot_id, token FROM bot_data where alias="root" """).fetchall()

        if bot_data:
            return {
                'token': 'bot{}:{}'.format(bot_data[0][0], bot_data[0][1]),
                'bot_id': bot_data[0][0]
            }

    def read_esky_link(self, link):
        l = link.split('?')
        larr = l[0].split('/')
        props = l[1].split('&')
        props = {p.split('=')[0]: p.split('=')[1] for p in props}

        route_dict = {
            'site': larr[2],
            'type': larr[5],  # oneway
            'route': '/'.join([larr[7], larr[9]])
        }
        route_dict.update(props)
        return route_dict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()