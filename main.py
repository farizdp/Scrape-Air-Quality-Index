import requests, telepot, os
import prettytable as pt
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
id_telegram = os.getenv('ID_TELEGRAM')
token = os.getenv('TOKEN')
bot = telepot.Bot(token)

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
    pollutant_2 = html2.find('span', class_="Pollutants_sensor_text pm25Val").string

table = pt.PrettyTable()
table.title = 'Air Quality Index Jakarta'
table.field_names = ['Parameter', 'IQAir', 'AQI']
table.align['Parameter'] = 'l'
table.add_row(['Update',    str(update_1),      str(update_2)])
table.add_row(['Value',     str(aqi_value_1),   str(aqi_value_2)])
table.add_row(['Status',    str(aqi_status_1),  str(aqi_status_2)])
table.add_row(['Pollutant', str(pollutant_1),   str(pollutant_2)])

text = "AQI Monitoring Jakarta\n\n```{0}```".format(table)

im = Image.new("RGB", (640, 180), "white")
draw = ImageDraw.Draw(im)
path = os.path.dirname(__file__) + '/'
font = ImageFont.truetype(path + "font/FreeMono.ttf", 15)
draw.text((10, 10), str(table), font=font, fill="black")

im.save(path + "out/aqi.png")
bot.sendPhoto(id_telegram, photo=open(path + "out/aqi.png", 'rb'))