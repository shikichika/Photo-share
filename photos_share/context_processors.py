
def gallery_name_processor(request):

    try:
        gallery_name = request.session['gallery_name']



    except:
        gallery_name = ""
        
    return{
        'gallery_name' : gallery_name,
    }

