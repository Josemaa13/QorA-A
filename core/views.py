from django.shortcuts import render
from publications.models import Document
from publications.services.services import get_user_feed
from recommendations.services.services import get_user_recommendations, get_topic_recommendations

def home(request):
    if request.user.is_authenticated:
        documents = list(get_user_feed(request.user.id))
        recommended_users = get_user_recommendations(request.user.id)
        recommended_topics = get_topic_recommendations(request.user.id)
                
        context = {
            'documents': documents,
            'page_title': 'Your Feed',
            'recommended_users': recommended_users[:5],
            'recommended_topics': recommended_topics[:5]
        }
    else:
        documents = list(Document.objects.filter(is_public=True).order_by('-timestamp')[:20])
            
        context = {
            'documents': documents,
            'page_title': 'Latest Public Documents'
        }
        
    return render(request, 'pages/index.html', context)