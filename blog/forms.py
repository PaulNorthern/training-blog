from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError

class TagForm(forms.ModelForm):
    class Meta: #связать Tag и нашу TagForm
        model = Tag
        fields = ['title', 'slug']

        widgets = {
        'title': forms.TextInput(attrs={'class':'form-control'}),
        'slug': forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean_slug(self): #clean_ - кастомный метод для поля slug, чтобы сделать возможность на проверку данных
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count(): #вернет список отличный от нуля
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug)) #если True т.е 1, то выдаст ошибку
        return new_slug

class PostForm(forms.ModelForm):
    class Meta:
        model = Post #модель с которой мы уже связываемся
        fields = ['title', 'slug', 'body', 'tags'] #поля модели, которые мне нужны

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}), 
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')       
        return new_slug
