from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
from django.shortcuts import render


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# paginas
def perfil(request):
    segment = 'Perfil.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/perfil.html')
    return HttpResponse(html_template.render(context, request))

def alumnos(request):
    segment = 'alumnos.html'
    context = {'segment': segment}

    # Hacer una solicitud GET al endpoint del JSON
    response = requests.get('https://randomuser.me/api/?results=2')
    if response.status_code == 200:
        data = response.json()
        alumnos = []
        for result in data['results']:
            alumno = {
                'nombre': result['name']['first'] + ' ' + result['name']['last'],
                'imagen': result['picture']['medium']
            }
            alumnos.append(alumno)
        context['alumnos'] = alumnos
        print(alumnos)  # Comprobación en consola
    

    return render(request, 'home/alumnos.html', context)

def notas(request):
    segment = 'notas.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/notas.html')
    return HttpResponse(html_template.render(context, request))

def testvocacional(request):
    segment = 'testvocacional.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/testvocacional.html')
    return HttpResponse(html_template.render(context, request))

def cuestionario(request):
    segment = 'cuestionario.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/cuestionario.html')
    return HttpResponse(html_template.render(context, request))