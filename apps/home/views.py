from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
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


    

    return render(request, 'home/alumnos.html', context)

def notas(request):
    preguntas = [
        {
            'pregunta': '1.¿Qué tipo de actividades prefieres?',
            'respuestas': [
                {'opcion': 'A', 'texto': 'Actividades al aire libre'},
                {'opcion': 'B', 'texto': 'Actividades creativas e imaginativas'},
                {'opcion': 'C', 'texto': 'Actividades intelectuales y analíticas'},
                {'opcion': 'D', 'texto': 'Actividades Electronicas'}
            ]
        },
        {
            'pregunta': '2.¿Qué tipo de entorno te gusta más?',
            'respuestas': [
                {'opcion': 'A', 'texto': 'Entornos naturales'},
                {'opcion': 'B', 'texto': 'Entornos artísticos'},
                {'opcion': 'C', 'texto': 'Entornos académicos o de negocios'},
                {'opcion': 'D', 'texto': 'Entornos Tecnologicos'}
            ]
        }
        # Agregar más preguntas aquí si es necesario
    ]

    if request.method == 'POST':
        respuestas = request.POST
        # Verificar si todas las preguntas han sido respondidas
        if all(pregunta['pregunta'] in respuestas for pregunta in preguntas):
            puntuaciones = {pregunta['pregunta']: respuestas.get(pregunta['pregunta']) for pregunta in preguntas}

            # Aquí agregamos la lógica para calcular el resultado basado en las respuestas
            puntaje_artistico = 0
            puntaje_matematico = 0
            puntaje_intelectual = 0
            puntaje_tecnologicos = 0
            
            #arreglar esto mucho codigo 
            
            for pregunta, respuesta in puntuaciones.items():
                if pregunta.startswith('1'):  # Si es la pregunta 1
                    if respuesta == 'A':
                        puntaje_artistico += 1
                    elif respuesta == 'B':
                        puntaje_matematico += 1
                    elif respuesta == 'C':
                        puntaje_intelectual += 1
                    elif respuesta == 'D':
                        puntaje_tecnologicos += 1
            for pregunta, respuesta in puntuaciones.items():
                if pregunta.startswith('2'):  # Si es la pregunta 1
                    if respuesta == 'A':
                        puntaje_artistico += 1
                    elif respuesta == 'B':
                        puntaje_matematico += 1
                    elif respuesta == 'C':
                        puntaje_intelectual += 1
                    elif respuesta == 'D':
                        puntaje_tecnologicos += 1
            # Determina el resultado basado en los puntajes mas vocaciones
            if puntaje_artistico > puntaje_matematico and puntaje_artistico > puntaje_intelectual:
                resultado = "Tu perfil es: Matematico"
            elif puntaje_matematico > puntaje_artistico and puntaje_matematico > puntaje_intelectual:
                resultado = "Tu perfil es: Ciencialo y tecnologico"
            elif puntaje_intelectual > puntaje_artistico and puntaje_intelectual > puntaje_matematico:
                resultado = "Tu perfil es: Necesita dieta"
            elif puntaje_tecnologicos > puntaje_artistico and puntaje_tecnologicos > puntaje_matematico and puntaje_tecnologicos > puntaje_intelectual :
                resultado = "Tu perfil es: Informatica"
            elif puntaje_tecnologicos == puntaje_artistico and puntaje_tecnologicos == puntaje_matematico and puntaje_tecnologicos == puntaje_intelectual :
                resultado = "Tu perfil es: Null"
            else:
                resultado = "Tu perfil es mixto o no se puede determinar claramente"

            context = {'preguntas': preguntas, 'resultado': resultado}
        else:
            error_message = "Debes responder todas las preguntas."
            context = {'preguntas': preguntas, 'error_message': error_message}
    else:
        context = {'preguntas': preguntas}

    segment = 'notas.html'
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