import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    nameAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def __str__(self):
        return self.ratingAuthor

    def update_rating(self):
        total_post_rating = sum(post.rating * 3 for post in self.posts.all())
        total_comment_rating = sum(comment.rating for comment in self.comments.all())
        total_comment_post_rating = sum(comment.post.rating for comment in self.comments.filter(post__author=self))

        self.rating = total_post_rating + total_comment_rating + total_comment_post_rating
        self.save()


class Category(models.Model):
    titleCategory = models.CharField(max_length=32, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postType = models.CharField(TYPE_CHOICES, max_length=16)
    postDateTime = models.DateTimeField(auto_now_add=True)
    postCategories = models.ManyToManyField(Category, through='PostCategory')
    postContent = models.CharField(max_length=526)
    postRating = models.IntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        if len(self.postContent) > 124:
            return self.postContent[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.CharField(max_length=128)
    commentDateTime = models.DateTimeField(auto_now_add=True)
    commentRating = models.IntegerField(default=0)

    def __str__(self):
        return self.commentUser

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()

