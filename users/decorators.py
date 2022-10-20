from django.shortcuts import redirect



def login_required_user(func):
    def login_check(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except:
            return redirect('user_login')
    return login_check

