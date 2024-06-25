from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
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
    if load_template in ['seccion', 'notasal', 'testvocacional', 'cuestionario']:
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

notas = {
    "historia": [5, 6],
    "matematicas": [4, 7],
    "ciencias": [6, 3],
    "lenguaje": [4, 6],
    "tecnologia": [4, 7],
    "ingles": [6, 2],
    "religion": [5, 5],
    "artes": [4, 6],
    "musica": [7, 3],
    "educacion fisica": [5, 6],
    "orientacion": [4, 5]
}

materias = list(notas.keys())

@login_required(login_url="/login/")
def analisisnota(request):
    # Calcular estadísticas de las notas
    datos_materias = []
    for materia, notas_materia in notas.items():
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

    promedio_general = round(sum(d["promedio"] for d in datos_materias) / len(datos_materias), 1)
    mejor_materia = max(datos_materias, key=lambda x: x["promedio"])["materia"]
    materias_ordenadas = sorted(datos_materias, key=lambda x: x["promedio"], reverse=True)

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
            notas_area.extend(notas[materia])
        promedio_area = sum(notas_area) / len(notas_area)
        promedios_areas[area] = promedio_area
    return promedios_areas

@login_required(login_url="/login/")
def notasal(request):
    if request.method == 'POST':
        for materia in materias:
            # Actualizar las notas existentes
            for i in range(len(notas[materia])):
                nota_actual = request.POST.get(f'{materia}_evaluacion_{i+1}')
                if nota_actual:
                    notas[materia][i] = float(nota_actual)
            
            # Agregar nueva evaluación si existe
            nueva_evaluacion = request.POST.get(f'{materia}_nueva_evaluacion')
            if nueva_evaluacion:
                notas[materia].append(float(nueva_evaluacion))
        
        return redirect('analisisnota')

    # Generar datos de materias para el contexto
    datos_materias = [{'materia': materia, 'notas': notas[materia]} for materia in materias]
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

@login_required(login_url="/login/")
def cuestionario(request):
    context = {'segment': 'cuestionario'}
    return render(request, 'home/cuestionario.html', context)