from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .models import Alumno, AñoCurso
from apps.home.models import Alumno, AñoCurso



@login_required(login_url="/login/")
def pages(request):
    context = {}
    load_template = request.path.split('/')[-1]

    # Redirigir a la página de administración si la URL es 'admin'
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    # Si la URL corresponde a una vista específica, renderizar esa vista
    if load_template in ['seccion', 'notas', 'testvocacional', 'cuestionario']:
        return globals()[load_template](request)

    # Si la URL no coincide con ninguna vista específica, cargar la plantilla HTML correspondiente
    try:
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    # Manejar el caso en que no se encuentre la plantilla
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    # Manejar otros errores
    except Exception as e:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# paginas

@login_required(login_url="/login/")
def perfil(request):
    context = {
        'segment': 'perfil' 
    }
    return render(request, 'home/perfil.html', context)

@login_required(login_url="/login/")
def alumnos(request):
    
    seccion = request.GET.get('seccion')

    alumnos = Alumno.objects.filter(año_cursado__nombre=seccion)

    
    añocursos = AñoCurso.objects.all()

    context = {'segment': 'alumnos', 'alumnos': alumnos,'seccion': seccion, 'añocursos': añocursos}
    return render(request, 'home/alumnos.html', context)

@login_required(login_url="/login/")
def seccion(request):
    años = AñoCurso.objects.all()
    grupos = {
        'Primeros medios': [],
        'Segundos medios': [],
        'Terceros medios': [],
        'Cuartos medios': [],
    }
    Alumnos = Alumno.objects.all()
    for año in años:
        nombre = año.nombre
        if nombre.startswith('Primero medio'):
            grupos['Primeros medios'].append(nombre)
        elif nombre.startswith('Segundo medio'):
            grupos['Segundos medios'].append(nombre)
        elif nombre.startswith('Tercero medio'):
            grupos['Terceros medios'].append(nombre)
        elif nombre.startswith('Cuarto medio'):
            grupos['Cuartos medios'].append(nombre)

    context = {'segment': 'alumnos', 'grupos': grupos, 'alumnos': alumnos}
    return render(request, 'home/seccion.html', context)

@login_required(login_url="/login/")
def notas(request):
    context = {'segment': 'notas'}
    return render(request, 'home/notas.html', context)

@login_required(login_url="/login/")
def testvocacional(request):
    context = {'segment': 'testvocacional'}
    return render(request, 'home/testvocacional.html', context)

@login_required(login_url="/login/")
def cuestionario(request):
    context = {'segment': 'cuestionario'}
    return render(request, 'home/cuestionario.html', context)