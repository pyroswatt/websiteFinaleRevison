"""water_clean URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog import views

urlpatterns = [
    #url(r'^accueil$', views.home),  # Accueil du blog
    url(r'^admin/', admin.site.urls),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
    url(r'^accueil$', views.accueil, name='accueil'),
    url(r'^accueil/principe/$', views.call_principe, name='call_principe'),
    url(r'^accueil/services/$', views.call_services, name='call_services'),
    url(r'^accueil/clients/$', views.call_clients, name='call_clients'),
    url(r'^accueil/plateforme/$', views.call_plateforme, name='call_plateforme'),
    url(r'^accueil/plateformeUser/$', views.call_plateformeUserRecord, name='call_plateformeUserRecord'),
    url(r'^accueil/plateformeUserRecord/$', views.call_recordCredentialsUser, name='call_recordCredentialsUser'),
    url(r'^accueil/configurationPlateforme/$', views.call_configurationPlateforme, name='call_configurationPlateforme'),
    url(r'^accueil/statusPlateforme/$', views.call_statusPlateforme, name='call_statusPlateforme'),
    url(r'^accueil/statusPlateformee/$', views.call_fillChart, name='call_fillChart'),
    url(r'^accueil/plateformeMonitoringPlateforme/$', views.call_monitoringPlateforme, name='call_monitoringPlateforme')
]

