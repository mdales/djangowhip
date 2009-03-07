# Create your views here.

import simplejson

from twfy import TWFY

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django import forms


from djangowhip import settings
from djangowhip.pw.models import *

def mp_info(request, mp_id):
    
    mp = get_object_or_404(MP, mp_id=mp_id)
    
    # we want a lat/long for this MP's constituency
    t = TWFY.TWFY(settings.TWFY_API_KEY)
    res = t.twfy.getGeometry(output='js', name=mp.constituency)
    data = simplejson.loads(res)
    
    
    point = {'latitude': data['centre_lat'],
        'longitude': data['centre_lon']}
    
    
    return render_to_response('mpinfo.html', 
        {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY, 
        'mp': mp, 'points': [point,]},)
