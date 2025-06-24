from django.shortcuts import render
from django.views import View

class FotoUser(View):
    def get(self, request, arquivo):
        try:
            user = User.objects.get(foto='users/fotos/{}'.format(arquivo))
            return FileResponse(user.foto)
        except ObjectDoesNotExist:
            return Http404('<h1>Usuário não encontrado</h1>')