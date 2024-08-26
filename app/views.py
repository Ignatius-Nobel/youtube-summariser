from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from pytube import YouTube
from django.conf import settings
import os
from .models import GeneratedContent,VideoDetail
import yt_dlp as youtube_dl
links = []
# Create your views here.
@login_required
def home(request):
    return render(request,"index.html")

## get link , retreive details , save details
def get_result(request):
    if request.method == "POST":
        try:
            logged_user = request.user
            links = request.POST.getlist('links')
            content_title = get_details(links[0])[0]
            generated_content = GeneratedContent.objects.create(
                user = logged_user,
                name=content_title
            )
            generated_content.save()
            print(generated_content.id)
            for link in links:
                title, author, length, pub_date = get_details(link)
                audio_path = download_audio(link)
                print(audio_path)
                video_details = VideoDetail.objects.create(
                    generated_content=generated_content,
                    title=title,
                    author=author,
                    length=length,
                    publish_date=pub_date,
                    youtube_link = link,
                )
                video_details.save()

            # Redirect to the result page after processing
            return redirect('result_page',generated_content.id)
        except Exception as e:
            messages.error(request, 'Please enter a valid link!!!')
            print(e)
            return redirect('home')

# result page
def result_page(request,content_id):
    content = get_object_or_404( GeneratedContent,id=content_id)
    video_details = VideoDetail.objects.filter(generated_content=content).order_by('id')
    return render(request, 'result.html', {'content': content,'video_detail': video_details})

# get details
def get_details(link):
    yt = YouTube(link)
    if yt:
        title = yt.title
        author = yt.author
        length = yt.length
        pub_date = yt.publish_date
        return title,author,length,pub_date
    else:
        return False

# Download audio
def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Adjust quality as needed (128, 192, 256, etc.)
        }],
        'outtmpl': f'{settings.MEDIA_ROOT}/%(title)s.%(ext)s',  # Save with video title as file name
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        file_name = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    
    # Print the full path of the saved MP3 file
    saved_file_path = os.path.abspath(file_name)
    return saved_file_path

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials!!!'
            return render(request,'login.html',{'error_message':error_message})
    return render(request,"login.html")
def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeatPassword')

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                return redirect('login')
            except:
                error_message = 'Error creating account!'
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message = 'Password do not match!'
            return render(request,'register.html',{'error_message':error_message})
    return render(request,"register.html")

def user_logout(request):
    logout(request)
    return redirect('home')

def saved_content(request):
    generated_content = GeneratedContent.objects.filter(user=request.user)
    # video_detail = VideoDetail.objects.filter(generated_content=generated_content)
    return render(request,"saved.html",{'generated_content':generated_content})


