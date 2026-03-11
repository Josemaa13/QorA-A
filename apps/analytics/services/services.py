from core.clients.mongodb_client import mongodb_client
from datetime import datetime
from django.utils import timezone

def track_page_view(user_id, url_path, ip_address):
    document = {
        "event_type": "page_view",
        "user_id": user_id,
        "url_path": url_path,
        "ip_address": ip_address,
        "timestamp": timezone.now().isoformat()
    }
    mongodb_client.insert_one("analytics", document)

def track_search(user_id, query):
    document = {
        "event_type": "search_query",
        "user_id": user_id,
        "query": query,
        "timestamp": timezone.now().isoformat()
    }
    mongodb_client.insert_one("analytics", document)

def get_recent_page_views(limit=100):
    return mongodb_client.find_many("analytics", filter={"event_type": "page_view"}, limit=limit, sort=[("timestamp", -1)])

def get_recent_searches(limit=100):
    return mongodb_client.find_many("analytics", filter={"event_type": "search_query"}, limit=limit, sort=[("timestamp", -1)])
