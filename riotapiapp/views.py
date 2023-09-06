from django.shortcuts import render
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import apifunction


# Create your views here.
def index(request):
    return render(request, 'riotapiapp/listpage.html')


def result(request):
    if request.method == 'POST':
        summonerName = request.POST['subject']
        myData = apifunction.myfunction(summonerName=summonerName)
        context = {'myData': myData}
        return render(request, 'riotapiapp/result.html', context)
