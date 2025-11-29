from django.shortcuts import render
from django.http import HttpResponse

def see_videos(request):
    return HttpResponse("seeing available videos")

def see_video_info(request):
    return HttpResponse("seeing details")

def index(request):
    text = "<a href='see/'>videos</a>  <a href='info/'>See video info</a>"

    return HttpResponse(text)