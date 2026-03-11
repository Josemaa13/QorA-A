from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .services.services import get_recent_page_views, get_recent_searches

@user_passes_test(lambda u: u.is_staff)
def dashboard_view(request):
    page_views = get_recent_page_views(limit=100)
    searches = get_recent_searches(limit=100)

    context = {
        'page_views': page_views,
        'searches': searches
    }
    return render(request, 'pages/analytics/dashboard.html', context)
