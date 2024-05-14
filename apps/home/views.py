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
    #PREGUNTA = LISTA que macena la pregunta y las posibles repuesta dentro de una letra
    preguntas = [ 
    {
        'pregunta': '1. ¿Qué tipo de actividades te resultan más interesantes?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Diseñar y construir estructuras físicas.'},                           # OPCION :Es una letra que identifica la opción de respuesta
            {'opcion': 'B', 'texto': 'Cuidar y mejorar la salud de las personas.'},                         #TEXTO: Es el texto que describe la opción de respuesta
            {'opcion': 'C', 'texto': 'Enseñar y compartir conocimientos.'},
            {'opcion': 'D', 'texto': 'Gestionar y dirigir proyectos empresariales.'},
            {'opcion': 'E', 'texto': 'Defender los derechos y resolver conflictos legales.'},
            {'opcion': 'F', 'texto': 'Trabajar con números y manejar aspectos financieros.'},
            {'opcion': 'G', 'texto': 'Comprender y ayudar a las personas en su desarrollo emocional.'},
            {'opcion': 'H', 'texto': 'Trabajar con sistemas y tecnologías digitales.'},
            {'opcion': 'I', 'texto': 'Planificar y organizar experiencias de viaje y hospitalidad.'}
        ]
    },
    {
        'pregunta': '2. ¿Qué habilidades consideras que posees o te gustaría desarrollar?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Habilidad para el diseño y la construcción.'},
            {'opcion': 'B', 'texto': 'Empatía y habilidades comunicativas.'},
            {'opcion': 'C', 'texto': 'Paciencia y capacidad para enseñar.'},
            {'opcion': 'D', 'texto': 'Habilidades de liderazgo y gestión.'},
            {'opcion': 'E', 'texto': 'Argumentación y análisis crítico.'},
            {'opcion': 'F', 'texto': 'Destreza numérica y atención al detalle.'},
            {'opcion': 'G', 'texto': 'Escucha activa y comprensión emocional.'},
            {'opcion': 'H', 'texto': 'Interés y habilidad para la informática.'},
            {'opcion': 'I', 'texto': 'Gusto por la atención al cliente y la planificación.'}
        ]
    },
    {
        'pregunta': '3. ¿Qué ambiente de trabajo prefieres?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Trabajar en obras de construcción o laboratorios.'},
            {'opcion': 'B', 'texto': 'Ambientes hospitalarios o consultorios médicos.'},
            {'opcion': 'C', 'texto': 'Aulas de clases o espacios educativos.'},
            {'opcion': 'D', 'texto': 'Oficinas corporativas o salas de juntas.'},
            {'opcion': 'E', 'texto': 'Despachos legales o salas de audiencia.'},
            {'opcion': 'F', 'texto': 'Oficinas financieras o departamentos contables.'},
            {'opcion': 'G', 'texto': 'Consultorios psicológicos o centros de atención.'},
            {'opcion': 'H', 'texto': 'Empresas de tecnología o startups.'},
            {'opcion': 'I', 'texto': 'Hoteles, agencias de viaje o destinos turísticos.'}
        ]
    },
    {
    'pregunta': '4. ¿Qué tipo de proyectos te gustaría liderar?',
    'respuestas': [
        {'opcion': 'A', 'texto': 'Proyectos de infraestructura y construcción.'},
        {'opcion': 'B', 'texto': 'Proyectos de investigación médica o de salud.'},
        {'opcion': 'C', 'texto': 'Proyectos educativos o de capacitación.'},
        {'opcion': 'D', 'texto': 'Proyectos empresariales o de innovación.'},
        {'opcion': 'E', 'texto': 'Proyectos legales o de defensa.'},
        {'opcion': 'F', 'texto': 'Proyectos financieros o de inversión.'},
        {'opcion': 'G', 'texto': 'Proyectos de bienestar psicológico o social.'},
        {'opcion': 'H', 'texto': 'Proyectos de desarrollo de software o tecnológicos.'},
        {'opcion': 'I', 'texto': 'Proyectos turísticos o de hospitalidad.'}
    ]
},
{
    'pregunta': '5. ¿Qué tipo de desafíos te motivan más?',
    'respuestas': [
        {'opcion': 'A', 'texto': 'Desafíos técnicos y de ingeniería.'},
        {'opcion': 'B', 'texto': 'Desafíos médicos o de atención sanitaria.'},
        {'opcion': 'C', 'texto': 'Desafíos educativos o de enseñanza.'},
        {'opcion': 'D', 'texto': 'Desafíos empresariales o de gestión.'},
        {'opcion': 'E', 'texto': 'Desafíos legales o judiciales.'},
        {'opcion': 'F', 'texto': 'Desafíos financieros o económicos.'},
        {'opcion': 'G', 'texto': 'Desafíos emocionales o psicológicos.'},
        {'opcion': 'H', 'texto': 'Desafíos tecnológicos o de desarrollo.'},
        {'opcion': 'I', 'texto': 'Desafíos relacionados con la hospitalidad y el turismo.'}
    ]
}
    
    # Agregar más preguntas aquí si es necesario
]

    if request.method == 'POST':
        respuestas = request.POST
        # Verificar si todas las preguntas han sido respondidas
        if all(pregunta['pregunta'] in respuestas for pregunta in preguntas):
            puntuaciones = {pregunta['pregunta']: respuestas.get(pregunta['pregunta']) for pregunta in preguntas}

            # INICIO DE PUNTAJE de vocaciones 
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

            # SUMAR PUNTAJE Y DEFINIR VARIABLE
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

            # Determinar el resultado basado en el valor mas alto :D
            max_puntaje = max(puntajes.values()) #Aqui sacas el puntaje maximo//// max_puntaje solo alamcena el valor mas alto 
            #EN "max_puntajes" con S crea una lista de claves que tienen el mismo puntaje máximo. por si hay un empate 
            max_puntajes = [key for key, value in puntajes.items() if value == max_puntaje]  #key = diccionario de puntaje value = representa los valores asociados a esas claves  
                                                                                            #"yo del futuro" me refiero al diccionario de python 
                                                                                            #el max_puntaje pasa a = value
            if len(max_puntajes) > 1:  # Si hay empate entre varios vocaciones // len = para la longitud de la colección "vocaciones"
                resultado = "Hay un empate!!!!" #posible mejora aqui
            else:
                resultado = "Tu perfil es: " + max_puntajes[0]

            context = {'preguntas': preguntas, 'resultado': resultado}
        else:
            error_message = "Debes responder todas las preguntas."  #Arreglar esto
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