import re
import math

from redis import Redis
import logging
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from App.models import User,Posts
from App.help import getip,page_cache
from App.email import send_mail
logger = logging.getLogger('inf')
redis = Redis()

def index(request,page=1):
    '''pagination'''
    pages = math.ceil(Posts.objects.filter(rid=0).count()/4)
    print(pages)
    page = int(page)
    start_post = (page-1)*4
    end_post = (page)*4
    posts = Posts.objects.filter(rid=0)[start_post:end_post]

    comment_counts = [(post,Posts.objects.filter(rid=post.id).count()) for post in posts]
    '''top_five'''
    top_ten = redis.zrevrange('posts',0,4,withscores=True)
    top_ten_id = [ench[0].decode('utf-8') for ench in top_ten]
    post_ten = {post.id:post for post in Posts.objects.filter(id__in=top_ten_id)}
    post_ten = [(post_ten[int(id)],int(count))for id,count in top_ten]
    '''hot post'''
    for post in Posts.objects.filter(rid=0):
        redis.zadd('com_counts',post.id,Posts.objects.filter(rid=post.id).count())
    com_five = redis.zrevrange('com_counts',0,4,withscores=True)
    com_five_id = [ench[0].decode('utf-8') for ench in com_five]
    post_five = {post.id:post for post in Posts.objects.filter(id__in=com_five_id)}
    post_five = [(post_five[int(id)],int(count)) for id,count in com_five]

    online_user_count = redis.get('online_user')
    context = {'title': 'index', 'posts': posts,'comment_counts':comment_counts, 'pages': range(pages),'rank':post_ten,'post_five':post_five,'onlineuser':online_user_count}
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
            redis.incr('online_user')
            token = u.generate_activate_token()
            url = 'http://10.0.129.114:8000/blog/useractivate/?token=%s'%token
            message = '<h3>你好,%s</h3><a href=%s>点我激活</a>'%(u.username,url)
            print('-------------------',message)
            send_mail(u.email,message,token=token)
            return HttpResponse('你好，激活邮件已经发送至你的 邮箱，快去激活吧')

def user_activate(request,token):
    print('--------------------',token)
    if User.check_activate_token(token):
        return render(request, 'registr_jump.html')
    else:
        return HttpResponse('激活失败，链接已经失效，请重新注册')
def login(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            u = User.objects.filter(username=username)[0]
            if u.check_password(password):
                request.session['user'] = u.username
                request.session.set_expiry(600)
                redis.incr('online_user')
                return HttpResponseRedirect(reverse('blog:index',args=[1]))
            else:
                return HttpResponse('密码输入错误，请重新输入')
    context = {'title':'登录'}
    return render(request,'login.html',context)

def logout(request):
    redis.decr('online_user')
    del request.session['user']
    return HttpResponseRedirect(reverse('blog:index',args=[1]))


def sendposts(request):
    if request.method == 'POST':
        username = request.session.get('user')
        u = User.objects.filter(username=username)[0]
        post = Posts()
        post.ptitle = request.POST.get('title')
        post.pcontent = request.POST.get('content')
        post.puser = u
        post.save()
        return HttpResponseRedirect(reverse('blog:index',args=[1]))
    return render(request,'sendposts.html',context={'title':'登录'})

# def getip(func):
#     def wrap(request,*args):
#
#         ip = request.META['REMOTE_ADDR']
#         logger.info('{ip}  {}'.format(ip=ip,*args))
#         return func(request,*args)
#     return wrap
#
# def page_cache(timeout):
#     def article_cache(func):
#         def wrap(request,*args,**kwargs):
#             key = 'url_%s'%request.get_full_path()
#             response = cache.get(key)
#             if response is None:
#                 print('execute...')
#                 response = func(request,*args,**kwargs)
#                 cache.set(key,response,timeout)
#             return response
#         return wrap
#     return article_cache

@getip
@page_cache(5)
def detail(request,id):
    count = redis.zincrby('posts',id,1)
    print('aa',count)
    p = Posts.objects.filter(id=id)[0]
    context = {'title': p.ptitle, 'post': p,'count':int(count)}
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

def coll_post(request,id):
    post = Posts.objects.filter(id=id)[0]
    username = request.session.get('user')
    user = User.objects.filter(username=username)[0]
    if post.pcollect_user.filter(username=username).exists():
        post.pcollect_user.remove(user)
        post.save()
        return JsonResponse({'status':'remove'})

    else:
        post.pcollect_user.add(user)
        post.save()
        return JsonResponse({'status':'add'})

def mycoll(request):
    username = request.session.get('user')
    user = User.objects.filter(username=username)[0]
    posts = user.cuser.all()
    context = {'posts':posts}
    return render(request,'mycollections.html',context)

