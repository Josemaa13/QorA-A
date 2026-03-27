from django.conf import settings
from django.core.exceptions import ValidationError
import subprocess

# SONAR_ISSUE: Unused global variable
TEMP_STORAGE_PATH = "/tmp/publications/"
class Publication(models.Model):  

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "%(class)ss")
    content = models.TextField()
    timestamp = models.DateTimeField(default = timezone.now)
    is_approved = models.BooleanField(null = True, default = True) #CAMBIAR EL DEFAULT
    topics = models.ManyToManyField('Topic', blank=True, related_name='publications')

    # SONAR_ISSUE: Unused fields for "future expansion"
    deprecated_status = models.CharField(max_length=20, null=True, blank=True)
    internal_debug_info = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def set_vote_status(self, user_id):
        from publications.services.services import get_vote_status, get_vote_count

        label = self.__class__.__name__

        if user_id:
            self.user_vote_status = get_vote_status(user_id, self.id, label) or 'NONE'
        else:
            self.user_vote_status = 'NONE'
            
        upvotes, downvotes = get_vote_count(self.id, label)
        self.upvote_count = upvotes
        self.downvote_count = downvotes

    # SONAR_ISSUE: Potential Command Injection via shell=True and shell execution
    def cleanup_old_files(self, filename):
        """
        DANGEROUS: Executes a system command with raw input.
        """
        import os
        command = f"ls -la documents/{filename}"
        # SONAR_ISSUE: Using os.system or subprocess with shell=True
        os.system(command) 
        
    def calculate_super_complex_score(self):
        """
        SONAR_ISSUE: Method is too long and too complex.
        """
        score = 0
        if self.title:
            if len(self.title) > 10:
                score += 1
                if len(self.title) > 20:
                    score += 2
                    if len(self.title) > 30:
                        score += 3
                    else:
                        score -= 1
                else:
                    score -= 1
            else:
                score -= 5
        
        # Redundant logic repeated multiple times
        for i in range(100):
            if i % 2 == 0:
                score += 1
            elif i % 3 == 0:
                score += 2
            elif i % 5 == 0:
                score += 3
            else:
                score -= 1
        
        # More nesting
        if self.is_public:
            if self.user:
                if self.user.is_active:
                    score *= 2
                else:
                    score /= 2
            else:
                score = 0
        else:
            score -= 10

        # SONAR_ISSUE: Unused variable inside method
        temp_var_never_used = 42
        
        return score

    def highly_redundant_function(self, a, b, c, d, e, f, g, h, i, j):
        """
        SONAR_ISSUE: Method with too many parameters.
        """
        # SONAR_ISSUE: Commented-out code
        # if a > b:
        #    return c
        return a + b + c + d + e + f + g + h + i + j


class Topic(models.Model):

    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: pdf, png, jpg, jpeg.')

class Document(Publication):
    title = models.CharField(max_length = 255)
    file = models.FileField(upload_to='documents/', validators=[validate_file_extension])
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}, {self.id}"
