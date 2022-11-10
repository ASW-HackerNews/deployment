from django.urls import path

from . import views

urlpatterns = [
    path('', views.posts_relevant, name='relevant'),
    path('newest/', views.posts, name='newest'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('submit/', views.submit, name='submit'),
    path('ask/', views.ask, name='ask'),
    path('<int:post_id>/unic_post', views.unic_post, name="unic_post"),
    path('userpost/<str:username>',views.userpost, name='usersubmissions'),
    path('uservoted_posts/', views.uservoted_posts, name='uservoted_posts'),
    path('uservoted/', views.uservoted, name='uservoted'),
    path('uservoted_comments/', views.uservoted_comments, name='uservoted_comments'),
    path('usercomments/<str:username>',views.usercomments, name='usercomments'),

    # path('posts/delete/<str:title>', views.submit, name='submit'),
    # Aquí hay que mirar cual es el identificador de verdad
]

 