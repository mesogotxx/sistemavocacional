from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno, AñoCurso, Asignatura, Calificaciones, Profesor, Calificaciones
from apps.home.models import Alumno, AñoCurso, Asignatura, Calificaciones, Profesor, Calificaciones
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.db.models import Avg
=======
from django.shortcuts import render, redirect,get_object_or_404
from .models import Alumno, AñoCurso
from apps.home.models import Alumno, AñoCurso
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event
from .forms import EventForm
from django.views.decorators.csrf import csrf_exempt
>>>>>>> 58d0b0a97cd6fba154d3c77d543d8d5ca6caea11




@login_required(login_url="/login/")
def pages(request):
    context = {}
<<<<<<< HEAD
    load_template = request.path.split('/')[-1]
    
=======
    load_template = request.path.split('index/')[-1]

>>>>>>> 58d0b0a97cd6fba154d3c77d543d8d5ca6caea11
    # Redirigir a la página de administración si la URL es 'admin'
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    # Si la URL corresponde a una vista específica, renderizar esa vista
    if load_template in ['seccion', 'notasal', 'testvocacional', 'cuestionario']:
        return globals()[load_template](request)

    # Si la URL no coincide con ninguna vista específica, cargar la plantilla HTML correspondiente
    try:
        html_template = loader.get_template('home/index' + load_template + '.html')
        return HttpResponse(html_template.render(context, request))

    # Manejar el caso en que no se encuentre la plantilla
    except TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    # Manejar otros errores
    except Exception as e:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def perfil(request):
    tipo_usuario = None
    perfil_usuario = None
    asignaturas = None
    
    if hasattr(request.user, 'alumno'):
        tipo_usuario = 'alumno'
        perfil_usuario = request.user.alumno
    elif hasattr(request.user, 'profesor'):
        tipo_usuario = 'profesor'
        perfil_usuario = request.user.profesor
        asignaturas = perfil_usuario.asignatura_set.all()
    
    context = {
        'segment': 'perfil',
        'tipo_usuario': tipo_usuario,
        'perfil_usuario': perfil_usuario,
        'asignaturas': asignaturas
    }
    return render(request, 'home/perfil.html', context)

@login_required(login_url="/login/")
def alumnos(request, asignatura_id):
    asignatura = Asignatura.objects.get(id_asignatura=asignatura_id)
    alumnos = Alumno.objects.all()
    
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura)
    calificaciones_dict = {
        calificacion.alumno.id_alumno: calificacion
        for calificacion in calificaciones
    }
    
    for alumno in alumnos:
        if alumno.id_alumno not in calificaciones_dict:
            calificaciones_dict[alumno.id_alumno] = Calificaciones(
                alumno=alumno,
                asignatura=asignatura,
                eva1=None,
                eva2=None,
                eva3=None,
            )
    
    context = {
        'asignatura': asignatura,
        'alumnos': alumnos,
        'calificaciones_dict': calificaciones_dict,
    }
    return render(request, 'home/alumnos.html', context)

@login_required(login_url="/login/")
def guardar_calificaciones(request):
    if request.method == 'POST':
        asignatura_id = request.POST.get('asignatura_id')
        asignatura = Asignatura.objects.get(id_asignatura=asignatura_id)

        for alumno_id in request.POST:
            if alumno_id.startswith('eva1_'):
                alumno_id = alumno_id.split('_')[1]
                eva1 = request.POST.get(f'eva1_{alumno_id}')
                eva2 = request.POST.get(f'eva2_{alumno_id}')
                eva3 = request.POST.get(f'eva3_{alumno_id}')
                alumno = Alumno.objects.get(id_alumno=alumno_id)
                
                # Actualiza o crea las calificaciones
                calificaciones, created = Calificaciones.objects.update_or_create(
                    alumno=alumno,
                    asignatura=asignatura,
                    defaults={
                        'eva1': eva1 if eva1 else None,
                        'eva2': eva2 if eva2 else None,
                        'eva3': eva3 if eva3 else None,
                    }
                )

    return redirect('alumnos', asignatura_id=asignatura_id)

