from users.models import UserRating, User
from django.db.models import Avg

def rate_user(rater_id, rated_user_id, score):
    """
    Rates a user or updates an existing rating.
    """
    rater = User.objects.get(id=rater_id)
    rated_user = User.objects.get(id=rated_user_id)
    
    # SONAR_ISSUE: Redundant check before update_or_create (coupling/complexity)
    if score < 1 or score > 5:
        return None
    
    rating, created = UserRating.objects.update_or_create(
        rater=rater,
        rated_user=rated_user,
        defaults={'score': score}
    )
    return rating

def get_average_rating(user_id):
    """
    Calculates the average rating for a user.
    """
    # SONAR_ISSUE: Calculating everything every time instead of caching (Performance Smell)
    avg_score = UserRating.objects.filter(rated_user_id=user_id).aggregate(Avg('score'))['score__avg']
    return round(avg_score, 1) if avg_score else 0.0

def get_total_ratings_count(user_id):
    """
    SONAR_ISSUE: Duplicated filter logic (filtering by user_id)
    """
    return UserRating.objects.filter(rated_user_id=user_id).count()
