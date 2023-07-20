from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from mausamApi.settings import API_KEY

import requests
import datetime

# Create your views here.
def index(request):
    
    current_weather_url='https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    #one call is ultimate ...return dail,minutely,hourly and alerts response, we want just daily
    
    forecast_url='https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    
    if request.method=='POST':
        city= request.POST['city']
        try:
            weather_data1 ,daily_forecasts1 =fetch_weather_and_forecast(city , current_weather_url,forecast_url)
        except:
            return HttpResponseRedirect('/cityerror')
        
        context ={
            "weather_data1":weather_data1,
            "daily_forecasts1":daily_forecasts1[:7]
        }
        return render(request,'weatherapp/index.html',context)
        
    else:
        return render(request,'weatherapp/index.html')
    
    
def fetch_weather_and_forecast(city,current_weather_url,forecast_url):
    response =requests.get (current_weather_url.format(city, API_KEY)).json()
    
    print(response)
    print('\n\n\n\n')
# https://openweathermap.org/current#current_JSON >>response will be in this format
    
    lat, lon= response['coord']['lat'], response['coord']['lon']
    
    print('\n\n\n\n')    
    
    forecast_response = requests.get(forecast_url.format(lat, lon, API_KEY)).json() 
#https://openweathermap.org/api/one-call-3#example >>response details here


    print(forecast_response)
    
    print('\n\n\n\n')    


    weather_data = {
        'city': city.upper(),
        'temperature': round(response['main']['temp']-273.15, 2),
        'description':response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }
    
    daily_forecasts = []
    for daily_data in forecast_response['daily']:
        daily_forecasts.append({
            'day':datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            "min_temp": round(daily_data['temp']["min"]- 273.15,2),
            "max_temp": round(daily_data['temp']["max"]- 273.15,2),
            # "description":daily_data['summary'],
            "description":daily_data['weather'][0]['description'],
            'icon':daily_data['weather'][0]['icon']
        })
        
    return weather_data, daily_forecasts



def error_message(request):
    return render(request, "weatherapp/error.html")