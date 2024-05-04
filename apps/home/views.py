from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render


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

@login_required(login_url="/login/")
def perfil(request):
    segment = 'Perfil.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/perfil.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def alumnos(request):
    segment = 'alumnos.html'
    context = {'segment': segment}


    

    return render(request, 'home/alumnos.html', context)

@login_required(login_url="/login/")
def notas(request):
    segment = 'notas.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/notas.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def testvocacional(request):
    segment = 'testvocacional.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/testvocacional.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def cuestionario(request):
    segment = 'cuestionario.html'
    context = {'segment': segment}

    html_template = loader.get_template('home/cuestionario.html')
    return HttpResponse(html_template.render(context, request))