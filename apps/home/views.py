from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .models import Alumno
from apps.home.models import Alumno



@login_required(login_url="/login/")
def pages(request):
    context = {}
    load_template = request.path.split('/')[-1]

    # Redirigir a la página de administración si la URL es 'admin'
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    # Si la URL corresponde a una vista específica, renderizar esa vista
    if load_template in ['alumnos', 'notas', 'testvocacional', 'cuestionario']:
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

    return render(request,'home/perfil.html')

@login_required(login_url="/login/")
def alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'home/alumnos.html', {"alumnos":alumnos})

@login_required(login_url="/login/")
def notas(request):

    return render(request, 'home/notas.html')

@login_required(login_url="/login/")
def testvocacional(request):
    
    return render(request, 'home/testvocacional.html')

@login_required(login_url="/login/")
def cuestionario(request):
    
    return render(request,'home/cuestionario.html')