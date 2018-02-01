from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$', views.getlist),  #跳转到问题页面
    url(r'^login/$', views.login_view),  #登录页面
    url(r'^register/$', views.regina),   #注册页面
    url(r'^logout/$', views.logout_view), #登出页面
    url(r'^user/$', views.user_view), #用户管理页面
    url(r'^answer/$', views.answer_view), #回答页面
    url(r'^answeruserview/$', views.answeruserview), #用户进入回答页面
    url(r'^api/todoadd/$', views.question_add), #添加问题
    url(r'^api/todogetlist/$', views.todogetlist), #添加问题后更新问题
    url(r'^api/answeradd/$', views.answer_add), #添加回答
    url(r'^api/answergetlist/$', views.answerlist), #添加回答更新回答
    url(r'^api/followexe/$', views.followexe), #关注处理
    url(r'^api/unfollowexe/$', views.unfollowexe), #取消关注处理
    url(r'^api/likeexe/$', views.likeexe), #点赞处理
]