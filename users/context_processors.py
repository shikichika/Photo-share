from django.http import HttpRequest
from django.shortcuts import redirect


def username_processor(request):

    try:
        username = request.session['username']



    except:
        username = ""
        
    return{
        'username' : username,
    }

