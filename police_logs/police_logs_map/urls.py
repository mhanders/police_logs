from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^create/', views.create, name='create'),
	url(r'^reports/', views.create_report, name='create_report')
]