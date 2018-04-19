from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import app.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', app.views.login, name='login'),
    url(r'^$', app.views.logout, name='logout'),
    url(r'^$', app.views.main, name='main'),
    url(r'^$', app.views.new_project, name='new_project'),
    url(r'^$', app.views.delete_project, name='delete_project'),
    url(r'^$', app.views.new_goal, name='new_goal'),
    url(r'^$', app.views.complete_goal, name='complete_goal'),
    url(r'^$', app.views.revert_goal, name='revert_goal'),
    url(r'^$', app.views.add_work, name='add_work'),
    url(r'^$', app.views.project_management, name='project_management'),
    url(r'^$', app.views.analytics, name='analytics'),
    url(r'^$', app.views.register, name='register'),
    url(r'^$', app.views.forgot, name='forgot'),
    url(r'^$', app.views.load_user, name='load_user')
]
