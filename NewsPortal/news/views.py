from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from.filters import PostFilter
from.forms import PostForm


class PostList(ListView):
    model = Post
    context_object_name = 'Posts'
    queryset = Post.objects.order_by('-dateCreation')
    template_name = 'default.html'
    paginate_by = 3


class PostSearch(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'filter_form.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.filterset
        return context


class PostListDetail(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'PostDetails'

    def detail(request, slug):
        post = Post.objects.get(slug__iexact=slug)
        return render(request, 'detail.html', context={'post': post})


class PostCreateNews(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_form_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class PostCreateArticles(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_form_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AT'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'update_form.html'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    raise_exception = True
    model = Post
    template_name = 'delete_form.html'
    success_url = reverse_lazy('Default')


@login_required
@csrf_protect
def subscribe(request):
    if request.method == 'POST':
        topics_id = request.POST.get('topics_id')
        topic = Topics.objects.filter(id=topics_id).get()
        action = request.POST.get('action')

        if action == 'subscribe':
            subscribed = Subscription.objects.create(user=request.user, topics=topic)
            return render(subscribed, 'success_message.html')
        elif action == 'unsubscribe':
            unsubscribed = Subscription.objects.filter(user=request.user, topics=topic).delete()
            return render(unsubscribed, reverse_lazy('search_all_posts'))

    topics_with_subscriptions = Topics.objects.annotate(
        user_subscribed=Exists(Subscription.objects.filter(user=request.user, topics=OuterRef('pk')))).order_by('name')
    return render(request, 'subscriptions.html', {'topics': topics_with_subscriptions})
