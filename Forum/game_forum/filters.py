from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from .models import Post, Category, Author
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
        }

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='All'
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='All'
    )

    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Пост добавлен после',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-locale'}
        )
    )

    added_earlier = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='lt',
        label='Пост добавлен ранее',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-locale'}
        )
    )
