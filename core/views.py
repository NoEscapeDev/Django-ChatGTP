from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#import user
from django.contrib.auth.models import User
import openai
from gtts import gTTS
import string
import random
import os
import shutil
import random
from django.http import FileResponse

openai.api_key='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'
# openai.api_key='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'
def writeblogs(topic,models,language,tones,formality,paragraphs,keywords,max_tokens):
    print(max_tokens)
    response = openai.Completion.create(
    model="{}".format(models),
    prompt="\"Generate a blog  about {}. The blog should be written in {} and should have a {} tone. It should be written in a {} style, and should have at least {} paragraphs and maximum 3000 words. Keywords to include: {}.\"\n".format(topic,language,tones,formality,paragraphs,keywords),
    temperature=0.3,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    ).choices[0].text
    return response


def rewriteblogs(topic,models,language,tones,formality,paragraphs):
  response = openai.Completion.create(
    model="{}".format(models),
    prompt="rewrite the following blog:{}\nlanguage:{}\nFormality:{}\nTones:{}\nNumber of Paragraph:{}\n".format(topic,language,formality,tones,paragraphs),
    temperature=0.3,
    max_tokens=2877,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    ).choices[0].text
  return response

def generateblogideas(topic,models,language,tones,formality,numbers,keywords):

    response = openai.Completion.create(
    model="{}".format(models),
    prompt="generate {} different blog ideas on the following topic:{}\nlanguage:{}\nkeywords:{}\nFormality:{}\nTones:{}\n\n".format(numbers,topic,language,keywords,formality,tones),
    temperature=0.3,
    max_tokens=2284,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    ).choices[0].text
    return response



def generateblogoutline(topic,models,language,tones,formality,paragraphs,keywords):
   response = openai.Completion.create(
    model="{}".format(models),
    prompt="generate outline on the following blog topic:{} \nnumber of paragraph:{}\nlanguage:{}\nkeywords:{}\nFormality:{}\nTones:{}".format(topic,paragraphs,language,keywords,formality,tones),
    temperature=0.3,
    max_tokens=2284,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    ).choices[0].text
   return response

def write(request):
    if request.method == 'POST':
        topic = request.POST['description']
        models= request.POST['models']
        language = request.POST['language']
        tones = request.POST['tones']
        formality = request.POST['formality']
        paragraphs = request.POST['paragraph']
        keywords = request.POST['keywords']
                
        if models == "text-davinci-003":
            max_tokens = 3000
            response = writeblogs(topic,models,language,tones,formality,paragraphs,keywords,max_tokens)
        elif models == "text-curie-001":
            max_tokens = 2022
            response = writeblogs(topic,models,language,tones,formality,paragraphs,keywords,max_tokens)
        elif models == "text-babbage-001":
            max_tokens = 1950
            response = writeblogs(topic,models,language,tones,formality,paragraphs,keywords,max_tokens)
        elif models == "text-ada-001":
            max_tokens = 1950
            response = writeblogs(topic,models,language,tones,formality,paragraphs,keywords,max_tokens)
        
        return render(request, 'write.html', {'response': response,'topic':topic,})
    else:
        return render(request, 'write.html')

def rewrite(request):
    if request.method == 'POST':
        topic = request.POST['description']
        models= request.POST['models']
        language = request.POST['language']
        tones = request.POST['tones']
        formality = request.POST['formality']
        paragraphs = request.POST['paragraph']
        response = rewriteblogs(topic,models,language,tones,formality,paragraphs)
        return render(request, 'rewrite.html', {'response': response})
    else:

    
     return render(request, 'rewrite.html')
def blogideas(request):
    if request.method == 'POST':
        topic = request.POST['description']
        models= request.POST['models']
        language = request.POST['language']
        tones = request.POST['tones']
        formality = request.POST['formality']
        numbers = request.POST['variant']
        keywords = request.POST['keywords']
        response = generateblogideas(topic,models,language,tones,formality,numbers,keywords)
        return render(request, 'blogideas.html', {'response': response})
    return render(request, 'blogideas.html')
    
def blogoutline(request):
    if request.method == 'POST':
        topic = request.POST['description']
        models = request.POST['models']
        language = request.POST['language']
        tones = request.POST['tones']
        formality = request.POST['formality']
        paragraphs = request.POST['paragraph']
        keywords = request.POST['keywords']
        response = generateblogoutline(topic,models,language,tones,formality,paragraphs,keywords)
        return render(request, 'blogoutline.html', {'response': response})
    else:

     return render(request, 'blogoutline.html')

def tools(request):
    
    audioFileName = request.session.get('audio-file-current-user')
    if audioFileName:
        path = "static/"+audioFileName
        file_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return render(request, 'projects.html')

def text(request):
    return render(request, 'text.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('tools')
    if request.method == 'POST':
        # The user has submitted the login form
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # The authentication was successful
            auth.login(request,user)
            return redirect('tools')
        else:
            # The authentication was unsuccessful
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        # The user has not submitted the login form yet
        return render(request, 'login.html')

# Download audio file
def Download(request):
    if request.method == "POST":
        text = request.POST['textarea']
        tdl = 'com'
        lang = 'en'
        if text:
            tts = gTTS(text, lang=lang, tld=tdl)

            random_number = random.randint(0,5000)
            extension = 'mp3'
            file_name = str(random_number) + "." + extension
            tts.save(file_name)

            request.session['audio-file-current-user'] = file_name        

            dir = os.getcwd()
            full_dir = os.path.join(dir, file_name)

            dest = shutil.move(full_dir, os.path.join(dir, "static/audios"))

            data = {"loc" : file_name}
            return render(request,'blogideas.html',data)
        return redirect('blogideas')
    
    return redirect('blogideas')

def logout(request):
    auth.logout(request)
    return redirect('login')

from django.http import HttpResponse
def Download(request):
    if request.method == "POST":
        text = request.POST['textarea']
        if text:
            language = request.GET.get('language', 'en')
            tts = gTTS(text=text, lang=language)
            response = HttpResponse(content_type="audio/mp3")
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
            tts.write_to_fp(response)
            return response
        
    
