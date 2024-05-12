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

            # Inicializar puntajes
            puntajes = {
                'Ingeniería Civil': 0, #Ingeniería Civil
                'Medicina': 0, #Medicina
                'Educación': 0, #Educación
                'Administración de Empresas': 0, #Administración de Empresas
                'Derecho': 0, #Derecho
                'Contabilidad y Finanzas': 0, #Contabilidad y Finanzas
                'Psicologia': 0, #Psicologia
                'Tecnología de la Información': 0, #Tecnología de la Información
                'Turismo y Hotelería': 0 #Turismo y Hotelería
                    #MAS!!               
            }

            # Contar puntajes
            for pregunta, respuesta in puntuaciones.items():
                if respuesta == 'A':
                    puntajes['Ingeniería Civil'] += 1
                elif respuesta == 'B':
                    puntajes['Medicina'] += 1
                elif respuesta == 'C':
                    puntajes['Educación'] += 1
                elif respuesta == 'D':
                    puntajes['Derecho'] += 1
                elif respuesta == 'D':
                    puntajes['Contabilidad y Finanzas'] += 1
                elif respuesta == 'D':
                    puntajes['Psicologia'] += 1
                elif respuesta == 'D':
                    puntajes['Tecnología de la Información'] += 1
                elif respuesta == 'D':
                    puntajes['Turismo y Hotelería'] += 1

            # Determinar el resultado
            max_puntaje = max(puntajes.values()) #Aqui sacas el puntaje maximo
            max_puntajes = [key for key, value in puntajes.items() if value == max_puntaje]

            if len(max_puntajes) > 1:  # Si hay empate entre varios perfiles
                resultado = "Tu perfil es mixto o no se puede determinar claramente"
            else:
                resultado = "Tu perfil es: " + max_puntajes[0]

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