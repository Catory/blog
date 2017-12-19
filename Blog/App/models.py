from django.db import models
from werkzeug.security import generate_password_hash,check_password_hash
from django.utils import timezone
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password_hash = models.CharField(max_length=200)
    email = models.CharField(max_length=50)

    @property
    def password(self):
        raise AttributeError('密码是不可读属性')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


    class Meta:
        db_table = 'blog_user'


class Posts(models.Model):
    pcontent = models.CharField(max_length=500)
    ptitle = models.CharField(max_length=50,default=' ')
    rid = models.IntegerField(default=0)
    ptime = models.DateTimeField(default=timezone.now)
    puser = models.ForeignKey(User)

    class Meta:
        db_table = 'blog_posts'
