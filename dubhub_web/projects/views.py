from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, FileResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

from .models import Projects
from .forms import form_project

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Projects
    form_class = form_project
    template_name = 'create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        
        if not (user.is_superuser or user.is_staff or user.user_type == 3):
            raise PermissionDenied("Você não tem permissão para criar esse registro")
            #return HttpResponseForbidden("You do not have permission to access this page.")
        
        project = form.save(commit=False)
        project.director = user
        if 'foto' in self.request.FILES:
            project.foto = self.request.FILES['foto']
            print(project.foto)
        
        return super().form_valid(form)

class ProjectListView(ListView):
    model = Projects
    template_name = 'list.html'
    context_object_name = 'projects'

class FotoProject(View):
    def get(self, request, arquivo):
        try:
            project = Projects.objects.get(foto='projects/fotos/{}'.format(arquivo))
            return FileResponse(project.foto)
        except ObjectDoesNotExist:
            return Http404('<h1>Projeto não encontrado</h1>')