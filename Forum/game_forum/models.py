from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField('Категория', max_length=64, unique=True, help_text='category name')
    subscribers = models.ManyToManyField(User, related_name='categories')
    description = models.TextField('Описание', default='Описание категории')
    url = models.SlugField(max_length=160, unique=True, default='url категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text='user name')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, help_text='post title')
    text = models.TextField('Тескт')
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')
    is_active = models.BooleanField(default=True)
    content = RichTextUploadingField(blank=True, null=True)

    url = models.SlugField(max_length=130, unique=True, default='url поста')
    image = models.ImageField(upload_to="posts/", default='Изображение')

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + "..."

    def __str__(self):
        return f'{self.title[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория поста"
        verbose_name_plural = "категории постов"

    def __str__(self):
        return f'{self.post.title} | {self.category.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    content = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
