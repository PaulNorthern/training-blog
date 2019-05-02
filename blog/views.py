from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .utils import *
from .forms import TagForm, PostForm # тут формы для добавления данных 

from django.contrib.auth.mixins import LoginRequiredMixin #этот модуль надо подмешать в те объекты
# к которым хочу ограничить доступ
from django.core.paginator import Paginator 

from django.db.models import Q #для множественного поиска, в конструктор класса передавая искомые параметры

#http://127.0.0.1:8000/blog/?page=1

def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query: #если юзер ничего не ввел, то будет пустая строка
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query)) #поиск по заголовкам и телам
    else: #если search_query будет пустым, тогда получаем полный список
        posts = Post.objects.all()

    paginator = Paginator(posts, 2) # делим посты по две штуки на страницу

    page_number = request.GET.get('page', 1) #считываю данные из адресной строки; считывает переданный ключ page, а 1 - это дефолтное значение
    page = paginator.get_page(page_number) #у каждой страницы будет по два поста и свой URL номер ?page=1,2,3

    is_paginated = page.has_other_pages() #есть другие посты, если нет, то убираем панельку
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
         next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog/index.html', context=context)
    #object_list возвращает QuerySet

class PostDetail(ObjectDetailMixin, View): 
    model = Post
    template = 'blog/post_detail.html'
    # def get(self, request, slug): #get запросы
    #     #post = Post.objects.get(slug__iexact=slug)
    #     post = get_object_or_404(Post, slug__iexact=slug) #передаю класс и логику
    #     return render(request, 'blog/post_detail.html', context={'post':post})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'
    # def get(self, request, slug):
    #     tag = get_object_or_404(Tag, slug__iexact=slug)
    #     return render(request, 'blog/tag_detail.html', context={'tag':tag})

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm # не вызываю конструкто поэтому без скобок
    template = 'blog/tag_create.html'
    raise_exception = True
    # def get(self, request):
    #     form = TagForm()
    #     return render(request, 'blog/tag_create.html', context={'form': form})

    # def post(self, request):
    #     bound_form = TagForm(request.POST) #получили связанную форму, передава данные в словарь
    #     if bound_form.is_valid():
    #         new_tag = bound_form.save() #если True, получив новый объект 
    #         return redirect(new_tag) #Передавая объект; в качестве URL-а для перенаправления будет использоваться результат вызова метода get_absolute_url():
    #     return render(request, 'blog/tag_create.html', context={'form':bound_form}) #если форма не валидна

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True
    # def get(self, request): #этот метод (чтение) используем для первичного заполнения пустых форм на веб-странице
    #     form = PostForm() #создаем объект формы
    #     return render(request, 'blog/post_create_form.html', context={'form': form})

    # def post(self, request):
    #     bound_form = PostForm(request.POST) 
    #     if bound_form.is_valid():
    #         new_post = bound_form.save() 
    #         return redirect(new_post) 
    #     return render(request, 'blog/post_create_form.html', context={'form': bound_form})

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag 
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post 
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True
        
class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post 
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag 
    model_form = TagForm 
    template = 'blog/tag_update_form.html'
    raise_exception = True

    # надо получить конкертный объект
    # def get(self, request, slug): #идентиф. признак - slug
    #     tag = Tag.objects.get(slug__iexact=slug) #поулчили объект нечусвст. к регистру
    #     bound_form = TagForm(instance=tag) #создаю связанную форму и хочу подставить свойства этого тега из бд
    #     return render(request, 'blog/tag_update_form.html', context={'form': bound_form, 'tag':tag})

    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug) 
    #     bound_form = TagForm(request.POST, instance=tag)

    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         return redirect(new_tag)
    #     return render(request, 'blog/tag_update_form.html', context={'form': bound_form, 'tag':tag})





