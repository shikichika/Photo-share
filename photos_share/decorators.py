from django.shortcuts import redirect



def login_required_gallery(func):
    def login_check(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except:
            return redirect('gallery_login')
    return login_check

