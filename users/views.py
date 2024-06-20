from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, FormView, DeleteView
from .models import CustomUser, Newsletter
from .forms import CustomUserCreationForm, ProfileForm, ContactForm
from message_board.models import Post
from responses.models import Responses
from django.contrib import messages
from django.core.mail import send_mail
from .forms import NewsletterForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()
        send_mail(
            'Подтверждение регистрации',
            'Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return response

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.request.GET.get('post_id')
        responses = Responses.objects.filter(post__author=self.request.user)
        if post_id:
            responses = responses.filter(post_id=post_id)
        context['responses'] = responses
        context['posts'] = Post.objects.filter(author=self.request.user)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

class ContactView(FormView):
    template_name = 'users/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        send_mail(
            'Новое сообщение с сайта',
            form.cleaned_data['message'],
            form.cleaned_data['email'],
            ['admin@example.com'],
            fail_silently=False,
        )
        return super().form_valid(form)

class UserProfileView(DetailView):
    model = CustomUser
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.get_object())
        return context

class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Responses
    template_name = 'responses/response_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Responses.objects.filter(post__author=self.request.user)

class ResponseAcceptView(LoginRequiredMixin, UpdateView):
    model = Responses
    fields = []
    template_name = 'responses/response_confirm_accept.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = self.get_object()
        response.accepted = True
        response.save()
        send_mail(
            'Ваш отклик был принят',
            f'Ваш отклик на объявление "{response.post.title}" был принят.',
            'from@example.com',
            [response.author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'users/newsletter_form.html'
    success_url = reverse_lazy('newsletter_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        newsletter = self.object
        recipients = User.objects.values_list('email', flat=True)
        send_mail(
            newsletter.subject,
            newsletter.message,
            'from@example.com',
            recipients,
            fail_silently=False,
        )
        return response
