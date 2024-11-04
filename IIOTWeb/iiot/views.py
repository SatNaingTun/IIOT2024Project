from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
    if request.method=='GET':
        return render(request,"iiot/test.html")
    elif request.method=='POST':
        
        messages.info(request,'You clicked the submit button')
        return redirect(test)

