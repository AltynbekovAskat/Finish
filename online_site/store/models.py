from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.CharField(max_length=40)
    image = models.ImageField(upload_to='image/')
    website = models.URLField()

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}, {self.following}'


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to='post_image')
    video = models.FileField()
    description = models.TextField()
    hashtag = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.post}'

    class Meta:
        unique_together = ('user', 'post',)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField()
    parent = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, {self}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        unique_together = ('user', 'comment',)


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='store_user')
    image = models.ImageField(upload_to='store-image/')
    video = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.image}'


class Save(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='save_user')

    def __str__(self):
        return f'{self.user}'


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='save_item')
    save = models.ForeignKey(Save, on_delete=models.CASCADE, related_name='save')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, {self.save}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    create_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='message/', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
