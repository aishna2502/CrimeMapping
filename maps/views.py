from django.shortcuts import render
from django.core import serializers
from crimeReporting.models import *
from django import forms
from .forms import *
from datetime import datetime
from dateutil.parser import parse
import json
# Create your views here.
from prediction.fusioncharts import FusionCharts

def map_render(request):
    json_serializer = serializers.get_serializer("json")()
    reports = json_serializer.serialize(FIR_REPORT.objects.all(), ensure_ascii=False)
    context = {
        'report' : reports,
    }

    # request_page(request)
    return render(request, 'map.html',context)

def request_page(request):
    reports=[]
    json_serializer = serializers.get_serializer("json")()
    if (request.GET.get('mybtn')):
        somevar = (request.GET.getlist('crime'))
        date_start = (request.GET.get('date_crime_start'))
        date_end = (request.GET.get('date_crime_end'))
        status_var=(request.GET.getlist('status'))

        if not somevar:
            if not date_end and not date_start:
                if not status_var:
                    report = FIR_REPORT.objects.all()
                else :
                    report = FIR_REPORT.objects.filter(STATUS__in=status_var)
            else:
                if not status_var:
                    report = FIR_REPORT.objects.filter(DATE_CRIME__range=[date_start, date_end])
                else:
                    report = FIR_REPORT.objects.filter(STATUS__in=status_var)

        else:
            if not date_end and not date_start:
                if not status_var:
                    report = FIR_REPORT.objects.filter(CRIME_TYPE__in = somevar)
                else:
                    report = FIR_REPORT.objects.filter(CRIME_TYPE__in=somevar,STATUS__in=status_var)
            elif date_end and date_start:
                if not status_var:
                    report = FIR_REPORT.objects.filter(CRIME_TYPE__in = somevar,DATE_CRIME__range=[date_start, date_end])
                else:
                    report = FIR_REPORT.objects.filter(CRIME_TYPE__in=somevar,STATUS__in=status_var,DATE_CRIME__range=[date_start, date_end])

        reports = json_serializer.serialize(report, ensure_ascii=False)

    context = {
        'report': reports,
    }
    return render(request, 'map.html',context)


def map_render_filter(request):
    json_serializer = serializers.get_serializer("json")()
    reports = json_serializer.serialize(FIR_REPORT.objects.all(), ensure_ascii=False)
    context = {
        'report' : reports,
    }
    return render(request, 'map.html',context)

def crime_status(request):
    if request.method == 'GET':

        crime_id= request.GET.get('crime_id')
        global detail
        detail=  FIR_REPORT.objects.filter(ID = crime_id)
        report = CRIME_TIMELINE.objects.filter(CRIME_ID = crime_id)
        json_serializer = serializers.get_serializer("json")()
        reports = json_serializer.serialize(report, ensure_ascii=False)
        details= json_serializer.serialize(detail, ensure_ascii=False)
        users = json_serializer.serialize(USER.objects.all(), ensure_ascii = False)
        form = UPDATE_FORM()
        context = {
            'reports': reports,
            'details': details,
            'users': users,
            'form': form
        }
        return render(request, 'status_report.html', context)


def update_crime(request):
    if request.method == 'GET':
        #crime_id = request.GET.get('crime_id')
        form = UPDATE_FORM(request.GET)
        if form.is_valid():
            data = form.save(commit=False)
            data.CRIME_ID = detail[0]
            var=USER.objects.filter(NAME='AISHNA')
            data.UPDATED_BY = var[0]
            #request.session.get('username')
            data.save()
            return render(request, 'done.html')

    return render(request, 'done.html')




