from django.views.generic import CreateView, ListView
from .models import Responses
from .forms import ResponseForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class ResponseCreateView(CreateView):
    model = Responses
    form_class = ResponseForm
    template_name = 'responses/response_form.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = self.request.user
        response.post_id = self.kwargs['post_id']
        response.save()
        send_mail(
            'Новый отклик на ваше объявление',
            f'Вы получили новый отклик от {response.author.username}',
            'from@example.com',
            [response.post.author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class ResponseListView(LoginRequiredMixin, ListView):
    model = Responses
    template_name = 'responses/response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Responses.objects.filter(post__author=self.request.user)

def delete_response(request, pk):
    response = get_object_or_404(Responses, pk=pk, post__author=request.user)
    response.delete()
    messages.success(request, "Отклик удален.")
    return redirect('response_list')

def accept_response(request, pk):
    response = get_object_or_404(Responses, pk=pk, post__author=request.user)
    # Отправка уведомления о принятии
    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{response.post.title}" был принят.',
        'noreply@example.com',
        [response.author.email],
        fail_silently=False,
    )
    messages.success(request, "Отклик принят.")
    return redirect('response_list')