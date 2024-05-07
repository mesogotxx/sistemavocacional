function calcularPorcentaje() {
    const radios = document.querySelectorAll('input[type="radio"]:checked');
    let siCount = 0;
    let noCount = 0;
/* Decisiones */
    radios.forEach(radio => {
        if (radio.value === 'Sí') {
            siCount++;
        } else if (radio.value === 'No') {
            noCount++;
        }
    });
   /* porcentaje segun cantidad de preguntas */
    const total = siCount + noCount;
    const porcentajeSi = (siCount / total) * 100;
    const porcentajeNo = (noCount / total) * 100;
/* Aqui muestra el resultado  */
    const resultados = document.getElementById('resultados');
    resultados.innerHTML = `Porcentaje de respuestas Sí: ${porcentajeSi.toFixed(2)}%<br>
                            Porcentaje de respuestas No: ${porcentajeNo.toFixed(2)}%`;

    /* RESULTADO  */
    const mensaje = document.getElementById('mensaje');                        
    if (porcentajeSi === 50) {
        mensaje.innerHTML = 'Personalidad Determinado!';
    } else {
        mensaje.innerHTML = '';
    }


/* la alerta de enviado 'hay que mejorar para que quede mas bonito' */
    mostrarMensaje();
}

function mostrarMensaje() {
    alert('Test enviado');
    
}