def report(request):

    report = FIR_REPORT.objects.all()
    dataSource = {}
    dataSource['chart'] = {
        "theme": "fint",
        "palette": "2",
        "caption": "Product Comparison",
        "showlabels": "1",
        "showvalues": "0",
        "numberprefix": "$",
        "showsum": "1",
        "decimals": "0",
        "useroundedges": "1",
        "legendborderalpha": "0",
        "showborder": "0"
    }
    dataSource["categories"]=[{
                "category": [
                {
                    "label": "Monday",

                },
                {
                    "label": "Tuesday",

                },
                {
                    "label": "Wednesday",

                },
                {
                    "label": "Thursday",

                },
                {
                    "label": "Friday",

                },
                {
                    "label": "Saturday",

                },
                {
                    "label": "Sunday",

                }
            ]
        }]
    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    json_serializer = serializers.get_serializer("json")()
    reports = json_serializer.serialize(report, ensure_ascii=False)
    print(reports)
    final={}
    dict_monday = {}
    dict_tuesday = {}
    dict_wednesday = {}
    dict_thursday = {}
    dict_friday = {}
    dict_saturday = {}
    dict_sunday = {}
    reports=json.loads(reports)
    for i in reports:
        date = i["fields"]["DATE_CRIME"]
        date=datetime.strptime(date, '%Y-%m-%d')

        print (type(date))
        day = date.weekday()
        if day ==0:
             if i["fields"]["CRIME_TYPE"] in dict_monday:
                 dict_monday[i["fields"]["CRIME_TYPE"]]=dict_monday[i["fields"]["CRIME_TYPE"]]+1
             else:
                 dict_monday[i["fields"]["CRIME_TYPE"]]=1
        elif day==1:
            if i["fields"]["CRIME_TYPE"] in dict_tuesday:
                dict_tuesday[i["fields"]["CRIME_TYPE"]] = dict_tuesday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_tuesday[i["fields"]["CRIME_TYPE"]] = 1
        elif day==2:
            if i["fields"]["CRIME_TYPE"] in dict_wednesday:
                dict_wednesday[i["fields"]["CRIME_TYPE"]] = dict_wednesday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_wednesday[i["fields"]["CRIME_TYPE"]] = 1
        elif day==3:
            if i["fields"]["CRIME_TYPE"] in dict_thursday:
                dict_thursday[i["fields"]["CRIME_TYPE"]] = dict_thursday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_thursday[i["fields"]["CRIME_TYPE"]] = 1
        elif day==4:
            if i["fields"]["CRIME_TYPE"] in dict_friday:
                dict_friday[i["fields"]["CRIME_TYPE"]] = dict_friday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_friday[i["fields"]["CRIME_TYPE"]] = 1
        elif day==5:
            if i["fields"]["CRIME_TYPE"] in dict_saturday:
                dict_saturday[i["fields"]["CRIME_TYPE"]] = dict_saturday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_saturday[i["fields"]["CRIME_TYPE"]] = 1
        elif day==6:
            if i["fields"]["CRIME_TYPE"] in dict_sunday:
                dict_sunday[i["fields"]["CRIME_TYPE"]] = dict_sunday[i["fields"]["CRIME_TYPE"]] + 1
            else:
                dict_sunday[i["fields"]["CRIME_TYPE"]] = 1

    print(dict_sunday)
    print(dict_monday)
    print(dict_tuesday)
    print(dict_wednesday)
    print(dict_thursday)
    print(dict_friday)
    print(dict_saturday)
    crimedata=['rape','kidnap','theft']
    dataSource['dataset'] = []
    for i in crimedata:
        data_outer = {}
        data_outer['seriesname']= i
        data=[]
        dict={}

        if i in dict_monday:
            dict["value"] = str(dict_monday[i])
        else:
            dict["value"] = "0"
        data.append(dict)
        dict = {}
        if i in dict_tuesday.keys():
            dict["value"] = str(dict_tuesday[i])
        else:
            dict["value"]= "0"
        data.append(dict)
        print(data)
        dict = {}
        if i in dict_wednesday.keys():
            dict["value"] = str(dict_wednesday[i])
        else:
            dict["value"] = str(0)
        data.append(dict)
        dict = {}
        if i in dict_thursday.keys():
            dict["value"] = str(dict_thursday[i])
        else:
            dict["value"] = "0"
        data.append(dict)
        dict = {}
        if i in dict_friday.keys():
            dict["value"] = str(dict_friday[i])
        else:
            dict["value"] = "0"
        data.append(dict)
        dict = {}
        if i in dict_saturday.keys():
            dict["value"] = str(dict_saturday[i])
        else:
            dict["value"] = "0"
        data.append(dict)
        dict = {}
        if i in dict_sunday.keys():
            dict["value"] = str(dict_sunday[i])
        else:
            dict["value"] = "0"
        data.append(dict)
        print (type(str(data)))
        data_outer['data']=str(data)

        dataSource['dataset'].append(data_outer)
    print (dataSource)
    column2D = FusionCharts("stackedcolumn2d", "ex10", "500", "300", "chart-1", "json", dataSource)
    context = {
        'data' : dataSource,
        'total': column2D.render(),
    }

    return render(request, 'report.html', context)

#EXPECTED OUTPUT
#https://jsfiddle.net/15zbv887/331/
'''
FusionCharts.ready(function() {
    var revenueChart = new FusionCharts({
        type: 'stackedcolumn2d',
        renderAt: 'chart-container',
        width: '500',
        height: '300',
        dataFormat: 'json',
        dataSource: {
            "chart": {
                "theme": "fint",
        "palette": "2",
        "caption": "Product Comparison",
        "showlabels": "1",
        "showvalues": "0",
        "numberprefix": "$",
        "showsum": "1",
        "decimals": "0",
        "useroundedges": "1",
        "legendborderalpha": "0",
        "showborder": "0"
            },
            "categories": [
                {
                     "category": [
                {
                    "label": "Monday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                },
                {
                    "label": "Tuesday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                },
                {
                    "label": "Wednesday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                },
                {
                    "label": "Thursday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                },
                {
                    "label": "Friday",
                    "stepSkipped": false,
                    "appliedSmartLabel":true
                },
                {
                    "label": "Saturday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                },
                {
                    "label": "Sunday",
                    "stepSkipped": false,
                    "appliedSmartLabel": true
                }
            ]
                }
            ],
            "dataset": [{'seriesname': 'rape', 'data': [{'value': '1'}, {'value': '0'}, {'value': '1'}, {'value': '0'}, {'value': '0'}, {'value': '0'}, {'value': '0'}]}, {'seriesname': 'kidnap', 'data': [{'value': '0'}, {'value': '0'}, {'value': '1'}, {'value': '0'}, {'value': '0'}, {'value': '0'}, {'value': '0'}]}, {'seriesname': 'theft', 'data': [{'value': '1'}, {'value': '0'}, {'value': '3'}, {'value': '0'}, {'value': '0'}, {'value': '1'}, {'value': '0'}]}],
        }
    }).render();
});
'''
