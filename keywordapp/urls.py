from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Work, name='work'),
    path('house/', House, name='house'),
    # =============== REFRESH CHECK
    path('refresh-check/',
         RefreshConditionCheck, name='refresh-page'),
    # =============== WORK
    path('work-refresh/',
         RefreshWork, name='work-refresh-page'),
    path('work-collect/',
         CollectWorkFromDB, name='work-collect-page'),
    # =============== HOUSE
    path('house-refresh/',
         RefreshHouse, name='house-refresh-page'),
    path('house-collect/',
         CollectHouseFromDB, name='house-collect-page'),
]
