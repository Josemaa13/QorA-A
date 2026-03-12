from django.urls import path

from publications import views

urlpatterns = [
    path('upload/', views.upload_document_view, name = 'upload_document'),
    path('topic/<int:topic_id>/', views.topic_detail_view, name = 'topic_detail'),
    path('follow/<int:topic_id>/', views.follow_topic_view, name = 'follow_topic'),
    path('unfollow/<int:topic_id>/', views.unfollow_topic_view, name = 'unfollow_topic'),
]