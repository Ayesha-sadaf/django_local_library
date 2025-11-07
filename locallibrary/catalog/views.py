from django.shortcuts import render
def index(request):
    return render(request, 'This is catalog index page.')

