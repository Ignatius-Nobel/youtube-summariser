from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get-result/', views.get_result, name='get_result'),
    path('result-page/<int:content_id>/', views.result_page, name='result_page'),
    path('login',views.user_login,name='login'),
    path('register',views.user_register,name='register'),
    path('logout',views.user_logout,name='logout'),
    path('saved',views.saved_content,name='saved'),
    path('download-chat/<int:video_id>/', views.download_chat_pdf, name='download_chat_pdf'),
    path('download-audio/<int:video_id>/', views.generate_audio, name='download-audio'),
]