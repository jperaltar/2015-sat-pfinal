from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login$', 'cultural.views.myLogin'),
    url(r'^logout$', 'cultural.views.myLogout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^update/?$', 'cultural.views.update'),
    url(r'^ayuda/?$', 'cultural.views.help'),
    url(r'^style/?$', 'cultural.views.style'),
    url(r'^rss/?$', 'cultural.views.mainRss'),
    url(r'^$', 'cultural.views.main'),
    url(r'^todas/filter/?$', 'cultural.views.filter'),
    url(r'^todas/?$', 'cultural.views.all'),
    url(r'^actividad/([^/]*)/?$', 'cultural.views.activity'),
    url(r'^comment/([\d]*)/?$', 'cultural.views.commentAct'),
    url(r'^score/([\d]*)/?$', 'cultural.views.sumScore'),
    url(r'^(.*)/add$', 'cultural.views.add'),
    url(r'^(.*)/rss$', 'cultural.views.rss'),
    url(r'^([^/]*)/pg=([\d]*)/?$', 'cultural.views.user'),
)
