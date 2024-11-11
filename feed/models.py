from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from users.models import PinklerUser

LIKE_CHOISE = [
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
]

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='feed', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(PinklerUser, blank=True, related_name='likes')
    bookmark = models.ManyToManyField(PinklerUser, blank=True, related_name='bookmarks')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(PinklerUser, on_delete=models.CASCADE, related_name='feed')

    def __str__(self):
        return str(self.content)
    
    def number_of_likes(self):
        return self.liked.all().count()
    
    def number_of_comments(self):
        return self.comment_set.all().count()
    
    def created_just_now(self):
        return timezone.now() - self.created < timezone.timedelta(minutes=1)
    
    class Meta:
        ordering = ('-created', )
        unique_together = (('author', 'content'),)
    

class Comment(models.Model):
    user = models.ForeignKey(PinklerUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField(max_length=150)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Like(models.Model):
    user = models.ForeignKey(PinklerUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOISE, max_length=8)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}-{self.value}"
