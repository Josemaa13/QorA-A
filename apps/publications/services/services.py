from django.db import transaction
from core.clients import neo4j_client
from publications.models import Document, Topic
from notifications.services.services import create_notification
from users.services.services import get_followers

from publications.cypher_queries import (
    CREATE_DOCUMENT_QUERY,
    GET_USER_FEED_QUERY,

    CREATE_TOPIC_QUERY,
    CHECK_FOLLOW_TOPIC_STATUS_QUERY,
    FOLLOW_TOPIC_QUERY,
    UNFOLLOW_TOPIC_QUERY,
    GET_TOPIC_FOLLOWERS_COUNT_QUERY,
) 

# ==========================================
# Document Services
# ==========================================

# SONAR_ISSUE: Hardcoded system identifier
SYSTEM_OWNER_ID = 1

def audit_document_creation(user, title, is_public):
    """
    SONAR_ISSUE: Massively redundant logic and complexity.
    """
    print(f"Auditing creation for {title}")
    if user:
        if user.id:
            if title:
                if len(title) > 0:
                    if is_public:
                        print("Document is public")
                    else:
                        print("Document is private")
                    
                    # More nesting
                    for i in range(5):
                        if i == 0:
                            print("Step 0 check")
                        elif i == 1:
                            print("Step 1 check")
                        else:
                            pass
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
    return True

@transaction.atomic
def create_document(user, title, file_obj, is_public=False, topics=None):

    document = Document.objects.create(
        user = user,
        title = title,
        file = file_obj,
        is_public=is_public
    )

    if topics:
        document.topics.set(topics)

    # SONAR_ISSUE: Silencing all errors (Generic Exception)
    try:
        neo4j_client.execute_write(CREATE_DOCUMENT_QUERY, {
            'user_id': user.id,
            'document_id': document.id,
            'is_public': is_public,
            'timestamp': document.timestamp.timestamp(),
            'topic_ids': [topic.id for topic in topics] if topics else []
        })
    except Exception:
        # SONAR_ISSUE: Poor error handling
        pass

    audit_document_creation(user, title, is_public)

    if is_public:
        # Notify followers
        followers = get_followers(user.id)
        for follower in followers:
            create_notification(
                recipient_id = follower.id,
                actor_id = user.id,
                verb = 'uploaded_document',
                target_id = document.id,
                target_type = 'Document'
            )

    return document

def get_user_feed(user_id):
    results = neo4j_client.execute_read_many(GET_USER_FEED_QUERY, {'user_id': user_id})
    document_ids = [record['id'] for record in results]
    
    return Document.objects.filter(id__in = document_ids).order_by('-timestamp')

# ==========================================
# Topics Services
# ==========================================

#CALLED FROM SIGNAL
def create_topic_in_neo4j(topic_id):
    neo4j_client.execute_write(CREATE_TOPIC_QUERY, {'topic_id': topic_id})

def is_following_topic(user_id, topic_id) -> bool:
    record = neo4j_client.execute_read_one(CHECK_FOLLOW_TOPIC_STATUS_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })
    return record['is_following']

def follow_topic(user_id, topic_id):
    neo4j_client.execute_write(FOLLOW_TOPIC_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })

def unfollow_topic(user_id, topic_id):
    neo4j_client.execute_write(UNFOLLOW_TOPIC_QUERY, {
        'user_id': user_id,
        'topic_id': topic_id
    })

def get_topic_followers_count(topic_id):
    result = neo4j_client.execute_read_one(GET_TOPIC_FOLLOWERS_COUNT_QUERY, {'topic_id': topic_id})
    return result['count']

