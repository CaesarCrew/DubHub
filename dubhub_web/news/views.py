from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import NewsSerializer
from .models import News, NewsMedia
from .forms import NewsForm, NewsMediaFormSet
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'create_news.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_formset'] = NewsMediaFormSet(self.request.POST or None, self.request.FILES or None, queryset=NewsMedia.objects.none(), prefix='form')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        form.instance.author = self.request.user

        if form.is_valid() and media_formset.is_valid():
            self.object = form.save()
            for media_form in media_formset:
                if media_form.cleaned_data:
                    media = media_form.save(commit=False)
                    media.news = self.object
                    media.save()
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'delete.html'
    success_url = reverse_lazy('home')

    """ def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_superuser or self.request.user.is_staff or self.request.user.user_type == 1):
            raise PermissionDenied("Você não tem permissão para deletar esse registro")
        return obj """

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'update.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_formset'] = NewsMediaFormSet(self.request.POST or None, self.request.FILES or None, queryset=NewsMedia.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        form.instance.author = self.request.user

        if form.is_valid() and media_formset.is_valid():
            self.object = form.save()
            for media_form in media_formset:
                if media_form.cleaned_data:
                    media = media_form.save(commit=False)
                    media.news = self.object
                    media.save()
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))

class NewsListView(ListView):
    model = News
    template_name = 'list_news.html'
    context_object_name = 'news'

class NewsAPICreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NewsAPIDeleteView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

class NewsAPIUpdateView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

class NewsAPIListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class NewsAPIGetView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if not (self.request.user.is_superuser or self.request.user.is_staff or obj.author == self.request.user):
            raise PermissionDenied("Você não tem permissão para ver esse registro")
        return obj