from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy
from .models import Character
from .forms import CharacterForm

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = 'create_character.html'
    context_object_name = 'character'
    success_url = reverse_lazy('list-characters')

class CharacterListView(ListView):
    model = Character
    template_name = 'list_character.html'
    context_object_name = 'characters'

class CharacterDeleteView(DeleteView):
    model = Character
    template_name = 'delete_character.html'
    context_object_name = 'character'
    success_url = reverse_lazy('list-characters')