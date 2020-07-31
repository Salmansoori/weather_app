import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from django.contrib import messages
# Create your views here
# 
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')




def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=Your ApiKey'
    
    
    error_msg=''
    message=''
    message_class=''

    if request.method =="POST":
        form= CityForm(request.POST)

        if form.is_valid():
            new_city= form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                     error_msg="City does not exist in the world"
            else:
                error_msg="City allready exist"         
        
        if error_msg:
            message=error_msg
            message_class='is-danger'
        else:
            message_class='City added successfully'    
            message_class='is-success'

    form=CityForm()
    cities=City.objects.all()

    weather_data=[]
    for city in cities:
    
        r=requests.get(url.format(city)).json()

        city_weather={
         'city': city.name,
         'temperature':r['main']['temp'],
         'description':r['weather'][0]['description'],
         'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context={'weather_data': weather_data ,'form':form ,'message':message, 'message_class':message_class}
    return render(request, 'weather/weather.html',context)

