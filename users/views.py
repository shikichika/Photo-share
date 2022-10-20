from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Galleries, Owner
from .forms import RegisterForm, LoginForm
from .decorators import login_required_user

@login_required_user
def user_home(request):

    galleries = Galleries.objects.filter(
        user = Owner.objects.get(pk=request.session['id'])
    )

    context = {
        'galleries':galleries,
    }
    return render(request, 'user/user_home.html', context)


@login_required_user
def gallery_detail(request, slug):

    gallery = Galleries.objects.get(
        user = Owner.objects.get(pk=request.session['id']), 
        slug = slug)

    context = {
        'gallery':gallery,
    }
    return render(request, 'user/gallery_detail.html', context)


@login_required_user
def gallery_create(request):

    if request.method == 'POST':
        data = request.POST
        slug = data['name'].lower()

        is_created = Galleries.objects.filter(slug=slug).exists()

        if not data['name'].isalnum():
            return redirect('gallery_create')
        elif len(data['password']) < 6 or len(data['password']) >13:
            return redirect('gallery_create')
        elif not data['password'].isalnum():
            return redirect('gallery_create')
        elif is_created:
            return redirect('gallery_create')

        Galleries.objects.create(
            user = Owner.objects.get( pk=request.session['id']),
            name = data['name'], 
            slug = slug, 
            password = data['password'], 
            description = data['description']
            )

        return redirect('user_home')

    return render(request, 'user/gallery_create.html')




def gallery_update(request, slug):

    gallery = Galleries.objects.get(slug = slug)


    if request.method == 'POST':
        data = request.POST

        slug = data['name'].lower().strip()

        if not data['name'].isalnum():
            return redirect('gallery_create')
        elif len(data['password']) < 6 or len(data['password']) >13:
            return redirect('gallery_create')
        elif not data['password'].isalnum():
            return redirect('gallery_create')
        
        Galleries.objects.filter(slug=slug).update(name = data['name'], slug = slug, password = data['password'], description = data['description'])

        return redirect('user_home')

    context = {
        'gallery':gallery,
    }
    
    return render(request, 'user/gallery_update.html', context)




@login_required_user
def gallery_delete(request, slug):

    Galleries.objects.get(slug = slug).delete()

    return redirect('user_home')


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            owner = Owner.objects.create(
                username = username,
                email= email,
                password = password,
            )

            owner.save()
            return redirect('user_login')
  
    context = {
        'form': form,
    }


    return render(request, 'user/register.html', context)


def user_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:       
                user = Owner.objects.filter(email = email, password=password)
                request.session['username'] = user[0].username
                request.session['id'] = user[0].pk
                
                return redirect('user_home')

            except:
                messages.error(request, 'Invalid login')
                return redirect('user_login')

    context = {
        'form':form
    }
    return render(request, 'user/user_login.html', context=context)

def user_logout(request):
    request.session.clear()
    return redirect('user_login')
    