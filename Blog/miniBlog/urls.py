from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('bloggers/<int:pk>', views.BloggerDetailView.as_view(), name='blogger'),
    path('bloggers/', views.BloggerList.as_view(), name='bloggers'),
    path('blogs/<int:blog_id>>/posts/<int:pk>', views.BlogMessageDetailView.as_view(), name='message_detail'),
    path(r'blogs/<int:blog_id>>/posts/<int:post_id>/newcomment', views.new_comment, name='new_comment'),
]
