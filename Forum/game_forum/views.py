from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import *
from .filters import PostFilter
from django.views import View
from .tasks import weekly_sending, sending_about
import logging
from django.utils import timezone
import pytz


logger = logging.getLogger(__name__)


class PostList(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'game_forum.html'
    context_object_name = 'game_forum'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        current_time = timezone.localtime(timezone.now())
        print(current_time)
        models = Post.objects.all()
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/game_forum')

    def get_page_context(request):
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'game_forum.html', {'page_obj': page_obj})


class PostDetail(DetailView):
    model = Post
    ordering = 'game_forum'
    template_name = 'post_id.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        current_time = timezone.localtime(timezone.now())
        print(current_time)
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('game_forum.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('game_forum.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('game_forum.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def update_me(request):
    user = request.user
    premium_group = Group.objects.get()
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('game_forum/')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_game_forum'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get()
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей из категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class WeeklySendingView(View):
    def get(self, request):
        weekly_sending.delay()
        return redirect('/')


class SendingAboutView(View):
    def get(self, request):
        sending_about.delay()
        return redirect('/')



