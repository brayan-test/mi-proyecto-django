from django.shortcuts import render,redirect, get_object_or_404
from .models import CicloAhorro, Aporte
from .forms import CicloAhorroForm, AporteForm

# Create your views here.
def listar_ciclos(request):
    ciclos = CicloAhorro.objects.all()
    return render(request,'gestion/listar_ciclos.html',{'ciclos':ciclos})

def crear_ciclo(request):
    if request.method == 'POST':
        form = CicloAhorroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ciclos')
    else:
        form = CicloAhorroForm()

    return render(request, 'gestion/crear_ciclo.html',{'form':form})

def editar_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(CicloAhorro,id=ciclo_id)
    if request.method == 'POST':
        form = CicloAhorroForm(request.POST,instance=ciclo)
        if form.is_valid():
            form.save()
            return redirect('listar_ciclos')
    else:
        form = CicloAhorroForm(instance=ciclo)

    return render(request, 'gestion/editar_ciclo.html',{'form':form})
    
def eliminar_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(CicloAhorro,id=ciclo_id)
    ciclo.delete()
    return redirect('listar_ciclos')
    
def listar_aportes(request):
    aportes = Aporte.objects.all()
    return render(request,'gestion/listar_aportes.html',{'aportes':aportes})

def crear_aporte(request):
    if request.method == 'POST':
        form = AporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_aportes')
    else:
        form = AporteForm()

    return render(request, 'gestion/crear_aporte.html',{'form':form})
