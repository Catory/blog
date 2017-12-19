import re

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from App.models import User,Posts

# Create your views here.
def index(request):
    posts = Posts.objects.filter(rid=0)
    context = {'title':'index','posts':posts}
    return render(request,'index.html',context)

def register(request):
    context = {'title':'注册'}
    return render(request,'register.html',context)

def do_register(request):
    if request.method == 'POST':
        u = User()
        u.username = request.POST.get('username')
        u.email = request.POST.get('email')
        u.password = request.POST.get('password')
        if request.POST.get('password') == request.POST.get('cpassword'):
            u.save()
            request.session['user'] = u.username
            request.session.set_expiry(600)
            return render(request,'registr_jump.html')


def login(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            u = User.objects.filter(username=username)[0]
            if u.check_password(password):
                request.session['user'] = u.username
                request.session.set_expiry(600)
                print('***********',request.session.get('user'))
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return HttpResponse('密码输入错误，请重新输入')
    context = {'title':'登录'}
    return render(request,'login.html',context)

def logout(request):
    del request.session['user']
    return HttpResponseRedirect(reverse('blog:index'))


def sendposts(request):
    if request.method == 'POST':
        username = request.session.get('user')
        u = User.objects.filter(username=username)[0]
        post = Posts()
        post.ptitle = request.POST.get('title')
        post.pcontent = request.POST.get('content')
        post.puser = u
        post.save()
        return HttpResponseRedirect(reverse('blog:index'))
    return render(request,'sendposts.html',context={'title':'登录'})


def detail(request,id):
    p = Posts.objects.filter(id=id)[0]
    context = {'title': p.ptitle, 'post': p}
    if Posts.objects.filter(rid=p.id):
        reposts = Posts.objects.filter(rid=p.id)
        context['reposts'] = reposts
    return render(request,'detail.html',context)


def cposts(request,id):
    if request.method == 'POST':
        p = Posts.objects.filter(id=id)[0]
        u = User.objects.filter(username=request.session.get('user'))[0]
        cpost = Posts()
        cpost.puser = u
        cpost.pcontent = request.POST.get('content')
        cpost.rid = p.id
        cpost.save()
        return HttpResponseRedirect(reverse('blog:detail',args=[p.id]))


def search(request):
    title = request.POST.get('search')
    print(title)
    if Posts.objects.filter(ptitle=title):
        p = Posts.objects.filter(ptitle=title)[0]
        return render(request,'search.html',context={'post':p})
    else:
        return HttpResponse('查找内容不存在')

@csrf_exempt
def register_handler(request):
    username = request.POST.get('username')
    if len(username) > 20 or not username:
        context = {'result':'username_not_standard'}
        return JsonResponse(context)
    elif User.objects.filter(username=username).exists():
        context = {'result': 'username_already_existed'}
        return JsonResponse(context)
    else:
        password = request.POST.get('password')
        if len(password) >= 8 and re.findall(r'\D+',password):
            if request.POST.get('password') == request.POST.get('cpassword'):

                context = {'result': 'success'}
                return JsonResponse(context)
            else:
                context = {'result': 'password_not_same'}
                return JsonResponse(context)

        else:
            context = {'result':'password_not_standard'}
            return JsonResponse(context)

@csrf_exempt
def login_handler(request):
    username = request.POST.get('username')
    print(username,'1111111111')
    password = request.POST.get('password')
    print(password,'22222222')
    if User.objects.filter(username=username).exists():

        if User.objects.filter(username=username)[0].check_password(password):
            context = {'status':'success'}
            return JsonResponse(context)
        else:
            context = {'status': 'pwdFalse'}
            return JsonResponse(context)
    else:
        context = {'status': 'usernameFalse'}
        return JsonResponse(context)