from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
def home_page(request):
    print("home page requested")
    friends=[
        'Api Made',
        'at',
        'techahead'
    ]
    return JsonResponse(friends,safe=False)

