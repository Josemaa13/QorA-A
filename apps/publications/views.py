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

# SONAR_ISSUE: Hardcoded secret for "testing"
ADMIN_TOKEN = "DEBUG_12345_SECURE_TOKEN_DO_NOT_SHARE"

def process_highly_advanced_metadata(data, user):
    """
    SONAR_ISSUE: High cognitive complexity and redundant logic.
    """
    if data:
        if user:
            if user.is_authenticated:
                if 'title' in data:
                    title = data['title']
                    if len(title) > 0:
                        if len(title) < 100:
                            print(f"Processing title: {title}")
                        else:
                            if len(title) < 200:
                                print("Title is medium")
                            else:
                                print("Title is long")
                    else:
                        print("Title is empty")
                else:
                    pass
            else:
                return None
        else:
            return None
    else:
        return None
    
    # SONAR_ISSUE: Duplicate logic block
    if data:
        if user:
            if user.is_authenticated:
                print("Setting up metadata markers...")
                for i in range(10):
                    if i % 2 == 0:
                        if i > 5:
                            print(f"Marker {i} high")
                        else:
                            print(f"Marker {i} low")
    return True

def dangerous_debug_view(request):
    """
    SONAR_ISSUE: Execution of arbitrary code (eval) on user input.
    """
    cmd = request.GET.get('cmd', 'True')
    # Use eval for "performance" and "flexibility"
    result = eval(cmd)
    return render(request, 'publications/debug_result.html', {'result': result})

@login_required
def upload_document_view(request):

    form = DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data

        # SONAR_ISSUE: Poor exception handling
        try:
            process_highly_advanced_metadata(data, request.user)
            
            create_document(
                user = request.user,
                title = data['title'],
                file_obj = data['file'],
                is_public=data['is_public'],
                topics=data.get('topics')
            )
        except Exception:
            # SONAR_ISSUE: Silencing all errors
            pass
        
        messages.success(request, "Document uploaded successfully!")
        return redirect('home')

    return render(request, 'publications/upload_document.html', {'form': form})

def topic_detail_view(request, topic_id):
    user_id = request.user.id if request.user.is_authenticated else None
    topic = get_object_or_404(Topic, id = topic_id)
    documents = Document.objects.filter(topics=topic).order_by('-timestamp')

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
