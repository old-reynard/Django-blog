from urllib.parse import quote_plus

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def posts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Done!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request, "Not done!")
    context = {"form" : form}
    return render(request, "post_form.html", context)


def posts_detail(request, id): # retrieve
    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title" : instance.title,
        "post" : instance,
        "share_string" : share_string,
    }
    return render(request, "post_detail.html", context)


def posts_list(request): # list items
    queryset_list = Post.objects.active()
    paginator = Paginator(queryset_list, 5)

    page_var = 'page'
    page = request.GET.get(page_var)
    queryset = paginator.get_page(page)
    context = {
        "object_list" : queryset,
        "title" : "At old Reynard's",
        "page_var" : page_var,
    }
    
    return render(request, "post_list.html", context)


def posts_update(request, id=id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Done!")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title" : instance.title,
        "post" : instance,
        "form" : form,
    }

    return render(request, "post_form.html", context)


def posts_delete(request, id=id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Deleted!")
    return redirect('list')
