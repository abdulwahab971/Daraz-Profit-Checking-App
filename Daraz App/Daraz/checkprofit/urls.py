
from unicodedata import name
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
   
    path('',views.home,name='home'),
    path('enterRetailprices/',views.enterretailprices,name="enter_Retail_prices"),
    path('display/',views.display, name = "display")
    
]

