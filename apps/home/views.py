from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno, AñoCurso, Asignatura, Calificaciones, Profesor, Calificaciones
from apps.home.models import Alumno, AñoCurso, Asignatura, Calificaciones, Profesor, Calificaciones
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.db.models import Avg



@login_required(login_url="/login/")
def pages(request):
    context = {}
    load_template = request.path.split('/')[-1]

    # Redirigir a la página de administración si la URL es 'admin'
    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))

    # Si la URL corresponde a una vista específica, renderizar esa vista
    if load_template in ['seccion', 'notasal', 'testvocacional', 'cuestionario']:
        return globals()[load_template](request)

    # Redirigir al perfil después de login
    if load_template == '':
        return HttpResponseRedirect(reverse('perfil'))

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
    
    # Obtener el curso asociado con la asignatura
    año_cursado = asignatura.curso
    
    # Filtrar los alumnos por el curso asociado con la asignatura
    alumnos = Alumno.objects.filter(año_cursado=año_cursado)
    
    # Obtener las calificaciones para la asignatura y los alumnos filtrados
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura, alumno__in=alumnos)
    calificaciones_dict = {
        calificacion.alumno.id_alumno: calificacion
        for calificacion in calificaciones
    }
    
    # Asegurarse de que todos los alumnos tengan una entrada en el diccionario de calificaciones
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
    # Obtener el alumno autenticado
    alumno = get_object_or_404(Alumno, user=request.user)
    
    # Obtener el curso del alumno
    curso = alumno.año_cursado
    
    # Obtener todas las asignaturas del curso del alumno
    asignaturas = Asignatura.objects.filter(curso=curso)
    
    # Obtener todas las calificaciones del alumno
    calificaciones = Calificaciones.objects.filter(alumno=alumno)
    
    # Generar datos de materias para el contexto
    datos_materias = []
    for asignatura in asignaturas:
        calificacion = calificaciones.filter(asignatura=asignatura).first()
        datos_materias.append({
            'materia': asignatura.nombre_asig,
            'notas': [
                calificacion.eva1 if calificacion else None,
                calificacion.eva2 if calificacion else None,
                calificacion.eva3 if calificacion else None,
            ]
        })
    
    # Calcular promedios por áreas de estudio
    promedios_areas = calcular_promedios_areas()

    context = {
        'datos_materias': datos_materias,
        'promedios_areas': promedios_areas,
    }

    return render(request, 'home/notasal.html', context)

