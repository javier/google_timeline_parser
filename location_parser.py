import csv
from datetime import datetime, timedelta
import sys

import requests

from lxml import etree 


reload(sys)
sys.setdefaultencoding('utf-8')

cached_locs = {}
api_key = open('API_KEY.secret.txt').read()


#https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude
#for country, 1 decimal digit is more than we need. It will differentiate also cities usually. Check link above
#the more digits, the more precission, but also the more http request and the slower it will be
def key_for(lat,lng):
    return str(round(lat,1))+'#'+str(round(lng,1))

def city_for(lat,lng, cached_locs):
    city = cached_locs.get(key_for(lat, lng))
    if city:
        return city
    
    base_url='https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}&result_type=locality'
    try:
        response = requests.get(base_url.format(lat, lng, api_key)).json()
        city = response['results'][0]['formatted_address'].replace(',','.')
    except:
        city = 'Error' 
    cached_locs[key_for(lat,lng)]=city
    return city

def parse_foursquare_date(date_str):
     dt,tz=date_str.rsplit(' ',1)
     dt_obj=datetime.strptime(dt,'%a, %d %b %y %H:%M:%S')
     tz_delta = timedelta(hours=int(tz[1:3]),minutes=int(tz[3:])) 
     if tz[0]=='+':    
         dt_obj-= tz_delta
     else:     
         dt_obj+= tz_delta
     return dt_obj    
     

with open('inputs/filtered_locations.csv','rb') as csv_in, open('inputs/foursquare.kml', 'rb') as kml_in, open('outputs/output.csv','wb') as csv_out:
    c_out=csv.writer(csv_out)
    c_in=csv.reader(csv_in)
    k_in=csv.reader(kml_in)
    
    for row in c_in:
        lat = int(row[0])/10000000.0
        lng = int(row[1])/10000000.0
        timestamp = int(row[2])
        date = datetime.fromtimestamp(timestamp/1000.0).strftime('%Y-%m-%d')
        city = city_for(lat, lng, cached_locs).encode('utf-8')
        if city =="Error":
            continue
         
        c_out.writerow([timestamp,date,lat,lng,city,'location_history', None])
    
    tree = etree.parse(kml_in) #("inputs/5000foursquare.kml")        
    for placemark in tree.findall('.//Placemark'):
        name = placemark.find('name').text
        lng,lat = placemark.find('Point/coordinates').text.split(',')
        lng = float(lng)
        lat = float(lat)
        foursquare_date = parse_foursquare_date(placemark.find('published').text) 
        timestamp =  (foursquare_date - datetime(1970, 1, 1)).total_seconds() * 1000
        date = foursquare_date.strftime('%Y-%m-%d')
        city = city_for(lat, lng, cached_locs).encode('utf-8')        
        if city =="Error":
            continue
        c_out.writerow([timestamp,date,lat,lng,city,'foursquare',name])
        
        

