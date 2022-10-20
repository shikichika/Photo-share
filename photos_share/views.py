from unicodedata import name
from django.shortcuts import redirect, render

from .models import Category, Photo
from .forms import LoginGalleryForm
from users.models import Galleries

def gallery(request):

    #categoryごとに検索
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(
            gallery_id = Galleries.objects.get(pk = request.session['gallery_id']),
            category__name__icontains = category,
            )
    
    categories = Category.objects.filter()
    context = {
        'categories':categories,
        'photos' : photos
        }
    return render(request, 'photo_folder/gallery.html', context)



def photo_detail(request, pk):
    photo = Photo.objects.get(
        id=pk,
        gallery_id = Galleries.objects.get(pk = request.session['gallery_id']),
        )
    context = {
        'photo':photo,
        }
    return render(request, 'photo_folder/photo_detail.html', context)


def photo_add(request):
    categories = Category.objects.filter(gallery_id = request.session['gallery_id'])

    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] !='none':
            category = Category.objects.get(name=data['category'])
        elif data['category_new'] != '':
            category_new = Category.objects.create(name=data['category_new'])
            category = Category.objects.get(name=category_new)
            
        else:
            category = None
        
        photo = Photo.objects.create(
            gallery_id = request.session['gallery_id'],
            category=category,
            title = data['title'],
            description = data['discription'],
            image = image,
        )

        return redirect('gallery')

    context = {
        'categories': categories,
    }
    return render(request, 'photo_folder/photo_add.html', context)

def photo_update(request, pk):

    photo = Photo.objects.get(
        gallery_id = request.session['gallery_id'],
        id=pk
        )
    categories = Category.objects.all()
    print(pk)
    if request.method == 'POST':
        
        data = request.POST

        photo = Photo.objects.filter(id = pk)
        photo.update(category = Category.objects.get(name = data['category']), title = data['title'], description = data['description'])
        return redirect('gallery')

    context = {
        'photo':photo,
        'categories':categories,
    }

    return render(request, 'photo_folder/photo_update.html', context)

def photo_delete(request, pk):
    Photo.objects.filter(id=pk).delete()
    return redirect('gallery')



def categories_list(request):

    categories = Category.objects.filter(
        gallery_id = request.session['gallery_id']
    )

    context = {
        'categories':categories,
    }

    return render(request, 'photo_folder/categories_list.html', context)



def category_update(request, pk):

    category = Category.objects.get(id = pk)

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = Category.objects.filter(id = pk)
        category.update(name = category_name)

        return redirect('categories_list')

    context = {
        'category' : category,
    }

    return render(request, 'photo_folder/category_update.html', context)


def category_delete(request, pk):
    Category.objects.get(id=pk).delete()
    return redirect('categories_list')



def gallery_login(request):
    form = LoginGalleryForm()

    if request.method == "POST":
        form = LoginGalleryForm(request.POST)
        print("form" , form.is_valid(), form)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            
            gallery = Galleries.objects.filter(name= name, password=password)
            request.session['gallery_id'] = gallery[0].pk
            request.session['gallery_name'] = gallery[0].name

            return redirect('gallery')

    context = {
        'form': form
    }

    return render(request, 'photo_folder/login_gallery.html', context)
