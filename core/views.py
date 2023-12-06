from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import Http404, get_object_or_404

from .models import Post, User, Comment
from .forms import ProfileCreationForm, PostCreationForm, CommentCreationForm


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'core/post_list.html'
    paginate_by = 50


class PostCreationView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreationForm
    success_url = reverse_lazy('post_list')
    template_name = 'core/post_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'core/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().filter(post=self.object.pk)
        context['comment_form'] = CommentCreationForm
        return context


class CommentCreationView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentCreationForm
    template_name = 'core/comment_create.html'

    def get_success_url(self):
        return get_object_or_404(Post, id=self.kwargs.get('pk')).get_absolute_url()

    def form_valid(self, form):
        form.instance.upload_by = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'core/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[str(self.kwargs.get('post_pk'))])

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        if self.request.user != comment.upload_by:
            raise Http404('Страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class CommentChangeView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    template_name = 'core/comment_update.html'
    fields = ['text_of_comment', 'image_of_comment']

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[str(self.kwargs.get('post_pk'))])

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        if self.request.user != comment.upload_by:
            raise Http404('Страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class UserCreationView(generic.CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sighup.html'


class UserChangeView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'core/user_update.html'
    fields = ['email', 'description', 'avatar']

    def get_success_url(self):
        return self.object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            raise Http404('Страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = 'core/user_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != request.user:
            raise Http404('Страница не найдена')
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'core/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().filter(created_by=self.request.user)

        return context

