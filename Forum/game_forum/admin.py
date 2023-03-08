from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Author, Comment, Category, PostCategory

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)


@admin.register
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')


