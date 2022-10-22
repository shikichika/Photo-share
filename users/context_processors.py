
def username_processor(request):

    try:
        username = request.session['username']



    except:
        username = ""
        
    return{
        'username' : username,
    }

