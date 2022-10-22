from django.shortcuts import redirect, render
from django.contrib import messages


from .models import Category, Photo
from users.models import Galleries
from .decorators import login_required_gallery
from .utils import judge_images

@login_required_gallery
def gallery(request):

    #categoryごとに検索
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(
            gallery_id = Galleries.objects.get(pk = request.session['gallery_id']),
            )
    else:
        photos = Photo.objects.filter(
            gallery_id = Galleries.objects.get(pk = request.session['gallery_id']),
            category__name__icontains = category,
            )
    
    categories = Category.objects.filter(gallery_id = Galleries.objects.get(pk = request.session['gallery_id']))
    context = {
        'categories':categories,
        'photos' : photos
        }
    return render(request, 'photo_folder/gallery.html', context)


@login_required_gallery
def photo_detail(request, pk):
    photo = Photo.objects.get(
        id=pk,
        gallery_id = Galleries.objects.get(pk = request.session['gallery_id']),
        )
    context = {
        'photo':photo,
        }
    return render(request, 'photo_folder/photo_detail.html', context)

@login_required_gallery
def photo_add(request):
    categories = Category.objects.filter(gallery_id = request.session['gallery_id'])

    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] !='none':
            category = Category.objects.get(
                gallery_id = Galleries.objects.get(id = request.session['gallery_id']),
                name=data['category']
                )
        elif data['category_new'] != '':

            if Category.objects.filter(gallery_id = Galleries.objects.get(id = request.session['gallery_id']),name=data['category']).exists() == False:
                category_new = Category.objects.create(
                    gallery_id = Galleries.objects.get(id = request.session['gallery_id']),
                    name=data['category_new']
                    )
                category = Category.objects.get(
                    gallery_id = Galleries.objects.get(id = request.session['gallery_id']),
                    name=category_new
                    )
            else:

                messages.error(request, 'The category already exists')
                return redirect('photo_add')
            
        else:
            category = None

        if judge_images(image) == False:
            messages.error(request, 'Your photo is prohibited')
            return redirect('photo_add')
        
        Photo.objects.create(
            gallery_id = Galleries.objects.get(id = request.session['gallery_id']),
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


@login_required_gallery
def photo_update(request, pk):

    photo = Photo.objects.get(
        gallery_id = request.session['gallery_id'],
        id=pk
        )
    categories = Category.objects.all()
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

@login_required_gallery
def photo_delete(request, pk):
    Photo.objects.filter(id=pk).delete()
    return redirect('gallery')


@login_required_gallery
def categories_list(request):

    categories = Category.objects.filter(
        gallery_id = request.session['gallery_id']
    )

    context = {
        'categories':categories,
    }

    return render(request, 'photo_folder/categories_list.html', context)



@login_required_gallery
def category_update(request, pk):

    category = Category.objects.get(id = pk)

    if request.method == 'POST':
        category_name = request.POST.get('category')

        if Category.objects.filter(name=category_name).exists() == True:
            messages.error(request, 'The category already exists')
            return redirect('category_update')

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


@login_required_gallery
def gallery_login(request):

    try:
        galley_id = request.session['gallery_id'] 
        gallery_name = request.session['gallery_name']

        return redirect('gallery')

    except:

        if request.method == 'POST':
            name = request.POST.get('name')
            password = request.POST.get('password')

            is_existed = Galleries.objects.filter(name=name, password=password).exists()

            if is_existed:
                gallery = Galleries.objects.filter(name=name, password=password)

                request.session['gallery_id'] = gallery[0].pk
                request.session['gallery_name'] = gallery[0].name

                return redirect('gallery')

            messages.error(request, 'Invalid login')

        return render(request, 'photo_folder/login_gallery.html')


@login_required_gallery
def gallery_logout(request):
    
    del request.session['gallery_id']
    del request.session['gallery_name'] 

    return redirect('home')
