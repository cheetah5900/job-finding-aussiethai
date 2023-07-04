from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Work, name='work'),
    path('house/', House, name='house'),
    path('test/', testTest, name='test-test'),
    path('keyword-manager/', KeywordManager, name='keyword-manager'),
    path('post-manager/', PostManager, name='post-manager'),
    path('del-keyword/<int:pk>/', DeleteKeyword),
    path('del-post-work/<int:pk>/', DeletePostWork),
    path('del-post-house/<int:pk>/', DeletePostHouse),
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
