from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Post


def home(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        contenido = request.POST.get('contenido')

        # Guardar en la base de datos
        Post.objects.create(user=user, contenido=contenido)

        # Redireccionar para evitar reenviar el formulario al refrescar
        return redirect('home')

    # Si es GET, muestra todos los posts
    posts = Post.objects.all().order_by('-fecha')[:5]  # más recientes primero
    return render(request, 'blog/home.html', {'posts': posts})


def search_by_user(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        redirect_path = reverse('posts_by_user', args=[user])
        return HttpResponseRedirect(redirect_path)
    return render(request, 'blog/search_user.html')


def show_post_by_user(request, user):
    try:
        posts = Post.objects.filter(user__iexact=user).order_by('-fecha')
        return render(
            request, 'blog/posts_by_user.html',
            {
                'user': user,
                'posts': posts
            })
    except KeyError:
        return HttpResponseNotFound('{"ErrorMessage": "Invalid user"}')


def show_all_post(request):
    posts = Post.objects.all().order_by('-fecha')
    return render(request, 'blog/all_posts.html', {'posts': posts})


def delete_post_by_id(request):
    posts = Post.objects.all().order_by('-fecha')[:15]  # ultimos 15
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            post_data = {
                'usuario': post.user,
            }
            post.delete()
            return render(
                request, 'blog/delete_posts.html',
                {
                    'posts': posts,
                    'deleted': True,
                    'deleted_user': post_data['usuario']
                })

        except Post.DoesNotExist:
            return HttpResponseNotFound("El post NO existe. Intenta de nuevo.")
    # Si es GET, muestra todos los posts
    return render(request, 'blog/delete_posts.html', {'posts': posts})

# TODO: Editar post