@login_required(login_url="/login/")
def seccion(request):
    profesor = Profesor.objects.get(user=request.user)
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
            grupos['Primeros medios'].append(año)
        elif nombre.startswith('Segundo medio'):
            grupos['Segundos medios'].append(año)
        elif nombre.startswith('Tercero medio'):
            grupos['Terceros medios'].append(año)
        elif nombre.startswith('Cuarto medio'):
            grupos['Cuartos medios'].append(año)

    context = {
        'segment': 'alumnos',
        'grupos': grupos,
        'profesor': profesor
    }

    return render(request, 'home/seccion.html', context)


@login_required(login_url="/login/")
def analisisnota(request):
    # Obtén el alumno logeado
    alumno = request.user.alumno
    
    # Filtra las calificaciones para el alumno logeado
    calificaciones = Calificaciones.objects.filter(alumno=alumno)
    
    # Agrupa las calificaciones por materia
    notas_materias = {}
    for calificacion in calificaciones:
        asignatura = calificacion.asignatura
        materia = asignatura.nombre_asig
        notas_materias.setdefault(materia, [])
        notas_materias[materia].extend([
            calificacion.eva1 if calificacion.eva1 is not None else 0,
            calificacion.eva2 if calificacion.eva2 is not None else 0,
            calificacion.eva3 if calificacion.eva3 is not None else 0
        ])
    
    # Calcular estadísticas de las notas
    datos_materias = []
    for materia, notas_materia in notas_materias.items():
        if notas_materia:  # Verifica si hay notas disponibles
            promedio = round(sum(notas_materia) / len(notas_materia), 1)
            tendencia = "sin cambios"
            for j in range(1, len(notas_materia)):
                if notas_materia[j] > notas_materia[j - 1]:
                    tendencia = "mejorando"
                elif notas_materia[j] < notas_materia[j - 1]:
                    tendencia = "empeorando"
                    break
            datos_materias.append({
                "materia": materia,
                "notas": notas_materia,
                "promedio": promedio,
                "tendencia": tendencia
            })

    if datos_materias:  # Verifica si hay datos para calcular el promedio general
        promedio_general = round(sum(d["promedio"] for d in datos_materias) / len(datos_materias), 1)
        mejor_materia = max(datos_materias, key=lambda x: x["promedio"])["materia"]
        materias_ordenadas = sorted(datos_materias, key=lambda x: x["promedio"], reverse=True)
    else:
        promedio_general = 0
        mejor_materia = None
        materias_ordenadas = []

    context = {
        'datos_materias': datos_materias,
        'promedio_general': promedio_general,
        'mejor_materia': mejor_materia,
        'materias_ordenadas': materias_ordenadas,
    }
    return render(request, 'home/analisisnota.html', context)

# Relación de materias con áreas de estudio
areas_estudio = {
    "negocios": ["historia", "matematicas", "lenguaje", "ingles"],
    "construccion": ["matematicas", "tecnologia"],
    "informatica": ["matematicas", "tecnologia", "ingles"],
    "medicina": ["ciencias", "lenguaje"],
    "mecanica": ["tecnologia", "matematicas"],
    "electricidad": ["tecnologia", "matematicas", "ciencias"],
    "prevencion_riesgos": ["ciencias", "tecnologia"]
}

def calcular_promedios_areas():
    promedios_areas = {}
    
    for area, materias_area in areas_estudio.items():
        notas_area = []
        
        for materia in materias_area:
            # Obtener la asignatura correspondiente
            asignatura = Asignatura.objects.filter(nombre_asig=materia).first()
            
            if asignatura:
                # Obtener las calificaciones para esta asignatura
                calificaciones = Calificaciones.objects.filter(asignatura=asignatura)
                
                # Recoger todas las notas de la asignatura
                for calificacion in calificaciones:
                    if calificacion.eva1 is not None:
                        notas_area.append(calificacion.eva1)
                    if calificacion.eva2 is not None:
                        notas_area.append(calificacion.eva2)
                    if calificacion.eva3 is not None:
                        notas_area.append(calificacion.eva3)
        
        # Calcular el promedio del área
        if notas_area:
            promedio_area = sum(notas_area) / len(notas_area)
        else:
            promedio_area = 0  # O un valor que indique que no hay notas disponibles
        
        promedios_areas[area] = promedio_area
    
    return promedios_areas

