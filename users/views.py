from django.shortcuts import redirect, render
from django.contrib import messages


from .models import Galleries, Owner
from .forms import RegisterForm, LoginForm
from .decorators import login_required_user
from .utils import make_hash

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
            messages.error(request, 'Name must be alphabet or number')
            return redirect('gallery_create')
        elif len(data['password']) < 6 or len(data['password']) >13:
            messages.error(request, 'Password must be more than 6 and less than 13')
            return redirect('gallery_create')
        elif not data['password'].isalnum():
            messages.error(request, 'Password must alphabet or number')
            return redirect('gallery_create')
        elif is_created:
            messages.error(request, 'The gallery name can\'t be use')
            return redirect('gallery_create')

        

        Galleries.objects.create(
            user = Owner.objects.get(pk=request.session['id']),
            name = data['name'], 
            slug = slug, 
            password = data['password'], 
            description = data['description']
            )

        return redirect('user_home')

    return render(request, 'user/gallery_create.html')



@login_required_user
def gallery_update(request, slug):

    gallery = Galleries.objects.get(slug = slug)


    if request.method == 'POST':
        data = request.POST

        slug = data['name'].lower().strip()

        is_created = Galleries.objects.filter(slug=slug).exists()

        if not data['name'].isalnum():
            messages.error(request, 'Name must be alphabet or number')
            return redirect('gallery_create')
        elif len(data['password']) < 6 or len(data['password']) >13:
            messages.error(request, 'Password must be more than 6 and less than 13')
            return redirect('gallery_create')
        elif not data['password'].isalnum():
            messages.error(request, 'Password must alphabet or number')
            return redirect('gallery_create')
        elif is_created:
            messages.error(request, 'The gallery name can\'t be use')
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


@login_required_user
def gallery_into(request, slug):

    gallery = Galleries.objects.filter(slug = slug)

    request.session['gallery_id'] = gallery[0].pk
    request.session['gallery_name'] = gallery[0].name

    return redirect('gallery')


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            hash_password = make_hash(email, password)

            owner = Owner.objects.create(
                username = username,
                email= email,
                password = hash_password,
            )

            owner.save()
            return redirect('user_login')
  
    context = {
        'form': form,
    }


    return render(request, 'user/register.html', context)


def user_login(request):

    try:
        username = request.session['username']
        id = request.session['id']

        return redirect('user_home')
    
    except:
        form = LoginForm()

        if request.method == "POST":
            form = LoginForm(request.POST)
            
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                hash_password = make_hash(email, password)

                try:       
                    user = Owner.objects.filter(email = email, password=hash_password)
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
    del request.session['username']
    del request.session['id']

    return redirect('home')

@login_required_user
def user_detail(request):

    return render(request, 'user/user_detail.html')

@login_required_user
def user_update(request):

    email = Owner.objects.filter(
        id = request.session['id']
    )[0].email

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Password not match')
            return redirect('user_update')

        if new_password.isalnum() == False:
            messages.error(request, 'Password must be alphabet or number')
            return redirect('user_update')
        
        if len(new_password) < 6 or len(new_password) > 14:
            messages.error(request, 'Password must be more than 6 and less than 13')
            return redirect('user_update')

        hash_password = make_hash(email, new_password)
        Owner.objects.filter(id = request.session['id']).update(password=hash_password)

        return redirect('user_home')


    context = {
        'email':email
    }

    return render(request, 'user/user_update.html', context)

@login_required_user
def user_update_username(request):
    if request.method == 'POST':
        new_username = request.POST['new_username']

        if new_username.isalnum() == False:
            messages.error(request, 'Name must be alphabet or number')
            return redirect('user_update_username')

        if len(new_username) < 3 or len(new_username) > 40:
            messages.error(request, 'Password must be more than 3 and less than 40')
            return redirect('user_update_username')
        
        try:
            Owner.objects.filter(pk = request.session['id']).update(password=new_username)
            request.session['username'] = new_username
        except:
            return redirect('user_update_username')

        return redirect('user_home')
    
    email = Owner.objects.filter(
        id = request.session['id']
    )[0].email

    context = {
        'email':email
    }

    return render(request, 'user/user_username.html', context)

@login_required_user
def user_delete_form(request):

    return render(request, 'user/user_delete.html')

@login_required_user
def user_delete(request):

    Owner.objects.filter(id=request.session['id']).delete()

    return redirect('home')

