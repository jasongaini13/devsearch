from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    fetured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    Vote_total = models.IntegerField(default=0, null=True, blank=True)
    Vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-Vote_ratio','-Vote_total','title']

    def update_vote_count(self):
        """
        Update the vote count for the project based on the number of reviews it has.
        """
        self.Vote_total = self.review_set.count()
        self.save()  
    
    def positive_feedback_percentage(self):
        """
        Calculate the percentage of positive feedback for the project.
        """
        if self.Vote_total > 0:
            positive_reviews = self.review_set.filter(value='up').count()
            return (positive_reviews / self.Vote_total) * 100
        else:
            return 0
        
    def reviewers(self):
        queryset = self.review.set.all().values_list('owner_id', flat=False)
        return queryset
              

    # def update_vote_count(self):
    #     """
    #     Update the vote count for the project based on the number of reviews it has.
    #     """
    #     self.Vote_total = self.review_set.count()
    #     self.save()

    # def positive_feedback_percentage(self):
    #     """
    #     Calculate the percentage of positive feedback for the project.
    #     """
    #     if self.Vote_total > 0:
    #         positive_reviews = self.review_set.filter(value='up').count()
    #         return (positive_reviews / self.Vote_total) * 100
    #     else:
    #         return 0

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to update the vote count of the associated project.
        """
        super().save(*args, **kwargs)
        self.project.update_vote_count()




       



class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
