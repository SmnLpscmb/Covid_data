# Web scraping using beautifulsoup and using data extracted to create a database

from bs4 import BeautifulSoup
import requests
import re
import sqlite3

# Working with file
# with open('html_example.html') as html_file:
#     soup = BeautifulSoup(html_file, 'lxml')

# Working with http address
# source = requests.get('https://www.gov.ie/en/publication/20f2e0-updates-on-covid-19-coronavirus-since-january-2020/').text
# soup = BeautifulSoup(source, 'lxml')


# Creating a list of data about COVID-19

def create_list(url):
    # Fetch the webpage
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')    
    # Create lists used while scraping
    jour = []
    morts_cas = []
    # Look for the date in headers and append to the first list
    for date_block in soup.find_all('h4'):
        date_text = date_block.text.strip()
        try:
            if date_text.split()[1].isdigit():
                jour.append(date_text.split()[1])    
        except IndexError:
            pass
    # Look for the headline "% new deaths and % cases confirmed" and append to the second list
    my_search = re.compile(r'\d+.*\d+')
    for cases in soup.find_all('p'):
        try:
            my_match = my_search.match(cases.strong.text)
            if my_match:
                try:
                    numbers = []
                    for elt in cases.text.split():
                        if elt.isdigit():
                            numbers.append(elt)
                    deaths = numbers[0]
                    new = numbers[1]
                    morts_cas.append((deaths, new))
                except IndexError:
                    pass
        except AttributeError:
            pass
    # Create the list containing tuples of values: (date, new deaths, new cases) by merging the two first lists
    month = []
    i = 0
    while i < len(jour):
        try:
            month.append((int(jour[i]), int(morts_cas[i][0]), int(morts_cas[i][1])))
            i += 1
        # Data for the 1st of April was missing, dirty workaround
        except IndexError:
            month.append((int(jour[i]), 14, 212))
            i += 1
    return month

avril = create_list('https://www.gov.ie/en/publication/20f2e0-updates-on-covid-19-coronavirus-since-january-2020/')
# print(avril)


# # Create database
try:
    conn = sqlite3.connect('covid-19.db')
    c = conn.cursor()
    c.execute("""
            CREATE TABLE covid(
            month text,
            date integer,
            new_deaths integer,
            total_deaths integer,
            new_cases integer,
            total_cases integer)
            """)
    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    pass

# Inserting manually obtained data into the database

march = [
        (3,0,2),
        (4,0,4),
        (5,0,7),
        (6,0,5),
        (7,0,1),
        (8,0,2),
        (9,0,3),
        (10,0,10),
        (11,1,9),
        (12,0,27),
        (13,0,20),
        (14,1,39),
        (15,0,40),
        (16,0,54),
        (17,0,69),
        (18,0,74),
        (19,1,191),
        (20,0,126),
        (21,0,102),
        (22,1,121),
        (23,2,219),
        (24,1,204),
        (25,2,235),
        (26,10,255),
        (27,3,302),
        (28,14,294),
        (29,10,200),
        (30,8,295),
        (31,17,325)
        ]

# Inserting our scraped data into the database

avril.reverse()
print(avril)

def insert_data(month, name):
    '''month is a list, name is a string'''
    conn = sqlite3.connect('covid-19.db')
    c = conn.cursor()

    try:
        c.execute("SELECT total_deaths, total_cases FROM covid ORDER BY date DESC LIMIT 1;")
        numbers = c.fetchall()
        prev_deaths, prev_cases = numbers[0][0], numbers [0][1]
    except IndexError:
        prev_deaths, prev_cases = 0, 0

    i = 0
    while i < len(month):
        c.execute("INSERT INTO covid VALUES (:month, :day, :deaths, :tot_deaths, :cases, :tot_cases)",
                {
                    'month': name,
                    'day': month[i][0],
                    'deaths': month[i][1],
                    'tot_deaths': prev_deaths + sum(x[1] for x in month[:i+1]),
                    'cases': month[i][2],
                    'tot_cases': prev_cases + sum(x[2] for x in month[:i+1])
                })
        i += 1
    conn.commit()
    conn.close()


insert_data(march, 'March')
insert_data(avril, 'April')