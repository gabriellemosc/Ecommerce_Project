from django.shortcuts import render

# Create your views here.

    #run the homepage view
def homepage(request):              
    return render(request, 'homepage.html')     #load the HTML file