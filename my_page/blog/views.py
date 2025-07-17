from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseBadRequest
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
    redirect_html = 'blog/search_user.html'
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.POST.get('user')  # obtenemos el usuario que mandan desde el HTML # noqa

        if action == 'search':
            posts = Post.objects.filter(user__iexact=user).order_by('-fecha')

            if not posts.exists():
                return render(
                    request, redirect_html,
                    {
                        'users': get_users(),
                        'show_posts': False,
                        'user': user,
                        'user_not_found': True
                    })

            return render(
                request, redirect_html,
                {
                    'user': user,
                    'posts': posts,
                    'show_posts': True
                })

    return render(
        request, redirect_html,
        {
            'users': get_users(),
            'show_posts': False
        })


def get_users():
    users = Post.objects.values_list('user', flat=True).distinct()
    users_list = []
    distinct = set()
    for user in users:
        lower_user = user.lower()
        if lower_user not in distinct:
            distinct.add(lower_user)
            users_list.append(user)
    return sorted(users_list)


def show_all_post(request):
    posts = Post.objects.all().order_by('-fecha')
    return render(request, 'blog/all_posts.html', {'posts': posts})


def delete_post_by_id(request):
    posts = Post.objects.all().order_by('-fecha')[:10]  # ultimos 10
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

        except (Post.DoesNotExist, ValueError):
            return HttpResponseNotFound("El post NO existe. Intenta de nuevo.")
    # Si es GET, muestra todos los posts
    return render(request, 'blog/delete_posts.html', {'posts': posts})


# TODO: Editar post
def update_post_by_id(request):
    redirect_html = 'blog/update_posts.html'
    posts = get_posts(total_posts=10)  # ultimos 10
    if request.method == 'POST':
        try:
            post_id = request.POST.get('post_id')
            new_comment = request.POST.get('new_comment')

            if len(new_comment) == 0:
                return render(
                    request, redirect_html,
                    {
                        'modified': False,
                        'posts': posts
                    }
                )

            post = Post.objects.get(id=post_id)
            post_data = {
                'user': post.user,
                'previous_comment': post.contenido
            }

            post.contenido = new_comment  # actualizar post ???
            post.save()
            # TODO: Actualizar fehcha
            return render(
                request, redirect_html,
                {
                    'modified': True,
                    'posts': posts,
                    'user': post_data['user'],
                    'previous_comment': post_data['previous_comment']
                }
            )
        except (Post.DoesNotExist, ValueError):
            return HttpResponseNotFound("El post NO existe. Intenta de nuevo.")

    return render(
                    request, redirect_html,
                    {
                        'modified': False,
                        'posts': posts
                    }
                )


def get_posts(all_posts=False, total_posts=0):
    """total_posts should be greater than Zero"""
    if all_posts:
        return Post.objects.all().order_by('-fecha')

    if total_posts < 0:
        return HttpResponseBadRequest("total_posts should be greater than Zero")  # noqa

    return Post.objects.all().order_by('-fecha')[:total_posts]
