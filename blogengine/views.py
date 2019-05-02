from django.http import HttpResponse
from django.shortcuts import redirect 

def redirect_blog(request):
    return redirect('posts_list_url', permanent=True) #имя url по которому будет производиться redirect
    #redirect может быть постоянным и временным 302-ым 