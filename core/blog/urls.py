from django.urls import path, include, reverse_lazy
from . import views

app_name = 'blog'

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(),name='about'),
    path('post/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<pk>/remove/', views.PostDeleteView.as_view(),name='post_remove'),
    path('draft/', views.DraftListView.as_view(),name='post_draft_list'),
    path('post/<pk>/comment/', views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<pk>/approve/', views.comment_approve,name='comment_approve'),
    path('comment/<pk>/remove/', views.comment_remove,name='comment_remove'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish')
]
