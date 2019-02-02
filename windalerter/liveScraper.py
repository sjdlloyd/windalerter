import datetime

import time
from pathlib2 import Path

from windalerter import find_first_number, get_webpage
from windalerter.util import append_csv


def current_conditions(soup):
    live = soup.findAll('div', attrs={'class':'live-td live-current'})[0]
    a = live.findAll('g')[0]
    rotation = a.attrs['transform']
    wind_speed = find_first_number(live.contents[-1])
    wind_direction = find_first_number(rotation)
    current_time = datetime.datetime.now();
    return wind_speed, wind_direction, current_time

if __name__ == "__main__":
    url = 'https://www.windguru.cz/618374'
    p = Path('dump.csv')
    for i in range(20):
        conditions = current_conditions(get_webpage(url, 5))
        append_csv(conditions, p)
        time.sleep(10*60)