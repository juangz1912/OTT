from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import Item, Item2, Item3, Item4

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data = request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username = user_creation_form.cleaned_data['username'], password = user_creation_form.cleaned_data['password1']  )
            login(request, user)
            return redirect('home')

    return render(request, 'registration/register.html', data)

@login_required
def principal(request):
    obj=Item.objects.all()
    return render(request, 'core/products.html', {'obj':obj})

def perfil(request):
    return render(request,  'core/user.html')

def reggaeton(request):
    obj=Item2.objects.all()
    return render(request, 'core/reggaeton.html', {'obj':obj})

def trap(request):
    obj=Item3.objects.all()
    return render(request, 'core/trap.html', {'obj':obj})

def house(request):
    obj=Item4.objects.all()
    return render(request, 'core/house.html', {'obj':obj})