from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

def gen_slug(s): #буду генерировать здесь SLUG из обычных строк
    new_slug = slugify(s, allow_unicode=True) 
    return new_slug + '-' + str(int(time())) #float->int->str
    #что касается уникальности slug (например подойдет указать время)?

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True) #для индексации
    slug = models.SlugField(max_length=150, unique=True, blank=True) #присваиваю уникальность
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts') #появится новое свойство у Tag
    date_pub = models.DateTimeField(auto_now_add=True) #при сохр. в бд сработает
    
    def get_absolute_url(self): #название метода - это соглашение Джанги
        return reverse('post_detail_url', kwargs={'slug': self.slug})
    
    def get_delete_url(self): #получение ссылки на удаление объекта
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})
    #reverse будет генерить нам ссылку
    #ОХУЕТЬ, Я ЭТО ПОНЯЛ
    #Значит в index.html мы перебираем циклом все наши новые посты, затем обращаемся к этом методу для каждого объекта
    #тут мы уже ВОЗВРАЩАЕМ СГЕНЕРИРОВАННУЮ ССЫЛКУ =>
    #вначале берем имя пути, куда затем в ИМЕНОВАННУЮ переменную мы подставляем объект полученный из цикла в Index
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): #параметры поля модели которые передаются в констр класса
        if not self.id: #если объект не был ранее сохранен (тобишь без id в бд) 
            self.slug = gen_slug(self.title)
        #после того как новый слаг для новый модели будет сгенерирован
        #Model - суперкласс
        super().save(*args, **kwargs)

    class Meta: #определяет внутреннее отношение
        ordering = ['-date_pub'] # минус для обратного порядка, начиная с новых


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    #'posts' появитлся для объектов класса Tag, для ссылки на Посты

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self): #генерирует ссылку на соот. вьюху для изменения объекта
        return reverse('tag_update_url', kwargs={'slug': self.slug})
    
    def get_delete_url(self): #получение ссылки на удаление объекта
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta: 
        ordering = ['title'] 