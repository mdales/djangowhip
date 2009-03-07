##############################################################################
##############################################################################
##
## Copyright Michael Dales (c) 2009 Made available under
## the Affero GNU Public License - see COPYING file for details.
##
##############################################################################
##############################################################################

from django.conf.urls.defaults import *
from djangowhip import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djangowhip/', include('djangowhip.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('', (r'^', include('pw.urls')))



urlpatterns += patterns('django.views',
     (r'^site_media/(?P<path>.*)$', 'static.serve', 
         {'document_root': settings.MEDIA_ROOT}),

)
