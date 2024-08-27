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
from groq import Groq
from dotenv import load_dotenv
from openai import OpenAI
from django.http import HttpResponse,StreamingHttpResponse
from .models import VideoDetail
import markdown2
from io import BytesIO
from xhtml2pdf import pisa
from bs4 import BeautifulSoup

load_dotenv()
groq_api = os.getenv('GROQ_API_KEY')
openai_api = os.getenv('OPENAI_API_KEY')

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
            for link in links:
                title, author, length, pub_date = get_details(link)
                transcript = get_transcription(link)
                print(transcript)
                summary = generate_summary(transcript)
                print(summary)
                blog = generate_blog(transcript)
                print(blog)
                video_details = VideoDetail.objects.create(
                    generated_content=generated_content,
                    title=title,
                    author=author,
                    length=length,
                    publish_date=pub_date,
                    youtube_link = link,
                    transcript = transcript,
                    summary = summary,
                    blog = blog,
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

# get transcript
def get_transcription(link):
    client = Groq()
    filename = download_audio(link)
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="distil-whisper-large-v3-en",
        response_format="text",
        temperature=0.0,
        )
    return transcription

# Generate summary 
def generate_summary(transcription):
    client = OpenAI(api_key=openai_api)
    prompt1 = f"""You are tasked with expertly summarizing a transcript from a YouTube video or podcast. Your goal is to create a comprehensive summary that captures all the key points, allowing a reader to understand the content well enough to hold an intellectual conversation about it with the original author.
 
    Here is the transcript you will be summarizing:
    
    <transcript>
    {transcription}
    </transcript>
    
    Please follow these steps to create your summary:
    
    1. Carefully read through the entire transcript, paying close attention to the main topics, arguments, and ideas presented.
    
    2. Identify the key points, ensuring you capture:
    - Main themes and topics
    - Important arguments or claims
    - Supporting evidence or examples
    - Any significant conclusions or insights
    
    3. As you analyze the content, consider:
    - The overall structure and flow of the discussion
    - Any recurring themes or ideas
    - Unique perspectives or novel information presented
    - Potential counterarguments or limitations addressed
    
    4. Create a concise yet comprehensive summary that:
    - Covers all major points without unnecessary detail
    - Maintains the logical flow and structure of the original content
    - Accurately represents the author's views and arguments
    - Includes any crucial context or background information
    
    5. Ensure your summary would enable the reader to:
    - Understand the main arguments and their supporting evidence
    - Grasp the significance of the topic and its implications
    - Identify potential areas for further discussion or debate
    - Formulate intelligent questions or responses related to the content
    
    6. Structure your summary in a clear and organized manner, using:
    - Short paragraphs for each main point or theme
    - Bullet points for lists of related ideas or examples, if appropriate
    - Transitional phrases to maintain coherence between sections
    
    7. Throughout your summary, focus on providing information that would prepare the reader for an intellectual conversation. Include:
    - Key terminology or concepts introduced in the transcript
    - Notable quotes or statements, if particularly impactful
    - Any controversies or debates mentioned within the topic
    
    8. After completing your summary, review it to ensure it accurately represents the original content without bias or misinterpretation.
    
    Please provide your expert summary. Aim for a length that balances comprehensiveness with conciseness, typically between 300-500 words, but adjust as necessary based on the complexity and length of the original transcript."""
    
    summary = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt1}
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"}
    )
    generated_summary = summary.choices[0].message.content.strip()
    return generated_summary

# Generate blog

def generate_blog(transcription):
        client = OpenAI(api_key=openai_api)
        prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article. Make it look like a proper blog article and not like a YouTube video transcript:\n\n{transcription}\n\nArticle:"
        response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"}
        )
        generated_blog = response.choices[0].message.content.strip()
        return generated_blog

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


def download_chat_pdf(request,video_id):
    video = VideoDetail.objects.get(id=video_id)
    title = video.title
    summary = video.summary
    transcript = video.transcript
    blog = video.blog

    # Data to be included in the PDF
    story = ""
    story = f"<h1 align='center' style=\"font-size:30px\" >{title}</h1>" + '\n\n\n\n' + "<h2 style=\"font-size:18px\"><u>Transcript</u></h2>" + '\n\n' + transcript + '\n\n\n' + "<h2 style=\"font-size:18px\"><u>Summary</u></h2>" + '\n\n' + summary + '\n\n\n' + "<h2 style=\"font-size:18px\"><u>Blog Article</u></h2>" + '\n\n' + blog + '\n\n\n\n'

    # Markdown to HTML
    html_text = markdown2.markdown(story)

    # Create a BytesIO buffer to hold the PDF
    buffer = BytesIO()

    # Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html_text, dest=buffer)

    # Get PDF data from buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HTTP response with PDF mime type
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}_Chat.pdf"'

    return response

def generate_audio(request,video_id):
    client = OpenAI(api_key=openai_api)
    video = VideoDetail.objects.get(id=video_id)
    title = video.title
    summary = video.summary
    audio_file_path = f"{settings.MEDIA_ROOT}/summary_audio/{title}.mp3"
    if os.path.exists(audio_file_path):
        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(file_iterator(audio_file_path), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
        return response
    else:
        # openai tts conversion
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="alloy",
            input=summary
        )
        response.stream_to_file(audio_file_path)
        print("Audio saved!",audio_file_path)

        if os.path.exists(audio_file_path):
            def file_iterator(file_path, chunk_size=8192):
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk

            response = StreamingHttpResponse(file_iterator(audio_file_path), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
            return response
        else:
            return HttpResponse("Audio file not found", status=404)