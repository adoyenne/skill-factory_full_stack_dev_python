from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Response
from .forms import PostForm, ResponseForm
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone


@login_required
def post_list(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            post_pk = request.POST.get('post_pk')  # Извлекаем post_pk из POST запроса
            post = get_object_or_404(Post, pk=post_pk)
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
            return redirect('post_list')  # Перенаправляем обратно на список постов после отправки комментария
    else:
        form = ResponseForm()
    return render(request, 'board/post_list.html', {'posts': posts, 'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_list', pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form})



@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        print("Unauthorized attempt to delete post")  # отладочное сообщение
        return redirect('profile')
    if request.method == "POST":
        post.delete()
        print("Post deleted successfully")  # отладочное сообщение
        return redirect('profile')  # Редирект на профиль
    return render(request, 'board/post_delete_confirm.html', {'post': post})



@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.post = post
            response.save()

            # Отправка уведомления автору поста
            subject = 'Новый комментарий к вашему посту'
            message = render_to_string('board/email_notification.html', {'post': post, 'comment': response})
            to_email = post.author.email

            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            return redirect('post_list')  # Редирект на профиль
    else:
        form = ResponseForm()
    return render(request, 'board/add_comment.html', {'form': form})

@login_required
def edit_comment(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.author != request.user:
        return redirect('post_detail', pk=response.post.pk)
    if request.method == "POST":
        form = ResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Редирект на профиль
    else:
        form = ResponseForm(instance=response)
    return render(request, 'board/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.author != request.user:
        return redirect('post_detail', pk=response.post.pk)
    if request.method == "POST":
        response.delete()
        return redirect('post_list')  # Редирект на профиль
    return render(request, 'board/delete_comment.html', {'response': response})


@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    responses = Response.objects.filter(post__author=request.user)

    context = {
        'posts': posts,
        'responses': responses,
    }
    return render(request, 'board/profile.html', context)

@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.post.author != request.user:
        return redirect('profile')
    response.delete()
    return redirect('profile')



def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('post_list')  # Если пользователь аутентифицирован, перенаправляем на список постов
    else:
        return redirect('home')  # Иначе перенаправляем на вашу домашнюю страницу (если она существует)


@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.post.author != request.user:
        return redirect('profile')
    response.accepted = True
    response.save()

    # Отправка уведомления автору отклика
    subject = 'Ваш отклик принят'
    message = render_to_string('board/email_response_accepted.html', {'response': response})
    to_email = response.author.email
    email = EmailMessage(subject, message, to=[to_email])
    email.send()

    return redirect('profile')


@login_required
def manage_responses(request):
    posts = Post.objects.filter(author=request.user)
    selected_post = request.GET.get('post')
    if selected_post:
        responses = Response.objects.filter(post__pk=selected_post)
    else:
        responses = Response.objects.filter(post__in=posts)
    return render(request, 'board/manage_responses.html', {'responses': responses, 'posts': posts})

# Представление для подтверждения удаления отклика
@login_required
def delete_comment_confirm(request, pk):
    print("Delete comment confirm view called")  # Отладочное сообщение

    response = get_object_or_404(Response, pk=pk)

    if request.method == "POST":
        print("POST request received")  # Отладочное сообщение

        confirm = request.POST.get('confirm_delete')  # Проверяем, подтверждено ли удаление
        if confirm == 'yes':
            print("Confirmation received")  # Отладочное сообщение

            # Отправляем уведомление автору отклика
            subject = 'Ваш отклик был отклонен'
            message = render_to_string('board/email_response_rejected.html', {'response': response})
            send_mail(subject, message, 'your_email@example.com', [response.author.email])

            # Удаляем отклик
            response.delete()

            messages.success(request, 'Отклик был успешно отклонен и отправлено уведомление автору.')
            return redirect('profile')
        else:
            messages.info(request, 'Отклик не был отклонен.')
            return redirect('profile')

    return render(request, 'board/delete_comment_confirm.html', {'response': response})

# Представление для подтверждения удаления поста
@login_required
def post_delete_confirm(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('profile')
    return render(request, 'board/post_delete_confirm.html', {'post': post})