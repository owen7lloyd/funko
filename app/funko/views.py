from django.shortcuts import render

# Create your views here.

from .models import Brand, Pop


def home(request):
    brands = Brand.objects.all()
    context = {"brands": brands}
    return render(request, "funko/home.html", context)
