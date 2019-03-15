"""为应用程序users定义URL模式"""

from django.conf.urls import url
# from django.contrib.auth.views import login     # 导入默认视图login
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'

urlpatterns = [
    # 登录页面
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # url(r'^users/login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # 注销页面
    url(r'^logout/$', views.logout_view, name='logout'),
    # 注册页面
    url(r'^register/$',views.register, name='register'),

]