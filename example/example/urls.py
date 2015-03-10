from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^manager/$', 'app.views.home', name='home'),
    url(r'^manager_or_moderator/$', 'app.views.manager_or_moderator', name='manager_or_moderator'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
