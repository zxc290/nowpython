import requests


def get_city_weather(ip):
    # 获取城市
    find_city='http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    find_city_response=requests.get(find_city)
    city=find_city_response.json()['data']['city']

    # 获取天气
    find_weather='https://free-api.heweather.com/s6/weather/now?location=' + city + '&key=7e9832bd2d1541dc9f6f9c5b5666818f'
    find_weather_response=requests.get(find_weather)
    weather=find_weather_response.json()['HeWeather6'][0]['now']
    tmp = weather['tmp']
    cond = weather['cond_txt']

    return {'city': city, 'tmp': tmp, 'cond': cond}
