from django.shortcuts import render
from django.views import View

class BasePageView(View):

    def get(self, request):
        return render(request, 'app/base_home.html')












# Create your views here.
