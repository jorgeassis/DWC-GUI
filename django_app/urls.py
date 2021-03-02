
from django.contrib import admin
from django.urls import path, include

from . import views
from .views import recordsDetailView, recordsDetailViewSimple, literatureView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homeView, name='home'),
    path('species', views.speciesView, name='species'),
    path('records', views.recordsView, name='records'),
    path('literature', views.literatureView, name='literature'),
    path('records/<id>/', recordsDetailView, name='record-detail'),
    path('records-simple/<id>/', recordsDetailViewSimple, name='record-detail-simple'),
    path('users', views.usersView, name='users'),
    path('search_autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('download-records/', views.DownloadResultsView, name='download-records'),

]
