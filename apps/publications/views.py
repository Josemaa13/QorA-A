from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import User
from publications.models import Document, Topic
from .forms import DocumentForm
from django.contrib import messages
from publications.services.services import (
    create_document,

    is_following_topic,
    follow_topic,
    unfollow_topic,
    get_topic_followers_count,
) 

@login_required
def upload_document_view(request):

    form = DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data

        create_document(
            user = request.user,
            title = data['title'],
            file_obj = data['file'],
            is_public=data['is_public']
        )
        
        messages.success(request, "Document uploaded successfully!")
        return redirect('home')

    return render(request, 'publications/upload_document.html', {'form': form})

def topic_detail_view(request, topic_id):
    user_id = request.user.id if request.user.is_authenticated else None
    topic = get_object_or_404(Topic, id = topic_id)
    documents = [] 

    is_following = (
        request.user.is_authenticated 
        and is_following_topic(user_id, topic_id)
    )

    follower_count = get_topic_followers_count(topic_id)

    context = {
        'topic': topic,
        'is_following': is_following,
        'topic_follower_count': follower_count,
        'documents': documents
    }

    return render(request, 'publications/topic_detail.html', context)

@login_required
@require_POST
def follow_topic_view(request, topic_id):
    follow_topic(request.user.id, topic_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
@require_POST
def unfollow_topic_view(request, topic_id):
    unfollow_topic(request.user.id, topic_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
