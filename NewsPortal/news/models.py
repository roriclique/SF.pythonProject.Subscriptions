from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.authorUser)

    def update_rating(self):
        postRate = self.post_set.aggregate(rPost=Sum('ratingPost'))
        pRate = 0
        pRate += postRate.get('rPost')

        commentRate = self.authorUser.comment_set.aggregate(rComment=Sum('ratingComment'))
        cRate = 0
        cRate += commentRate.get('rComment')

        self.ratingAuthor = pRate * 3 + cRate
        self.save()


class Topics(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subs = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return '{}'.format(self.name)


class Post(models.Model):
    authorPost = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE='AT'
    NEWS='NW'
    CATEGORY_CHOICES = (
        (NEWS,'Новость'),
        (ARTICLE,'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postTopic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    ratingPost = models. IntegerField(default=0)
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name="ID")

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def update_url(self):
        return reverse('update_post', kwargs={'slug': self.slug})

    def delete_url(self):
        return reverse('delete_post', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Topics, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    ratingComment = models. IntegerField(default=0)

    def like(self):
        self.ratingComment += 1
        self.save()

    def dislike(self):
        self.ratingComment -= 1
        self.save()



