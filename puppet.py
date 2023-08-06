import logging
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium import webdriver

from modules.names import NameSpace, Wait
from modules.bot import Bot

class Puppet:
    def __init__(self, driver, link, link_props):
        self.driver = driver
        self.link = link
        self.props = link_props

    def scrap_att(self, name_space, key, att):
        # Scrap element's attribute.
        val = 'unknown'
        for path in name_space:
            full = NameSpace.base + path
            try:
                val = self.driver.find_element(By.XPATH, full).get_attribute(att)
                break
            except:
                pass
        return {key: [val]}

    def scrap_txt(self, name_space, key):
        # Scrap element's text.
        val = 'unknown'
        for path in name_space:
            full = NameSpace.base + path
            try:
                val = self.driver.find_element(By.XPATH, full).text
                break
            except:
                pass
        return {key: [val]}

    def cookies(self):
        try:
            # Click 'more option' and then 'save' on Cookie banner. This will disable most of the cookies.
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[1]/div[2]/button[3]').click()
            logging.info('Puppet, rejecting cookies')
            time.sleep(Wait.short)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[1]/div[2]/button[1]').click()
        except:
            pass

if __name__ == '__main__':
    # init logging
    logging.basicConfig(format='%(asctime)s, %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='logbook.log',
                        force=True,
                        level=logging.INFO)

    operator = Bot()

    # Check site status.
    code = 0
    try:
        response = requests.get('https://www.esky.pl')
        code = response.status_code
    except requests.exceptions.ConnectionError as e:
        logging.info(e)
    finally:
        if code != 200:
            logging.error('Puppet, unable to reach server - code: %s' % code)
        else:
            logging.info('Puppet, target site responding')


    # Check if file contain links.
    links = operator.cur.execute("""SELECT url, url_id, user_id FROM links""").fetchall()

    if not links:
        logging.error('Puppet, links is empty or does not exist')

    if code == 200 and links:
        logging.info('Puppet, bot ready')

        # Starts main scraping if server responded and file contain links
        options = webdriver.ChromeOptions()
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-popup-blocking')

        driver = uc.Chrome(options=chrome_options)

        for l in links:
            # Variables.
            bot = Puppet(driver, l[0], operator.read_esky_link(l[0]))
            names_dict = NameSpace.xpath_dict
            results = {}
            logging.info('Puppet, entering site {}'.format(str(l[0])))

            # Get site and close Cookie banner if appears.
            driver.get(l[0])
            time.sleep(Wait.long)
            bot.cookies()
            time.sleep(Wait.extra_long)

            # Scrap.
            results.update({'departure_date': bot.props['departureDate']})
            for space in names_dict:
                if space in ['to_carrier_xpath', 'from_carrier_xpath']:
                    results.update(bot.scrap_att(names_dict[space], space.replace('_xpath', ''), 'title'))
                else:
                    results.update(bot.scrap_txt(names_dict[space], space.replace('_xpath', '')))

            to_save = {
                'url_id': l[1],
                'search_dt': int(time.time()),
                'departure_date': results['departure_date'],
                'to_departure': results['to_departure'][0],
                'to_arrival': results['to_arrival'][0],
                'to_direct': results['to_direct'][0],
                'to_carrier': results['to_carrier'][0],
                'price': int(results['price'][0].replace(' ', ''))
            }
            columns = ', '.join([k for k in to_save])
            values = tuple([to_save[k] for k in to_save])

            operator.cur.execute(
                f"""
                INSERT INTO results ({columns})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, values)
            operator.conn.commit()
            logging.info('Puppet, route {} saved'.format(l[1]))

        driver.delete_all_cookies()
        driver.quit()