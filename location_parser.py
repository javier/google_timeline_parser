import csv
import datetime
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

API_KEY = "XXX"

def key_for(lat,lng):
    return str(round(lat,3))+'#'+str(round(lng,3))

def city_for(lat,lng, cached_locs):
    city = cached_locs.get(key_for(lat, lng))
    if city:
        return city
    
    base_url='https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}&result_type=locality'
    try:
        response = requests.get(base_url.format(lat, lng, API_KEY)).json()
        city = response['results'][0]['formatted_address'].replace(',','.')
    except:
        city = 'Error' 
    cached_locs[key_for(lat,lng)]=city
    return city


cached_locs = {}

with open('filtered_locations.csv','rb') as csv_in, open('output.csv','wb') as csv_out:
    c_out=csv.writer(csv_out)
    c_in=csv.reader(csv_in)
    for row in c_in:
        lat = int(row[0])/10000000.0
        lng = int(row[1])/10000000.0
        timestamp = int(row[2])
        date = datetime.datetime.fromtimestamp(timestamp/1000.0).strftime('%Y-%m-%d')
        city = city_for(lat, lng, cached_locs).encode('utf-8')
        c_out.writerow([timestamp,date,lat,lng,city])

