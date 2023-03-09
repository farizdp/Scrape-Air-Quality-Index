import requests
import prettytable as pt
from bs4 import BeautifulSoup

r1 = requests.get('https://www.iqair.com/indonesia/jakarta')
if r1.status_code == 200:
    html1 = BeautifulSoup(r1.content, "html.parser")
    update_1 = html1.time.string
    aqi_value_1 = html1.find('p', class_="aqi-value__value").string
    aqi_status_1 = html1.find('span', class_="aqi-status__text").string
    pollutant_1 = html1.find('p', class_="number-above-time").string

r2 = requests.get('https://www.aqi.in/id/dashboard/indonesia/jakarta')
if r2.status_code == 200:
    html2 = BeautifulSoup(r2.content, "html.parser")
    update_2 = html2.find('p', class_="card-location-time").string.replace('Pembaharuan Terakhir: ', '')
    aqi_value_2 = html2.find('td', class_="AQI_toggle curr").string
    aqi_status_2 = html2.find('td', class_="AQI_text-1").string
    pollutant_2 = html2.find('span', class_="times_value").string

table = pt.PrettyTable()
table.title = 'Air Quality Index Jakarta'
table.field_names = ['Parameter', 'IQAir', 'AQI']
table.align['Parameter'] = 'l'
table.add_row(['Update',    str(update_1),      str(update_2)])
table.add_row(['Value',     str(aqi_value_1),   str(aqi_value_2)])
table.add_row(['Status',    str(aqi_status_1),  str(aqi_status_2)])
table.add_row(['Pollutant', str(pollutant_1),   str(pollutant_2)])
print(table)