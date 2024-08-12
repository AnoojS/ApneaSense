from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .models import *
from .forms import *

import numpy as np

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def login(request):
    form=LoginForm()
    if request.method == 'POST':
        form=LoginForm(request.POST)
        
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html',{'form':form})
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request,'login.html',{'form':form})
    
def logout(request):
    auth.logout(request)
    return redirect('/')
    
@login_required
@never_cache
def home(request):
    client = Client.objects.get(user=request.user)
    context = {
        'clientname': client.firstname
    }
    return render(request,'home.html',context)

@login_required
@never_cache
def report(request,record_id):
    object = get_object_or_404(Record, id=record_id)
    prediction=object.prediction
    prediction=np.array(prediction)
    prediction=prediction.astype(int)

    counts = np.bincount(prediction.flatten())
    events=[]
    for i in range(prediction.shape[0]):
        if prediction[i]==0:
            events.append('Normal')
        elif prediction[i]==1:
            events.append('Apnea')

    apn=str(prediction.shape[0])+' Events Recorded, '+str(counts[0])+' were found to be Normal Breathing and '+str(counts[1])+' were found to be Obstructive Apnea events.'

    if(counts[1]>=50):
        result='You were found to be Obstructive Apnea Positive.'
    else:
        result='You are a healthy sleeper'

    context = {
        'signal': object.signal,
        'datetime':object.datetime,
        'apn':apn,
        'result':result,
        'events':events,
    }
    return render(request,'report.html',context)

@login_required
@never_cache
def records(request):
    objects = Record.objects.filter(user=request.user).order_by('-datetime')
    context = {
        'objects': objects
    }
    return render(request, 'records.html', context)

@login_required
@never_cache
def instructions(request):
    return render(request,'instructions.html')

@login_required
@never_cache
def profile(request):
    objects = Client.objects.filter(user=request.user)
    context = {
        'objects': objects
    }
    return render(request,'profile.html',context)
