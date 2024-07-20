
/* Contado de inicio */
function calcularPuntos() {
    const radios = document.querySelectorAll('input[type="radio"]:checked');
    let aCount = 0;
    let bCount = 0;
    let cCount = 0;
    let dCount = 0;
    let eCount = 0;
/* Decisiones */

    radios.forEach(radio => {
        if (radio.value === 'A') {
            aCount++;
        } else if (radio.value === 'B') {
            bCount++;
        } else if (radio.value === 'C') {
            cCount++;
        } else if (radio.value === 'D') {
            dCount++;
        } else if (radio.value === 'E') {
            eCount++;
        }
    });
/* valor de repuestas */
    const puntosA = aCount * 5;
    const puntosB = bCount * 4;
    const puntosC = cCount * 3;
    const puntosD = dCount * 2;
    const puntosE = eCount * 1;

    const totalPuntos = puntosA + puntosB + puntosC + puntosD + puntosE;
/* resiltado de solo 1 */
    const resultados = document.getElementById('resultados');
    resultados.innerHTML = `Puntos en A: ${puntosA}<br>
                            Puntos en B: ${puntosB}<br>
                            Puntos en C: ${puntosC}<br>
                            Puntos en D: ${puntosD}<br>
                            Puntos en E: ${puntosE}<br>
                            Total de puntos: ${totalPuntos}`;

    const mensaje = document.getElementById('mensaje');
    /* Resultao total */
    if (Determinado === 10) {
        mensaje.innerHTML = 'Personalidad Determinado!';
    } else {
        mensaje.innerHTML = '';
    }
}

function mostrarMensaje() {
    alert('Test enviado');
}
