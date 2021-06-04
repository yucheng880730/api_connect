from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
from pprint import pprint
import json
import math
import geocoder

app_id = 'defd5cd9124746788be43e840b5b66b8'
app_key = 'rdKMsBfEiW4eXe4d5a9nshnfGWs'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        #print(xdate)
        #print(type(xdate))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        #print(hashed)
        signature = base64.b64encode(hashed.digest()).decode()
        #print(hashed.digest())
        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        #print(authorization)
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':

    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/Station?$format=JSON', headers= a.get_auth_header())
    #pprint(response.content)
    data = json.loads(response.text)
    #pprint(data)

    location = geocoder.ip('me').latlng
    current_latitude = location[0]
    current_longitude = location[1]
    #pprint(geocoder.ip('me'))
    #pprint(geocoder.ip('me').latlng)

    #current_latitude = 25.03544
    #current_longitude = 121.499922
    within_range = 9999
    result_name = '台北'

    for station in data['Stations']:
        #print(station)
        lat = station['StationPosition']['PositionLat']
        lon = station['StationPosition']['PositionLon']
        result = math.sqrt((current_latitude-lat)**2 + (current_longitude-lon)**2)
        if within_range > result:
            within_range = result
            result_name = station['StationName']['Zh_tw']
            station_id = station['StationID']
        #pprint(result)
        #pprint(station['StationName'])
    #pprint(station_id)
    pprint("距離最近的車站:" + result_name)

    
    datetime_dt = datetime.now()
    #datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")

    '''
    h1 = datetime_dt.hour
    m1 = datetime_dt.minute
    s1 = datetime_dt.second
    print(h1,m1,s1)
    '''
    
    pprint("目前時間:" + str(datetime_dt))

        
    response2 = request('get','https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/DailyStationTimetable/Today/Station/'+ station_id +'?$format=JSON',headers = a.get_auth_header())
    #pprint(response2.content)
    data2 = json.loads(response2.text)
    dt = datetime.now()
    #print(dt)
    #pprint(data2)
    h = dt.hour
    m = dt.minute
    s = dt.second
    difference = 9999
    within_range = 60 *24
    for train in data2['StationTimetables'][0]['TimeTables']:
            arrivaltime = train['ArrivalTime']
            date = datetime.strptime(arrivaltime, '%H:%M')
            #print(date)
            result2 = 60 * date.hour + date.minute - 60 * h - m
            if within_range > result2 & result2 >= 0:
                within_range = result2
                result_name = train['TrainNo']
                result_time = train['ArrivalTime']
    
    pprint("即將抵達的火車車次為:" + result_name)
    pprint("即將抵達的時間為:" + result_time)
    #pprint(within_range * 60)
    pprint("還有幾秒進站:" + str(within_range * 60))
    
    
        
    
        
        
    
    

  

    