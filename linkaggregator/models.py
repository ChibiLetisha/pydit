from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Vote(models.Model):
    vote = models.NullBooleanField()
    user = models.ForeignKey(User)


class Post(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, blank=True)
    votes = models.ManyToManyField(Vote, blank=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    def get_positive_votes(self):
        return self.votes.filter(vote=True).count()

    def get_negative_votes(self):
        return self.votes.filter(vote=False).count()
