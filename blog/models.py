from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone
from django_summernote import models as summer_model
from django_summernote import fields


class User(AbstractUser):
    like_posts = models.ManyToManyField('Post', blank=True, related_name='like_users')


class Post(summer_model.Attachment):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = fields.SummernoteTextField(default='')
    # text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # like_posts = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_users')

    like_count = models.PositiveIntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    password = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

