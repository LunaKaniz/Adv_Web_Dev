"""
URL configuration for climate_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Climate API - Luna Kaniz</h1>
        <ul>
            <li><a href="/api/climate/">All Climate Records</a></li>
            <li><a href="/api/climate/filter/?station_id=BASEL&date=2000-01-01">Filter by Station + Date</a></li>
            <li><a href="/api/climate/averages/?station_id=BASEL&month=1">Monthly Averages</a></li>
            <li><a href="/api/climate/extremes/">Extreme Weather Records</a></li>
            <li><a href="/api/climate/delete-old/?before=2005-01-01">Delete Old Records</a> (DELETE)</li>
        </ul>
        <p>Visit <a href="/admin/">Admin Panel</a> (admin:admin123)</p>
    """, content_type="text/html")


# Add it to urlpatterns
urlpatterns = [
    path('', home),  # 👈 new homepage view
    path('admin/', admin.site.urls),
    path('api/', include('weather.urls')),
]
