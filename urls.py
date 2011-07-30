from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tabtracker/', include('tabtracker.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^tabtrack/adduser/(?P<fbID>\d+)/$', 'tabtracker.tabtrack.views.adduser'),
    (r'^tabtrack/getuser/(?P<fbID>\d+)/$', 'tabtracker.tabtrack.views.getuser'),
    (r'^tabtrack/getuserdata/(?P<fbID>\d+)/$', 'tabtracker.tabtrack.views.getuserdata'),
    (r'^tabtrack/addtab/(?P<fbID1>\d+)/(?P<fbID2>\d+)/$', 'tabtracker.tabtrack.views.addtab'),
    (r'^tabtrack/additem/(?P<tabID>\d+)/(?P<amount>\d+)/$', 'tabtracker.tabtrack.views.additem'),
    (r'^tabtrack/$', 'tabtracker.tabtrack.views.index')

)
