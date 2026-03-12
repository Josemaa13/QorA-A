# Suggest users that my followings follow, but I don't follow yet
# Logic: (Me) -> (Friend) -> (Stranger)
RECOMMEND_USERS_QUERY = """
    MATCH (user:User {id: $user_id})-[:FOLLOWS]->(friend:User)-[:FOLLOWS]->(rec_user:User)
    WHERE NOT (user)-[:FOLLOWS]->(rec_user) AND user.id <> rec_user.id
    RETURN rec_user.id AS id, count(friend) AS mutual_connections
    ORDER BY mutual_connections DESC
    LIMIT 5
"""

# Suggest topics related to topics I already follow
# Logic: (Me) -> (MyTopic) <- (Document) -> (RecommendedTopic)
# "People who uploaded about X also uploaded about Y" implies connection via Documents
RECOMMEND_TOPICS_QUERY = """
    MATCH (user:User {id: $user_id})-[:INTERESTED_IN]->(my_topic:Topic)<-[:HAS_TOPIC]-(document:Document)-[:HAS_TOPIC]->(rec_topic:Topic)
    WHERE NOT (user)-[:INTERESTED_IN]->(rec_topic) AND my_topic.id <> rec_topic.id
    RETURN rec_topic.id AS id, count(document) AS strength
    ORDER BY strength DESC
    LIMIT 5
"""