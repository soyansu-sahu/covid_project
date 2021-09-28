from django.http import request
from django.shortcuts import render
import requests
import json



# Create your views here.
def home(request):
    response = requests.get("https://api.covid19api.com/total/country/india")
    result = response.json()
    result.reverse()
    return render(request,'home.html',{'data':result})

def chart(request):
    q_chart_days = 365 if (request.GET.get('chart_days') is None) else int(request.GET.get('chart_days'))
    default_chart_type = 'bar' if (request.GET.get('chart_name') is None) else request.GET.get('chart_name') 

    result = requests.get("https://api.covid19api.com/total/country/india")
    api_data = result.json()
    covid_data = {
        "date":[],
        "confirmed":[],
        "recovered":[],
        "deaths":[],
        "active":[],
    }
    api_data.reverse()
    count_days = 0
    for data in api_data:
        if count_days <= q_chart_days:
            covid_data['date'].append(data['Date'])
            covid_data['confirmed'].append(data['Confirmed'])
            covid_data['recovered'].append(data['Recovered'])
            covid_data['deaths'].append(data['Deaths'])
            covid_data['active'].append(data['Active'])
            count_days += 1

    return render(request,'chart.html',{
        'covid_data':json.dumps(covid_data),
        'default_chart_type': default_chart_type,
        'q_chart_days': q_chart_days
        })

