from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, PostSearchForm, PostImageFormSet
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = 'message_board/home.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'message_board/post_detail.html'
    context_object_name = 'post'

class PostListView(ListView):
    model = Post
    template_name = 'message_board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PostSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['q']:
                queryset = queryset.filter(content__icontains=form.cleaned_data['q'])
            if form.cleaned_data['category']:
                queryset = queryset.filter(category=form.cleaned_data['category'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_form'] = PostSearchForm(self.request.GET)
        return context

class CategoryPostsView(ListView):
    model = Post
    template_name = 'message_board/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(category__pk=self.kwargs['pk'])

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'message_board/post_form.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['images'] = PostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['images'] = PostImageFormSet()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  # Установка текущего пользователя как автора
        response = super().form_valid(form)
        context = self.get_context_data()
        images = context['images']
        if images.is_valid():
            images.instance = self.object
            images.save()
        return response

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'message_board/post_form.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['images'] = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['images'] = PostImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        context = self.get_context_data()
        images = context['images']
        if images.is_valid():
            images.instance = self.object
            images.save()
        return response

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'message_board/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
