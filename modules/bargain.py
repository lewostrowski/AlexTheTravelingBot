from .database import DataBase
import pandas as pd
import time

class Bargain(DataBase):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def fetch_data(self):
        query = """
        SELECT t1.*, t2.user_id, t2.url
        FROM results AS t1
            INNER JOIN (
                SELECT url_id, user_id, url
                FROM links
                WHERE user_id=:user_id
            ) AS t2 ON t1.url_id = t2.url_id
        ORDER BY search_dt DESC
        """

        df = pd.read_sql(query, self.conn, params={'user_id': self.user_id})

        route_data = []

        if not df.empty:
            for url_id in set(df['url_id']):
                route = df.loc[df['url_id'] == url_id]
                current_price = int(route.iloc[0, 7])
                before_price = current_price if len(route) < 2 else int(route.iloc[1, 7])

                mean_days = [1, 3, 7, 14]
                mean_prices = []
                for x in mean_days:
                    last_x_days = route.loc[route['search_dt'] >= int(time.time()) - 86400*x]['price'].iloc[1:]
                    mean_prices.append(last_x_days.mean())

                return_data = {
                    'route': self.read_esky_link(route.iloc[0, 9])['route'],
                    'current_price': current_price,
                    'direct': route.iloc[0, 5],
                    'departure': route.iloc[0, 2],
                    'min_price': route['price'].min(),
                    'max_price': route['price'].max(),
                    'before_price': (True if current_price < before_price else False, before_price)
                }

                m_index = 0
                for m in mean_prices:
                    key_name = '{}_days_avg'.format(mean_days[m_index])
                    return_data[key_name] = (True if current_price < m else False, m)
                    m_index += 1

                route_data.append(return_data)

        return route_data



    def send_status(self):
        routes = self.fetch_data()
        messages = []
        for r in routes:
            keys = list(r.keys())
            values = [r[k][1] if isinstance(r[k], tuple) else r[k] for k in r.keys()]
            msg = '\n'.join(['{}: {}'.format(keys[i].replace('_', ' '), values[i]) for i in range(0, len(keys))])
            messages.append(msg)

        return messages


    def check_bargain(self):
        routes = self.fetch_data()
        messages = []
        for r in routes:
            keys = list(r.keys())
            bargains = {k: r[k][1] for k in keys if isinstance(r[k], tuple) and r[k][0]}

            b_msg = 'BARGAIN ALERT FOR {} ({})\ncurrent price: {}'.format(r['route'].upper(), r['departure'], r['current_price'])
            for b in bargains:
                b_msg += '\n{}: {}'.format(b.replace('_', ' '), bargains[b])

            if bargains:
                messages.append((b_msg, '{}-{}-{}'.format(r['route'].upper(), r['departure'], r['current_price'])))

        return messages



