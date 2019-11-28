from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView

import blog
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, CreateUserForm, CommentDelete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class IndexView(View):
    def get(self, request):
        return render(request, 'home/index.html')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            print(comment)
            comment.post = post
            print(post)
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            post_comment = request.POST.get('password_confirm')
            post_id = request.POST.get('author')
            comment = Comment.objects.filter(password=post_comment).filter(id=post_id).values_list(flat=True).distinct()
            if comment:
                clist = list(comment)
                print(clist[-1])
                if clist[-1] == int(post_id):
                    print('삭제')
                    return comment_remove(request, pk=post_id)
                else:
                    print('실패')
            else:
                print('비밀번호 틀림')
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/post_detail.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    # form_class = UserCreationForm
    form_class = CreateUserForm
    success_url = reverse_lazy('create_user_done')


class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'


# @login_required
# def post_like_toggle(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     user = request.user
#     print(user)
#
#     profile = Profile.objects.get(user=user)
#     print(profile)
#
#     check_like_post = profile.like_posts.filter(pk=post.pk)
#
#     if check_like_post.exists():
#         profile.like_posts.remove(post)
#         post.like_count -= 1
#         post.save()
#     else:
#         profile.like_posts.add(post)
#         post.like_count += 1
#         post.save()
#
#     return redirect('post_detail', pk=post.pk)


@login_required
def post_like_toggle(request, pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    filtered_like_posts = user.like_posts.filter(pk=post.pk)

    if filtered_like_posts.exists():
        user.like_posts.remove(post)
        post.like_count -= 1
        user.save()
        post.save()
    else:
        user.like_posts.add(post)
        post.like_count += 1
        user.save()
        post.save()

    if next_path:
        return redirect(next_path)
    return redirect('post_detail', pk=post.pk)