@login_required(login_url="/login/")
def notasal(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    
    # Obtener todas las calificaciones del alumno
    calificaciones = Calificaciones.objects.filter(alumno=alumno)
    
    # Generar datos de materias para el contexto
    datos_materias = []
    for calificacion in calificaciones:
        datos_materias.append({
            'materia': calificacion.asignatura.nombre_asig,
            'notas': [calificacion.eva1, calificacion.eva2, calificacion.eva3]
        })
    
    # Calcular promedios y otros datos si es necesario
    promedios_areas = calcular_promedios_areas()

    context = {
        'datos_materias': datos_materias,
        'promedios_areas': promedios_areas,
    }

    return render(request, 'home/notasal.html', context)

@login_required(login_url="/login/")
def testvocacional(request):


    preguntas = [
    {
        'pregunta': '1. ¿Qué tipo de actividades te resultan más interesantes?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Diseñar y construir estructuras físicas.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Cuidar y mejorar la salud de las personas.'},  # Medicina
            {'opcion': 'C', 'texto': 'Enseñar y compartir conocimientos.'},  # Educación
            {'opcion': 'D', 'texto': 'Gestionar y dirigir proyectos empresariales.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Defender los derechos y resolver conflictos legales.'},  # Derecho
            {'opcion': 'F', 'texto': 'Trabajar con números y manejar aspectos financieros.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Comprender y ayudar a las personas en su desarrollo emocional.'},  # Psicología
            {'opcion': 'H', 'texto': 'Trabajar con sistemas y tecnologías digitales.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Planificar y organizar experiencias de viaje y hospitalidad.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '2. ¿Qué habilidad te gustaría desarrollar más?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Habilidad para diseñar planos y cálculos estructurales.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Capacidad para diagnosticar y tratar enfermedades.'},  # Medicina
            {'opcion': 'C', 'texto': 'Competencia para impartir clases y desarrollar material educativo.'},  # Educación
            {'opcion': 'D', 'texto': 'Habilidad para liderar y gestionar equipos.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Destreza para argumentar y defender casos jurídicos.'},  # Derecho
            {'opcion': 'F', 'texto': 'Aptitud para analizar y gestionar recursos financieros.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Capacidad para escuchar y ayudar a las personas.'},  # Psicología
            {'opcion': 'H', 'texto': 'Conocimiento en programación y desarrollo de software.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Habilidad para coordinar eventos y experiencias turísticas.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '3. ¿En qué entorno laboral te sientes más cómodo?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'En una obra de construcción.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'En un hospital o clínica.'},  # Medicina
            {'opcion': 'C', 'texto': 'En un aula o centro educativo.'},  # Educación
            {'opcion': 'D', 'texto': 'En una oficina corporativa.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'En un despacho de abogados.'},  # Derecho
            {'opcion': 'F', 'texto': 'En una firma de contabilidad.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'En una consulta psicológica.'},  # Psicología
            {'opcion': 'H', 'texto': 'En una empresa de tecnología.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'En una agencia de viajes o hotel.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '4. ¿Qué te motiva más en tu trabajo?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Ver resultados tangibles en las estructuras que construyo.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Salvar y mejorar vidas.'},  # Medicina
            {'opcion': 'C', 'texto': 'Ver a mis alumnos aprender y crecer.'},  # Educación
            {'opcion': 'D', 'texto': 'Alcanzar metas y objetivos empresariales.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Lograr justicia y defender los derechos de las personas.'},  # Derecho
            {'opcion': 'F', 'texto': 'Manejar y hacer crecer el capital financiero.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Ayudar a las personas a superar sus problemas.'},  # Psicología
            {'opcion': 'H', 'texto': 'Innovar y mejorar sistemas tecnológicos.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Crear experiencias memorables para las personas.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '5. ¿Qué tipo de proyectos te gustaría liderar?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Proyectos de infraestructura y construcción.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Investigaciones médicas y tratamientos innovadores.'},  # Medicina
            {'opcion': 'C', 'texto': 'Programas educativos y de formación.'},  # Educación
            {'opcion': 'D', 'texto': 'Estrategias de crecimiento empresarial.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Casos legales y reformas judiciales.'},  # Derecho
            {'opcion': 'F', 'texto': 'Proyectos de auditoría y consultoría financiera.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Iniciativas de bienestar emocional y mental.'},  # Psicología
            {'opcion': 'H', 'texto': 'Desarrollo de aplicaciones y sistemas tecnológicos.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Eventos y actividades turísticas.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '6. ¿Qué aspecto valoras más en una carrera profesional?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'La oportunidad de crear e innovar en construcciones.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'La posibilidad de salvar y mejorar vidas.'},  # Medicina
            {'opcion': 'C', 'texto': 'La oportunidad de influir y educar a las nuevas generaciones.'},  # Educación
            {'opcion': 'D', 'texto': 'El potencial de crecimiento y liderazgo.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'La capacidad de defender derechos y lograr justicia.'},  # Derecho
            {'opcion': 'F', 'texto': 'La estabilidad y crecimiento financiero.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'El impacto positivo en la salud mental de las personas.'},  # Psicología
            {'opcion': 'H', 'texto': 'El constante avance y cambio tecnológico.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'La interacción y servicio a los demás.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '7. ¿Qué tipo de problemas disfrutas resolver?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Problemas de diseño y construcción.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Problemas de salud y diagnóstico médico.'},  # Medicina
            {'opcion': 'C', 'texto': 'Dificultades de aprendizaje y enseñanza.'},  # Educación
            {'opcion': 'D', 'texto': 'Desafíos en la gestión empresarial.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Conflictos legales y disputas judiciales.'},  # Derecho
            {'opcion': 'F', 'texto': 'Problemas financieros y contables.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Problemas emocionales y psicológicos.'},  # Psicología
            {'opcion': 'H', 'texto': 'Problemas técnicos y de programación.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Desafíos en la organización de eventos y viajes.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '8. ¿Qué te gustaría aprender más?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Técnicas avanzadas de ingeniería y construcción.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Nuevas tecnologías y tratamientos médicos.'},  # Medicina
            {'opcion': 'C', 'texto': 'Métodos innovadores de enseñanza.'},  # Educación
            {'opcion': 'D', 'texto': 'Estrategias de administración y liderazgo.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Normas y leyes actualizadas.'},  # Derecho
            {'opcion': 'F', 'texto': 'Técnicas de auditoría y gestión financiera.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Nuevas terapias y enfoques psicológicos.'},  # Psicología
            {'opcion': 'H', 'texto': 'Lenguajes de programación y desarrollo de software.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Tendencias y gestión en turismo y hospitalidad.'}  # Turismo y Hotelería
        ]
    },
    {
        'pregunta': '9. ¿Cuál de estas responsabilidades te resulta más atractiva?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Supervisar la construcción de edificios y obras públicas.'},  # Ingeniería Civil
            {'opcion': 'B', 'texto': 'Atender a pacientes y gestionar su tratamiento.'},  # Medicina
            {'opcion': 'C', 'texto': 'Preparar y dar clases a estudiantes.'},  # Educación
            {'opcion': 'D', 'texto': 'Planificar y dirigir estrategias empresariales.'},  # Administración de Empresas
            {'opcion': 'E', 'texto': 'Asesorar y representar a clientes en temas legales.'},  # Derecho
            {'opcion': 'F', 'texto': 'Gestionar presupuestos y análisis financiero.'},  # Contabilidad y Finanzas
            {'opcion': 'G', 'texto': 'Realizar terapias y asesorar a personas con problemas emocionales.'},  # Psicología
            {'opcion': 'H', 'texto': 'Desarrollar y mantener sistemas informáticos.'},  # Tecnología de la Información
            {'opcion': 'I', 'texto': 'Organizar eventos y coordinar servicios turísticos.'}  # Turismo y Hotelería
        ]}]

    context = {'preguntas': preguntas}

    if request.method == 'POST':
        respuestas = {key: request.POST[key] for key in request.POST.keys() if key.startswith('pregunta_')}
        print(respuestas)  # Depuración: muestra todas las respuestas recibidas

        # Verificación de preguntas
        if all(f'pregunta_{i+1}' in respuestas for i in range(len(preguntas))):
            puntuaciones = {
                f'pregunta_{i+1}': respuestas.get(f'pregunta_{i+1}') for i in range(len(preguntas))
            }
            # Depuración: muestra las puntuaciones obtenidas
            print(puntuaciones)

            # Cálculo de puntajes y determinación del resultado
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

            # Determinar la vocación con mayor puntaje
            max_puntaje = max(puntajes.values())
            max_vocaciones = [key for key, value in puntajes.items() if value == max_puntaje]

            # Preparar el resultado
            if len(max_vocaciones) > 1:
                resultado = "Hay un empate entre varias opciones vocacionales."
            else:
                resultado = f"Tu perfil es: {max_vocaciones[0]}"

            # Devolver el resultado según sea necesario (JSON o HTML)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'resultado': resultado})
            else:
                context['resultado'] = resultado
                html_template = loader.get_template('home/testvocacional.html')
                return HttpResponse(html_template.render(context, request))

        else:
            # Error por no responder todas las preguntas
            error_message = "Debes responder todas las preguntas."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error_message': error_message}, status=400)
            else:
                context['error_message'] = error_message
                html_template = loader.get_template('home/testvocacional.html')
                return HttpResponse(html_template.render(context, request))

    # Si es una solicitud GET inicial, renderizar la página con el formulario
    return render(request, 'home/testvocacional.html', context)

@login_required(login_url="/login/")
def cuestionario(request):
    context = {'segment': 'cuestionario'}
    return render(request, 'home/cuestionario.html', context)

<<<<<<< HEAD
@login_required(login_url="/login/")
def asignaturas(request, id_añocurso):
    profesor_logueado = request.user.profesor
    
    # Obtener el objeto AñoCurso basado en el id proporcionado
    año_curso = AñoCurso.objects.get(id_añocurso=id_añocurso)
    
    # Filtra las asignaturas por el profesor logueado y el curso especificado
    asignaturas = Asignatura.objects.filter(profesor=profesor_logueado, curso_id=id_añocurso)
    
    context = {
        'asignaturas': asignaturas,
        'año_curso': año_curso
    }
    return render(request, 'home/asignaturas.html', context)

=======

@login_required(login_url="/login/")
def index(request):
    # Obtención de noticias
    api_key = 'pub_48808b16ca195b4bdea2450851b8a1ff1d990'
    base_url = 'https://newsdata.io/api/1/news'
    query_params = {
        'apikey': api_key,
        'country': 'cl',
        'q': 'chile',
        'size': 10  # Ajusta este parámetro para cambiar la cantidad de noticias por página
    }
    
    response = requests.get(base_url, params=query_params)
    
    if response.status_code == 200:
        data = response.json().get('results', [])  # Obtén los resultados de la API
    else:
        data = []
    
    paginator = Paginator(data, 5)  # Divide los resultados en páginas, 5 resultados por página
    page_number = request.GET.get('page')  # Obtén el número de página actual
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Si el número de página no es un entero, muestra la primera página
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Si la página está vacía, muestra la última página

    # Manejo del formulario de eventos
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            if request.is_ajax():
                return JsonResponse({
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                })
            return redirect('index')  # Redirige a la misma página para actualizar la lista de eventos
    else:
        form = EventForm()
    
    events = Event.objects.all()

    # Combina los datos de noticias y eventos en el contexto
    context = {
        'news': page_obj,  # Paginador de noticias
        'events': events,  # Lista de eventos
        'form': form,      # Formulario para agregar eventos
    }
    
    return render(request, 'home/index.html', context)





@login_required(login_url="/login/")
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('index')  # Redirige a la página principal después de eliminar
    return redirect('index')


@csrf_exempt
@login_required(login_url="/login/")
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        title = request.POST.get('title')
        description = request.POST.get('description')

        try:
            event = Event.objects.get(id=event_id)
            event.title = title
            event.description = description
            event.save()

            return JsonResponse({
                'id': event.id,
                'title': event.title,
                'description': event.description
            })
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)
>>>>>>> 58d0b0a97cd6fba154d3c77d543d8d5ca6caea11
