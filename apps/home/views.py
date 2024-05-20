from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .models import Alumno, AñoCurso
from apps.home.models import Alumno, AñoCurso





@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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
def perfil(request):
    context = {
        'segment': 'perfil' 
    }
    return render(request, 'home/perfil.html', context)

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

    context = {'segment': 'alumnos', 'grupos': grupos}
    return render(request, 'home/seccion.html', context)

@login_required(login_url="/login/")
def notas(request):
    context = {'segment': 'notas'}
    return render(request, 'home/notas.html', context)
=======
def notas(request):
    segment = 'notas.html'
    context = {'segment': segment}
    html_template = loader.get_template('home/notas.html')
    return HttpResponse(html_template.render(context, request))






def testvocacional(request):


    preguntas = [
        {
            'pregunta': '1. ¿Qué tipo de actividades te resultan más interesantes?',
            'respuestas': [
                {'opcion': 'A', 'texto': 'Diseñar y construir estructuras físicas.'},
                {'opcion': 'B', 'texto': 'Cuidar y mejorar la salud de las personas.'},
                {'opcion': 'C', 'texto': 'Enseñar y compartir conocimientos.'},
                {'opcion': 'D', 'texto': 'Gestionar y dirigir proyectos empresariales.'},
                {'opcion': 'E', 'texto': 'Defender los derechos y resolver conflictos legales.'},
                {'opcion': 'F', 'texto': 'Trabajar con números y manejar aspectos financieros.'},
                {'opcion': 'G', 'texto': 'Comprender y ayudar a las personas en su desarrollo emocional.'},
                {'opcion': 'H', 'texto': 'Trabajar con sistemas y tecnologías digitales.'},
                {'opcion': 'I', 'texto': 'Planificar y organizar experiencias de viaje y hospitalidad.'}
            ]
        }
    ]

    context = {'preguntas': preguntas}  # EH aquí está el cambio

    if request.method == 'POST':
        respuestas = request.POST
#verificacion de preguntas
        if all(f'pregunta_{i+1}' in respuestas for i in range(len(preguntas))):
            puntuaciones = {f'pregunta_{i+1}': respuestas.get(f'pregunta_{i+1}') for i in range(len(preguntas))}
#guardado
            puntajes = {
                'Ingeniería Civil': 0,
                'Medicina': 0,
                'Educación': 0,
                'Administración de Empresas': 0,
                'Derecho': 0,
                'Contabilidad y Finanzas': 0,
                'Psicología': 0,
                'Tecnología de la Información': 0,
                'Turismo y Hotelería': 0
            }

            for pregunta, respuesta in puntuaciones.items():
                if respuesta == 'A':
                    puntajes['Ingeniería Civil'] += 1
                elif respuesta == 'B':
                    puntajes['Medicina'] += 1
                elif respuesta == 'C':
                    puntajes['Educación'] += 1
                elif respuesta == 'D':
                    puntajes['Administración de Empresas'] += 1
                elif respuesta == 'E':
                    puntajes['Derecho'] += 1
                elif respuesta == 'F':
                    puntajes['Contabilidad y Finanzas'] += 1
                elif respuesta == 'G':
                    puntajes['Psicología'] += 1
                elif respuesta == 'H':
                    puntajes['Tecnología de la Información'] += 1
                elif respuesta == 'I':
                    puntajes['Turismo y Hotelería'] += 1
#sacarpuntaje mas alto
            max_puntaje = max(puntajes.values())
            max_puntajes = [key for key, value in puntajes.items() if value == max_puntaje]
#empate de vocaciones
            if len(max_puntajes) > 1:
                resultado = "Hay un empate entre varias opciones vocacionales."
            else:
                resultado = f"Tu perfil es: {max_puntajes[0]}"

            context['resultado'] = resultado
        else:
            context['error_message'] = "Debes responder todas las preguntas." #error por noresponder todo

    html_template = loader.get_template('home/testvocacional.html')
    return HttpResponse(html_template.render(context, request))





#///////////////////////////////////////////////////////////////////////////////////////////////////////////



def cuestionario(request):
    context = {'segment': 'cuestionario'}
    return render(request, 'home/cuestionario.html', context)