import requests
from bs4 import BeautifulSoup

def find_track_log_link(table_set):
    
    for table in table_set:
        td_set = table.find_all('td')
    
        for td in td_set:
            atmp = td.find_all('a')
            for a in atmp:
                tstr = str(a)
                if (tstr.find('tracklog')>=0):
                    return a

r = requests.get('http://flightaware.com/live/findflight?origin=KDFW&destination=KIAH')
soup = BeautifulSoup(r.content)

tables = soup.find_all('table',id='Results')
results_table = tables[0]

arrived_links = []
rows = results_table.find_all('tr')
for row in rows:
    tstr = str(row)
    if tstr.find('Arrived') >= 0:
        atmp = row.find_all('a')
        htmp = atmp[0].get('href')
        arrived_links.append(htmp)


num_links = str(len(arrived_links))
print("Number of links found: " + num_links)

flights = []

for i in range(0,10):

    print("Trying link " + str(i) + " of " + num_links + " : " + arrived_links[i])
    
    r2 = requests.get('http://flightaware.com' + arrived_links[i])
    soup2 = BeautifulSoup(r2.content)

    track_log_links = []

    table_set = soup2.find_all('table')
    track_log_link = find_track_log_link(table_set)

    if (track_log_link is None):
        continue
    
    htmp = track_log_link.get('href')
    r3 = requests.get('http://flightaware.com' + htmp)
    soup3 = BeautifulSoup(r3.content)

    tables = soup3.find_all('table',id='tracklogTable')
    track_log_table = tables[0]

    track_rows = track_log_table.find_all('tr')
    

    samples = []
    for row in track_rows:
        values = row.find_all('td')
        if (len(values) == 10):
            sample = {'edt': values[0].text,
                      'lat': values[1].text,
                      'lon': values[2].text,
                      'course': values[3].text,
                      'direction': values[4].text,
                      'knots': values[5].text,
                      'mph': values[6].text,
                      'feet': values[7].text,
                      'rate': values[8].text.strip(),
                      'facility': values[9].text}
            samples.append(sample)

    flight_data = {'link': arrived_links[i],
                       'data': samples}

    flights.append(flight_data)


              
            
#response_track = 
#soup_track = BeautifulSoup(response_track)
#tables = find_all('table',id='tracklogTable')
#trackLogTable = tables[0]

