import json

from windalerter import get_webpage
from windalerter.util import find_first_number


class Table:
    def __init__(self, lines):
        self.lines = lines
    def get_windEvent(self, i):
        values = [line.get_value(i) for line in self.lines]
        return WindEvent.from_values(values)

class Line:
    def __init__(self, line):
        self.line = line

    def get_value(self, i):
        return self.find_details(self.line[i])

    def find_details(self, element):
        raise Exception()

    def __getitem__(self, i):
        return self.get_value(i)

class Element:
    def __init__(self, element): pass


class AvgWindSpeedLine(Line):
    def __init__(self, table_soup):
        super().__init__(table_soup.findAll('td', {'class': 'wgfcst-clickable'}))

    def find_details(self, element):
        return AvgWindSpeedElement(element)


class AvgWindSpeedElement(Element):
    def __init__(self, element):
        super().__init__(element)
        self.data = json.loads(element.attrs['data-x'])
        self.time, self.initstr = int(self.data['hr_h']), self.data["initstr"]
        self.avg_wind_speed = int(list(element.children)[0])

    def __repr__(self):
        return 'time {} avg wind speed {}'.format(self.time, self.avg_wind_speed)


class GustSpeedLine(Line):
    def __init__(self, table_soup):
        super().__init__(list(table_soup.select('tr[id*=GUST]')[0].children))

    def find_details(self, element):
        return GustElement(element)


class GustElement(Element):
    def __init__(self, element):
        super().__init__(element)
        self.gust_speed = int(list(element.children)[0])

    def __repr__(self):
        return 'gust speed {}'.format(self.gust_speed)


class WindDirectionLine(Line):
    def __init__(self, table_soup):
        super().__init__(list(table_soup.find('tr', id=lambda x: 'SMER' in x).children))

    def find_details(self, element):
        return WindDirectionElement(element)


class WindDirectionElement(Element):
    def __init__(self, element):
        super().__init__(element)
        self.wind_direction = find_first_number(element.find('g').attrs['transform'])

    def __repr__(self):
        return 'wind dir {}'.format(self.wind_direction)




class WindTable(Table):
    def __init__(self, table_soup):
        self.table_soup = table_soup
        self.table_name = self.get_table_name()
        self.wind_speed = AvgWindSpeedLine(table_soup)
        self.gust_speed = GustSpeedLine(table_soup)
        self.wind_dir = WindDirectionLine(table_soup)

    def get_windEvent(self, i):
        return WindEvent.from_elements(self.wind_speed[i], self.gust_speed[i], self.wind_dir[i], i)

    def get_table_name(self):
        return None


class WindEvent:
    def __init__(self, avg_wind_speed, gust_speed, wind_dir, hr_r, name):
        self.avg_wind_speed, self.gust_speed, self.wind_dir, self.hr_r, self.name = avg_wind_speed, gust_speed, wind_dir, hr_r, name

    @classmethod
    def from_elements(cls, wind_el, gust_el, dir_el, i):
        return cls(wind_el.avg_wind_speed, gust_el.gust_speed, dir_el.wind_direction, wind_el.time, i)

    def __repr__(self):
        return ', '.join([str(s) for s in [self.name, self.hr_r, self.avg_wind_speed, self.gust_speed, self.wind_dir]])

if __name__ == "__main__":
    url = 'https://www.windguru.cz/618374'
    soup = get_webpage(url, 5)
    tables = soup.findAll('table', attrs={'class': 'tabulka'})
    table = WindTable(tables[2]) #2 is the icon model