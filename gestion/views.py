from django.shortcuts import render,redirect, get_object_or_404
from .models import CicloAhorro, Aporte, ParticipanteCiclo
from .forms import CicloAhorroForm, AporteForm, ParticipanteCicloForm, OrdenPagoForm, PagoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

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

    return render(request, 'gestion/detalle_ciclo.html', {'ciclo':ciclo, 'participantes':participantes})
   
@login_required
def agregar_participante(request, ciclo_id):
    ciclo = get_object_or_404(CicloAhorro, id=ciclo_id)

    if request.method == 'POST':
        form = ParticipanteCicloForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.ciclo = ciclo 
            participante.save()
            messages.success(request, "Participante agregado exitosamente.")
            return redirect('detalles_ciclo', ciclo_id=ciclo.id)
    else:
        form = ParticipanteCicloForm(initial={'ciclo': ciclo})

    return render(request, 'gestion/agregar_participante.html', {'form': form, 'ciclo': ciclo})

@login_required
def sortear_orden(request, ciclo_id):
    # Vista para sortear el orden de pago de los participantes
    ciclo = get_object_or_404(CicloAhorro, id=ciclo_id)
    ParticipanteCiclo.sortear_orden(ciclo_id)
    messages.success(request, "Sorteo realizado satisfactoriamente")
    return redirect('detalles_ciclo', ciclo_id=ciclo.id)

@login_required
def modificar_orden(request, participante_id):
    """Vista para cambiar manualmente el orden de pago"""
    participante = get_object_or_404(ParticipanteCiclo, id=participante_id)
    if request.method == 'POST':
        form = OrdenPagoForm(request.POST, instance=participante)
        if form.is_valid():
            form.save()
            messages.success(request, "Orden de pago actualizado.")
            return redirect('detalles_ciclo', ciclo_id=participante.ciclo.id)
    else:
        form = OrdenPagoForm(instance=participante)

    return render(request, 'gestion/modificar_orden.html', {'form': form, 'participante': participante})

@login_required
def eliminar_participante(request, participante_id):
    """Vista para eliminar un participante de un ciclo con confirmación."""
    participante = get_object_or_404(ParticipanteCiclo, id=participante_id)

    if request.method == 'POST':
        participante.delete()
        messages.success(request, f"El participante {participante.usuario.username} ha sido eliminado del ciclo.")
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=400)


@login_required
def registrar_pago(request, ciclo_id):
    # Vista para registrar pagos en un ciclo siguiendo el orden de pago
    ciclo = get_object_or_404(CicloAhorro, id=ciclo_id)
    participantes = ParticipanteCiclo.objects.filter(ciclo=ciclo).order_by('orden_pago')

    if not participantes.exists():
        ciclo.estado = "FINALIZADO"
        ciclo.save()
        messages.success(request, "Todos los pagos han sido realizados. Ciclo finalizado.")
        return redirect('detalles_ciclo', ciclo_id=ciclo.id)

    siguiente_participante = participantes.first()  # El siguiente en recibir pago

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Pago registrado para {siguiente_participante.usuario.username}")
            return redirect('detalles_ciclo', ciclo_id=ciclo.id)
    else:
        form = PagoForm(initial={'usuario': siguiente_participante.usuario, 'ciclo': ciclo, 'monto': ciclo.monto_por_participante})

    return render(request, 'gestion/registrar_pago.html', {'form': form, 'ciclo': ciclo})