from django.db import models
from django.http import request
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.utils import timezone
# Create your models here.
from Blog.settings import SECRET_KEY

class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password_hash = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=0)
    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_activate_token(self):
        s = Serializer(secret_key=SECRET_KEY,expires_in=3600)
        return s.dumps({'id':self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        if User.objects.filter(id = data['id']).exists():
            if not User.objects.filter(id=data['id'])[0].confirmed:
                user = User.objects.filter(id=data['id'])[0]
                user.confirmed = 1
            return True
        else:
            return False
    class Meta:
        db_table = 'blog_user'


class Posts(models.Model):
    pcontent = models.CharField(max_length=500)
    ptitle = models.CharField(max_length=50,default=' ')
    rid = models.IntegerField(default=0)
    ptime = models.DateTimeField(default=timezone.now)
    puser = models.ForeignKey(User)
    pcollect_user = models.ManyToManyField(User,related_name='cuser')
    class Meta:
        db_table = 'blog_posts'
        ordering = ['-ptime']

