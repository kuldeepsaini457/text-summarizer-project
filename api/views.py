from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from algorithm.finalalgo import Summarize

@api_view(['GET','POST'])
def get_summary(request,*args,**kwargs):
   
    title=request.data.get('title')
    article=request.data.get('article')
    lines=request.data.get('lines')

    if lines is not None:
        lines=int(lines)
    if article is None:
        return JsonResponse({"title":title,"article":article})

    summarizer=Summarize(title,article,lines)
    summary=summarizer.generate_summary()

    response={"title":title,"summary":summary.get('summary')}
    return Response(response)