from django.conf.urls import url
from App import views


urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^register/',views.register,name='register'),
    url(r'^doregister/',views.do_register,name='doregister'),
    url(r'^login/',views.login,name='login'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^sendposts/',views.sendposts,name='sendposts'),
    url(r'^detail/(\d+)/',views.detail,name='detail'),
    url(r'^cpost/(\d+)/',views.cposts,name='cposts'),
    url(r'^search/',views.search,name='search'),
    url(r'^registhandler/',views.register_handler,name='registhandler'),
    url(r'^loginhandler/',views.login_handler,name='loginhandler'),

]