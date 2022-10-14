from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import DataMixin


menu = ({"title": "Home", "url_name": "home"},
        {"title": "About", "url_name": "about"},
        {"title": "Add article", "url_name": "addarticle"},
        {"title": "Feedback", "url_name": "feedback"})


class CarHome(DataMixin, ListView):
    model = Car
    template_name = 'cars_app/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Homepage')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Car.objects.filter(is_published=True)
    

def about(request):
    categories = Category.objects.all()
    return render(request, 'cars_app/about.html', {'categories': categories, 'menu': menu, 'title': 'About'})


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars_app/addarticle.html'
    login_url = 'signin'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add article')
        return dict(list(context.items()) + list(c_def.items()))


class FeedBackView(LoginRequiredMixin, DataMixin, FormView):
    form_class = EmailSendForm
    template_name = 'cars_app/feedback.html'
    login_url = 'signin'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact us')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form: EmailSendForm):
        form.send_email()
        return redirect('feedbacksuccess')
    
class FeedbackSuccess(DataMixin, TemplateView):
    template_name = 'cars_app/success.html'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Success')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars_app/register.html'
    success_url = reverse_lazy('signin')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign up')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'cars_app/signin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('signin')


class ShowPost(DataMixin, DetailView):
    model = Car
    template_name = 'cars_app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class CarCategory(DataMixin, ListView):
    model = Car
    template_name = 'cars_app/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['posts'][0].category))
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Car.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

 
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
