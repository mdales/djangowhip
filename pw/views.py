##############################################################################
##############################################################################
##
## Copyright Michael Dales (c) 2009. Made available under
## the Affero GNU Public License - see COPYING file for details.
##
##############################################################################
##############################################################################

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


def overview(request):
    return render_to_response('overview.html')



def mp_list(request):
    mp_list = MP.objects.all()#.order_by('last_name')
    
    return render_to_response('mplist.html',
        {'mp_list': mp_list})


def mp_info(request, mp_id):
    
    mp = get_object_or_404(MP, mp_id=mp_id)
    
    # we want a lat/long for this MP's constituency
    t = TWFY.TWFY(settings.TWFY_API_KEY)
    res = t.twfy.getGeometry(output='js', name=mp.constituency)
    data = simplejson.loads(str(res))
    
    
    point = {'latitude': data['centre_lat'],
        'longitude': data['centre_lon']}
    
    
    return render_to_response('mpinfo.html', 
        {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY, 
        'mp': mp, 'points': [point,]},)


def division_list(request):
    div_list = Division.objects.all().order_by('division_date')
    
    return render_to_response('divisionlist.html',
        {'division_list': div_list})
        
        
def division_info(request, division_id):
    division = get_object_or_404(Division, division_id=division_id)
    
    vote_list = Vote.objects.filter(division=division)

    t = TWFY.TWFY(settings.TWFY_API_KEY)

    points = []
    errors = 0
    for vote in vote_list:
        try:
            c = ConstintuencyInfo.objects.get(name=vote.mp.constituency)
    
            point = {'latitude': c.lat,
                'longitude': c.lon,
                'voteyes': vote.vote.lower() == 'aye',
                'mp': vote.mp}
        except ConstintuencyInfo.DoesNotExist:
            errors += 1
        else:
            points.append(point)

    return render_to_response('divisioninfo.html', 
        {'division': division,
        'errors': errors,
        'points': points,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'vote_count': len(vote_list),
        })



def _populate_constituency_info():
    
    mp_list = MP.objects.all()
    
    t = TWFY.TWFY(settings.TWFY_API_KEY)
    
    for mp in mp_list:
        try:
            constitunecy = ConstintuencyInfo.objects.get(name=mp.constituency)    
        except ConstintuencyInfo.DoesNotExist:
            pass
        else:
            continue
        
        res = t.twfy.getGeometry(output='js', name=mp.constituency)
        try:
            data = simplejson.loads(res)
        except UnicodeDecodeError:
            continue
    
        try:
            point = {'latitude': data['centre_lat'],
                'longitude': data['centre_lon'],}
        except KeyError:
            continue
            
        constitunecy = ConstintuencyInfo.objects.create(
            name=mp.constituency,
            lat = float(point['latitude']),
            lon = float(point['longitude']))
        constitunecy.save()
            