def testvocacional(request):
    preguntas = [
    {
        'pregunta': '1. ¿Qué tipo de actividades te resultan más interesantes?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Diseñar y construir estructuras físicas.'},
            {'opcion': 'B', 'texto': 'Planificar y organizar experiencias de viaje y hospitalidad.'},
            {'opcion': 'C', 'texto': 'Desarrollar y gestionar sistemas de información.'},
            {'opcion': 'D', 'texto': 'Defender los derechos y resolver conflictos legales.'},
            {'opcion': 'E', 'texto': 'Enseñar y contribuir al desarrollo educativo.'}
        ]
    },
    {
        'pregunta': '2. ¿Qué habilidad te gustaría desarrollar más?',
        'respuestas': [
            {'opcion': 'F', 'texto': 'Capacidad para comprender y ayudar a las personas a nivel emocional.'},
            {'opcion': 'G', 'texto': 'Conocimientos médicos y de salud.'},
            {'opcion': 'H', 'texto': 'Habilidades en el manejo de finanzas y contabilidad.'},
            {'opcion': 'I', 'texto': 'Habilidades de gestión empresarial.'},
            {'opcion': 'A', 'texto': 'Competencias en tecnología y sistemas de información.'}
        ]
    },
    {
        'pregunta': '3. ¿En qué entorno laboral te sientes más cómodo?',
        'respuestas': [
            {'opcion': 'B', 'texto': 'En un despacho de abogados o tribunal.'},
            {'opcion': 'C', 'texto': 'En un salón de clases o institución educativa.'},
            {'opcion': 'D', 'texto': 'En un sitio de construcción al aire libre.'},
            {'opcion': 'E', 'texto': 'En un hotel o agencia de viajes.'},
            {'opcion': 'F', 'texto': 'En un hospital o clínica.'}
        ]
    },
    {
        'pregunta': '4. ¿Qué te motiva más en tus tareas?',
        'respuestas': [
            {'opcion': 'G', 'texto': 'Lograr metas empresariales y de negocios.'},
            {'opcion': 'H', 'texto': 'Manejar aspectos financieros y contables.'},
            {'opcion': 'I', 'texto': 'Innovar en tecnología y sistemas de información.'},
            {'opcion': 'A', 'texto': 'Contribuir al aprendizaje y crecimiento de otros.'},
            {'opcion': 'B', 'texto': 'Ver los resultados tangibles de tu trabajo.'}
        ]
    },
    {
        'pregunta': '5. ¿Qué tipo de proyectos te gustaría liderar?',
        'respuestas': [
            {'opcion': 'C', 'texto': 'Campañas de salud y bienestar.'},
            {'opcion': 'D', 'texto': 'Iniciativas para apoyar la salud mental.'},
            {'opcion': 'E', 'texto': 'Proyectos turísticos y de hospitalidad.'},
            {'opcion': 'F', 'texto': 'Casos legales y de defensa de derechos.'},
            {'opcion': 'G', 'texto': 'Proyectos de construcción e infraestructura.'}
        ]
    },
    {
        'pregunta': '6. ¿Qué aspecto valoras más en una carrera profesional?',
        'respuestas': [
            {'opcion': 'H', 'texto': 'Impacto en la educación y el aprendizaje.'},
            {'opcion': 'I', 'texto': 'Avance y desarrollo tecnológico.'},
            {'opcion': 'A', 'texto': 'Estabilidad financiera.'},
            {'opcion': 'B', 'texto': 'Crecimiento y avance empresarial.'},
            {'opcion': 'C', 'texto': 'Oportunidades de ayudar a otros.'}
        ]
    },
    {
        'pregunta': '7. ¿Qué te gustaría aprender más?',
        'respuestas': [
            {'opcion': 'D', 'texto': 'Normas y leyes actualizadas.'},
            {'opcion': 'E', 'texto': 'Nuevas técnicas de ingeniería.'},
            {'opcion': 'F', 'texto': 'Tendencias en turismo y hospitalidad.'},
            {'opcion': 'G', 'texto': 'Métodos educativos innovadores.'},
            {'opcion': 'H', 'texto': 'Estrategias de apoyo psicológico.'}
        ]
    },
    {
        'pregunta': '8. ¿Cuál de estas responsabilidades te resulta más atractiva?',
        'respuestas': [
            {'opcion': 'I', 'texto': 'Supervisar presupuestos y finanzas.'},
            {'opcion': 'A', 'texto': 'Gestionar sistemas de información.'},
            {'opcion': 'B', 'texto': 'Desarrollar planes de estudio.'},
            {'opcion': 'C', 'texto': 'Cuidar a los pacientes.'},
            {'opcion': 'D', 'texto': 'Defender a clientes en juicios.'}
        ]
    },
    {
        'pregunta': '9. ¿Qué tipo de ambiente de trabajo prefieres?',
        'respuestas': [
            {'opcion': 'E', 'texto': 'Dinámico y al aire libre.'},
            {'opcion': 'F', 'texto': 'Ambiente corporativo y de negocios.'},
            {'opcion': 'G', 'texto': 'Entorno de apoyo emocional.'},
            {'opcion': 'H', 'texto': 'Ambiente de hospitalidad y turismo.'},
            {'opcion': 'I', 'texto': 'Interacción educativa constante.'}
        ]
    },
    {
        'pregunta': '10. ¿Cuál es tu mayor fortaleza profesional?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Innovación tecnológica.'},
            {'opcion': 'B', 'texto': 'Resolución de problemas técnicos.'},
            {'opcion': 'C', 'texto': 'Argumentación y defensa.'},
            {'opcion': 'D', 'texto': 'Empatía y cuidado de los demás.'},
            {'opcion': 'E', 'texto': 'Habilidades de gestión.'}
        ]
    },
    {
        'pregunta': '11. ¿Cómo manejas los desafíos en el trabajo?',
        'respuestas': [
            {'opcion': 'F', 'texto': 'Adaptándome y encontrando nuevas formas de enseñar.'},
            {'opcion': 'G', 'texto': 'Buscando soluciones creativas en la hospitalidad.'},
            {'opcion': 'H', 'texto': 'Analizando datos financieros y ajustando estrategias.'},
            {'opcion': 'I', 'texto': 'Manteniéndome calmado y centrado en el bienestar del paciente.'},
            {'opcion': 'A', 'texto': 'Implementando soluciones tecnológicas.'}
        ]
    },
    {
        'pregunta': '12. ¿Qué te inspira a seguir aprendiendo y creciendo profesionalmente?',
        'respuestas': [
            {'opcion': 'B', 'texto': 'El deseo de innovar y mejorar estructuras.'},
            {'opcion': 'C', 'texto': 'Lograr justicia y equidad.'},
            {'opcion': 'D', 'texto': 'El crecimiento y éxito en los negocios.'},
            {'opcion': 'E', 'texto': 'El impacto positivo en la salud mental.'},
            {'opcion': 'F', 'texto': 'La posibilidad de salvar y mejorar vidas.'}
        ]
    },
    {
        'pregunta': '13. ¿Cómo te gustaría que fuera tu jornada laboral ideal?',
        'respuestas': [
            {'opcion': 'G', 'texto': 'Interactiva y educativa.'},
            {'opcion': 'H', 'texto': 'Centrada en el análisis financiero.'},
            {'opcion': 'I', 'texto': 'Llena de desafíos tecnológicos.'},
            {'opcion': 'A', 'texto': 'Enfocada en la organización de eventos turísticos.'},
            {'opcion': 'B', 'texto': 'Desafiante y centrada en la defensa legal.'}
        ]
    },
    {
        'pregunta': '14. ¿Qué tipo de equilibrio entre trabajo y vida personal buscas?',
        'respuestas': [
            {'opcion': 'C', 'texto': 'Flexibilidad para manejar proyectos.'},
            {'opcion': 'D', 'texto': 'Tiempo para el bienestar emocional.'},
            {'opcion': 'E', 'texto': 'Un equilibrio que permita dedicarse a la enseñanza y el desarrollo personal.'},
            {'opcion': 'F', 'texto': 'Balance con tiempo para la innovación tecnológica.'},
            {'opcion': 'G', 'texto': 'Compatibilidad con el crecimiento profesional.'}
        ]
    },
    {
        'pregunta': '15. ¿Cuál es tu principal objetivo a largo plazo en tu carrera?',
        'respuestas': [
            {'opcion': 'H', 'texto': 'Ser reconocido por mis contribuciones a la salud.'},
            {'opcion': 'I', 'texto': 'Convertirme en un líder en el sector turístico.'},
            {'opcion': 'A', 'texto': 'Ser un abogado destacado y respetado.'},
            {'opcion': 'B', 'texto': 'Innovar en métodos educativos.'},
            {'opcion': 'C', 'texto': 'Convertirme en un líder en ingeniería.'}
        ]
    },
    {
        'pregunta': '16. ¿Qué aspiraciones tienes en tu carrera profesional?',
        'respuestas': [
            {'opcion': 'D', 'texto': 'Un experto en sistemas de información.'},
            {'opcion': 'E', 'texto': 'Un profesional de la salud experimentado.'},
            {'opcion': 'F', 'texto': 'Un educador innovador.'},
            {'opcion': 'G', 'texto': 'Un experto en técnicas de construcción.'},
            {'opcion': 'H', 'texto': 'Un empresario exitoso.'}
        ]
    },
    {
        'pregunta': '17. ¿Qué valores son importantes para ti en un equipo de trabajo?',
        'respuestas': [
            {'opcion': 'I', 'texto': 'Basada en el análisis y resolución de problemas financieros.'},
            {'opcion': 'A', 'texto': 'De apoyo y con un enfoque en el bienestar de todos.'},
            {'opcion': 'B', 'texto': 'Intercambio constante de ideas y metodologías.'},
            {'opcion': 'C', 'texto': 'Profesional y orientada a objetivos.'},
            {'opcion': 'D', 'texto': 'Basada en la confianza y la ética.'}
        ]
    },
    {
        'pregunta': '18. ¿Qué habilidades consideras esenciales para un líder?',
        'respuestas': [
            {'opcion': 'E', 'texto': 'Capacidad para guiar e innovar en tecnología.'},
            {'opcion': 'F', 'texto': 'Habilidad para cuidar y motivar al equipo.'},
            {'opcion': 'G', 'texto': 'Competencia para inspirar y enseñar.'},
            {'opcion': 'H', 'texto': 'Facultad para tomar decisiones estratégicas.'},
            {'opcion': 'I', 'texto': 'Integridad y justicia en todas las acciones.'}
        ]
     },
    {
        'pregunta': '19. ¿Qué tipo de proyectos de investigación te interesan más?',
        'respuestas': [
            {'opcion': 'A', 'texto': 'Investigación en inteligencia artificial y sistemas de información.'},
            {'opcion': 'D', 'texto': 'Investigación en leyes y políticas públicas.'},
            {'opcion': 'F', 'texto': 'Investigación en métodos educativos innovadores.'},
            {'opcion': 'H', 'texto': 'Investigación en estrategias de salud mental.'}
        ]
    },
    {
        'pregunta': '20. ¿En qué área te gustaría especializarte a largo plazo?',
        'respuestas': [
            {'opcion': 'B', 'texto': 'Gestión y desarrollo de proyectos turísticos.'},
            {'opcion': 'C', 'texto': 'Desarrollo de nuevas técnicas de ingeniería.'},
            {'opcion': 'E', 'texto': 'Gestión y administración en el sector salud.'},
            {'opcion': 'G', 'texto': 'Planificación y diseño de infraestructuras.'}
        ]
    }
]


    context = {'preguntas': preguntas}

    if request.method == 'POST':
        respuestas = request.POST
        if all(f'pregunta_{i+1}' in respuestas for i in range(len(preguntas))):
            puntuaciones = {f'pregunta_{i+1}': respuestas.get(f'pregunta_{i+1}') for i in range(len(preguntas))}
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

            max_puntaje = max(puntajes.values())
            max_puntajes = [key for key, value in puntajes.items() if value == max_puntaje]

            if len(max_puntajes) > 1:
                resultado = f"Hay un empate entre las opciones vocacionales: {', '.join(max_puntajes)}"
            else:
                resultado = f"Tu perfil es: {max_puntajes[0]}"

            context['resultado'] = resultado
        else:
            context['error_message'] = "Debes responder todas las preguntas."

    html_template = loader.get_template('home/testvocacional.html')
    return HttpResponse(html_template.render(context, request))

def cuestionario(request):
    context = {'segment': 'cuestionario'}
    return render(request, 'home/cuestionario.html', context)

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

