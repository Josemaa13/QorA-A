# ==========================================
# Document Queries
# ==========================================

CREATE_DOCUMENT_QUERY = """
    MATCH (user:User {id: $user_id})
    MERGE (document:Document {id: $document_id})
    SET document.timestamp = $timestamp,
        document.is_public = $is_public
    MERGE (user)-[:UPLOADED]->(document)
"""

# ==========================================
# Topic Queries
# ==========================================

CREATE_TOPIC_QUERY = """
    MERGE (:Topic {id: $topic_id})
"""

CHECK_FOLLOW_TOPIC_STATUS_QUERY = """
    MATCH (:User {id: $user_id})-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    RETURN count(r) > 0 as is_following
"""

FOLLOW_TOPIC_QUERY = """
    MATCH (user:User {id: $user_id})
    MATCH (topic:Topic {id: $topic_id})
    MERGE (user)-[:INTERESTED_IN]->(topic)
"""

UNFOLLOW_TOPIC_QUERY = """
    MATCH (:User {id: $user_id})-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    DELETE r
"""

GET_TOPIC_FOLLOWERS_COUNT_QUERY = """
    MATCH (:User)-[r:INTERESTED_IN]->(:Topic {id: $topic_id})
    RETURN count(r) as count
"""

# ==========================================
# Feed Queries
# ==========================================
GET_USER_FEED_QUERY = """
    MATCH (user:User {id: $user_id})
    
    OPTIONAL MATCH (user)-[:UPLOADED]->(own_doc:Document)
    
    OPTIONAL MATCH (user)-[:FOLLOWS]->(:User)-[:UPLOADED]->(followed_doc:Document)
    WHERE followed_doc.is_public = true
    
    WITH collect(own_doc) + collect(followed_doc) AS documents, user
    UNWIND documents AS document
    
    WITH DISTINCT document
    WHERE document IS NOT NULL
    
    ORDER BY document.timestamp DESC
    LIMIT 50
    
    RETURN document.id AS id
"""
