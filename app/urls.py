from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('get-result/', views.get_result, name='get_result'),
    path('result-page/<int:content_id>/', views.result_page, name='result_page'),
]