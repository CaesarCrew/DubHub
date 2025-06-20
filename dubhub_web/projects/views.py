from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Projects
from .forms import form_project

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Projects
    form_class = form_project
    template_name = 'create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user

        if user.is_superuser or user.is_staff or user.user_type == 'director':
            form.instance.director = user
            return super().form_valid(form)
        else:
            raise PermissionDenied("Você não tem permissão para criar esse registro")
            #return HttpResponseForbidden("You do not have permission to access this page.")