from django.shortcuts import render,redirect, get_object_or_404
from .models import CicloAhorro, Aporte, ParticipanteCiclo
from .forms import CicloAhorroForm, AporteForm, ParticipanteCicloForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def inicio(request):
    return render(request, 'gestion/inicio.html')

@login_required
def listar_ciclos(request):
    ciclos = CicloAhorro.objects.all()
    return render(request,'gestion/listar_ciclos.html',{'ciclos':ciclos})

@login_required
def crear_ciclo(request):
    if request.method == 'POST':
        form = CicloAhorroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ciclos')
    else:
        form = CicloAhorroForm()

    return render(request, 'gestion/crear_ciclo.html',{'form':form})

@login_required
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

@login_required
def detalles_ciclo(request, ciclo_id):
    ciclo = get_object_or_404(CicloAhorro, id = ciclo_id)
    participantes = ParticipanteCiclo.objects.filter(ciclo=ciclo).order_by('orden_pago')

    return render(request, 'gestion/detalle_ciclo.html', {'ciclo':ciclo, 'particiopantes':participantes})
   
@login_required
def agregar_participante(request,ciclo_id):
    ciclo = get_object_or_404(CicloAhorro, id = ciclo_id)

    if request.method == 'POST':
        form = ParticipanteCicloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participante agregado correctamente al ciclo")
            return redirect('detalles_ciclo',ciclo_id = ciclo.id)
    else:
        form = ParticipanteCicloForm()

    return render(request, 'gestion/agregar_participante.html',{'form':form, 'ciclo':ciclo})