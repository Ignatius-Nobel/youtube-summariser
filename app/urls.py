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
    path('saved-detail/<int:content_id>/',views.saved_detail,name='saved-detail'),
    path('download-chat/<int:video_id>/', views.download_chat_pdf, name='download_chat_pdf'),
    path('download-audio/<int:video_id>/', views.generate_audio, name='download-audio'),
    path('transcript-audio/<int:video_id>/', views.transcript_audio, name='transcript-audio'),
    path('remove-content/<int:pk>/', views.remove_content,name="remove-content"),
    path('get-progress/', views.get_current_progress, name='get_current_progress'),
    path('get-blog/<int:video_id>/', views.generate_blog, name='get-blog'),
    path('saved-blog/<int:video_id>/', views.saved_generate_blog, name='saved-blog'),
]