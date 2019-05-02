from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import *

#self т.к для разных объектов нашего класса будут разные значения переменных

class ObjectDetailMixin: #класс для переопределения
    model = None
    template = None

    def get(self, request, slug): 
        obj = get_object_or_404(self.model, slug__iexact=slug) #принимает объект модели с полем slug, если нет то ошибка 404
        #НАПРИМЕР: передаю на шаблон 'blog/post_detail.html' ключ Post, который делаю с маленькой буквы
        return render(request, self.template, context={self.model.__name__.lower():obj, 'admin_object':obj, 'detail':True}) # передаю сюда инфу post_detail.html для отображения title и body
        #'detail' c True передаем на конкретную страницу, где затем отображаем кнопки Edit и Delete

class ObjectCreateMixin:
    model_form = None 
    template = None

    def get(self, request):
        form = self.model_form() #вызваем конструктор нашего класса form_model
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model_form(request.POST) #получили связанную форму, передава данные в словарь
        if bound_form.is_valid():
            new_obj = bound_form.save() #если True, получив новый объект 
            return redirect(new_obj) #Передавая объект; в качестве URL-а для перенаправления будет использоваться результат вызова метода get_absolute_url():
        return render(request, template, context={'form':bound_form}) #если форма не валидна

class ObjectUpdateMixin:
    model = None 
    model_form = None 
    template = None

    # надо получить конкертный объект
    def get(self, request, slug): #идентифицируем по - slug
        obj = self.model.objects.get(slug__iexact=slug) #поулчили объект нечусвст. к регистру
        bound_form = self.model_form(instance=obj) #создаю связанную форму и хочу подставить свойства этого тега из бд
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower() : obj})
        #instance передает выбранный объект из базы данных в контруктор класса model_form
    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug) 
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower() : obj})

class ObjectDeleteMixin:
    model = None 
    template = None 
    redirect_url = None 

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower():obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))