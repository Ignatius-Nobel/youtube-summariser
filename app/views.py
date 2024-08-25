from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from pytube import YouTube
from .models import GeneratedContent,VideoDetail
links = []
# Create your views here.
def home(request):
    return render(request,"index.html")

## get link , retreive details , save details
def get_result(request):
    if request.method == "POST":
        try:
            links = request.POST.getlist('links')
            content_title = get_details(links[0])[0]
            generated_content = GeneratedContent.objects.create(
                name=content_title
            )
            generated_content.save()
            print(generated_content.id)
            for link in links:
                title, author, length, description, pub_date = get_details(link)
                video_details = VideoDetail.objects.create(
                    generated_content=generated_content,
                    title=title,
                    author=author,
                    length=length,
                    description=description,
                    publish_date=pub_date,
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
        description = yt.description
        pub_date = yt.publish_date
        return title,author,length,description,pub_date
    else:
        return False