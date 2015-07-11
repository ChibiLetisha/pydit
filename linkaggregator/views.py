from django import forms
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import modelform_factory
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView, DetailView, CreateView, FormView, RedirectView, View
from linkaggregator.models import Post, Comment, Vote


class LoginRequiredMixin(View):
    """
    Checks if user has been logged in.
    Doesn't let unauthorized people access the page.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class PostList(ListView):
    """
    Lists out the existing posts.
    """
    model = Post
    template_name = 'home.html'


class SinglePost(DetailView):
    """
    Shows a single post which the user opened.
    """
    model = Post
    template_name = 'post.html'


class NewPost(LoginRequiredMixin, CreateView):
    """
    Saves posts created by logged in users.
    """
    model = Post
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')
    fields = ['title', 'link', 'description']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.slug = slugify(post.title)
        post.save()
        return super(NewPost, self).form_valid(form)


class NewComment(LoginRequiredMixin, CreateView):
    """
    Saves comments posted by logged in users.
    """
    model = Comment
    fields = ['text']

    def get(self, request, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.save()
        post = Post.objects.get(slug=self.kwargs['slug'])
        post.comments.add(comment)
        return super(NewComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'slug': self.kwargs['slug']})


class Login(FormView):
    """
    Logs in a registered user if the username and the password is valid.
    """
    form_class = AuthenticationForm
    template_name = 'login_form.html'

    def form_valid(self, form):
        redirect_to = reverse_lazy('home')
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return HttpResponseRedirect(redirect_to)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)


class Logout(RedirectView):
    """
    Logs out the current user.
    """
    url = reverse_lazy('home')
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        return super(Logout, self).dispatch(request, *args, **kwargs)


class Register(CreateView):
    """
    Registers an user with the given username and password.
    """
    model = User
    template_name = 'register_form.html'
    success_url = reverse_lazy('home')
    fields = ['username', 'password']
    widgets = {
        'password': forms.PasswordInput
    }

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        return super(Register, self).form_valid(form)

    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)

class VoteView(RedirectView):
    """
    Lets users vote on posts. Negative or positive votes available.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.get(slug=self.kwargs['slug'])
        if post.votes.filter(user=self.request.user).count():
            actual_vote = post.votes.filter(user=self.request.user)[0]
            post.votes.remove(actual_vote)
        vote_state = False
        if self.kwargs['state'] == 'y':
            vote_state = True
        vote, created = Vote.objects.get_or_create(user=self.request.user, vote=vote_state)
        post.votes.add(vote)
        return self.request.META.get('HTTP_REFERER', reverse('home'))
