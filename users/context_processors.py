from django.http import HttpRequest
from django.shortcuts import redirect


def username_processor(request):

    try:
        username = request.session['username']
        return {
        'username' : username,
    }


    except:
        return redirect('user_login')
    
