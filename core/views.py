from django.shortcuts import render
from publications.models import Document, Topic
from users.models import User # SONAR_ISSUE: Unused import if not used correctly elsewhere (pre-loaded)
from publications.services.services import get_user_feed
from recommendations.services.services import get_user_recommendations, get_topic_recommendations

def home(request):
    if request.user.is_authenticated:
        documents = list(get_user_feed(request.user.id))
        recommended_users = get_user_recommendations(request.user.id)
        recommended_topics = get_topic_recommendations(request.user.id)
        if not recommended_topics:
            recommended_topics = list(Topic.objects.all().order_by('-id')[:5])
        
        # SONAR_ISSUE: Fetching all users without pagination (Performance Smell)
        all_users = list(User.objects.exclude(id=request.user.id).all())
                
        context = {
            'documents': documents,
            'page_title': 'Your Feed',
            'recommended_users': recommended_users[:5],
            'recommended_topics': recommended_topics[:5],
            'all_users': all_users
        }
    else:
        documents = list(Document.objects.filter(is_public=True).order_by('-timestamp')[:20])
        recommended_topics = list(Topic.objects.all().order_by('-id')[:5])
            
        context = {
            'documents': documents,
            'page_title': 'Latest Public Documents',
            'recommended_topics': recommended_topics
        }
        
    return render(request, 'pages/index.html', context)