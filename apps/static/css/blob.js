



window.addEventListener('resize', adjustBackgroundSize);

function adjustBackgroundSize() {
    var background = document.querySelector('.background');
    if (background) {  // Ensure the element exists
        background.style.width = window.innerWidth + 'px';
        background.style.height = window.innerHeight + 'px';
    }
}


adjustBackgroundSize();


//detalles del fondo
var loginbgs = document.querySelectorAll('.loginbg');

loginbgs.forEach(function(loginbg) {
    var maxX = window.innerWidth - loginbg.offsetWidth + 20; // Ajusta el 20 al valor que necesites
    var maxY = window.innerHeight - loginbg.offsetHeight + 20;

    var x = Math.random() * maxX;
    var y = Math.random() * maxY;
    var rotation = Math.random() * 360;
    var scale = 1;

    var speedX = (Math.random() - 0.5) * 6;
    var speedY = (Math.random() - 0.5) * 6;
    var speedRotation = (Math.random() - 0.5) * 6;
    var speedScale = 0.005;

    loginbg.style.transform = `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`;

    function moveRotate() {
        x += speedX;
        y += speedY;
        rotation += speedRotation;
        scale += speedScale;

        if (x < 0 || x > maxX) {
            speedX = -speedX;
        }

        if (y < 0 || y > maxY) {
            speedY = -speedY;
        }

        if (scale < 0.5 || scale > 1.5) {
            speedScale = -speedScale;
        }

        loginbg.style.transform = `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`;

        requestAnimationFrame(moveRotate);
    }

    // Llama a la función al cargar la página para mover y rotar la imagen inicialmente
    moveRotate();
});
//pantalla de carga
document.addEventListener("DOMContentLoaded", function() {
    // Mostramos el contenido con una transición
    const content = document.getElementById('content');
    const loadingScreen = document.getElementById('loading-screen1');

    // Simulamos una carga de recursos
    setTimeout(function() {
        // Añadimos la clase de desvanecimiento desde el borde
        loadingScreen.classList.add('fade-out');
        
        // Mostramos el contenido principal después de la transición
        setTimeout(function() {
            loadingScreen.style.display = 'none';
            content.style.display = 'block';
            
            // Forzamos el reflow para iniciar la transición de opacidad
            content.offsetHeight;
            
            content.style.opacity = '1';
        }, 1500); // Duración de la transición en milisegundos
    }, 3000); // Simulación de 3 segundos de carga
});


document.addEventListener('click', function(event) {
    var isClickInside = document.querySelector('.sidebar').contains(event.target);

    if (!isClickInside) {
        document.querySelector('.sidebar').classList.remove('active');
    }
});

document.querySelector('.burger-button').addEventListener('click', function(event) {
    event.stopPropagation();
    document.querySelector('.sidebar').classList.toggle('active');
});

document.getElementById('edit-profile-btn').addEventListener('click', function() {
    var parentContainer = document.getElementById('parent-container');
    var profileContent = document.querySelector('.profile-content');

    // Toggle display of parentContainer
    if (parentContainer.style.display === 'none' || parentContainer.style.display === '') {
        parentContainer.style.display = 'flex'; // Mostrar el contenedor como flexbox
        parentContainer.style.opacity = '1'; // Establecer opacidad a 1 para hacerlo visible
        parentContainer.style.width = '95%'; // Restablecer el ancho al 100%
        parentContainer.style.transition = 'width 0.4s ease-out, opacity 0.4s ease-out'; // Transición para suavizar la animación al mostrar
    } else {
        parentContainer.style.opacity = '0'; // Establecer opacidad a 0 para desvanecer
        parentContainer.style.transition = 'width 0.4s ease-in, opacity 0.4s ease-in'; // Transición para suavizar la animación al ocultar

        setTimeout(function() {
            parentContainer.style.display = 'none'; // Ocultar el contenedor después de que termine la transición
            parentContainer.style.width = ''; // Restablecer el ancho al valor inicial vacío
        }, 400); // Tiempo de espera que debe coincidir con la duración de la transición en CSS
    }

    // Toggle the expanded class to use full space
    profileContent.classList.toggle('expanded');
    parentContainer.classList.toggle('expanded');
});


// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Inicializa SimpleBar en el contenedor deseado
    const simpleBar = new simpleBar(document.getElementById('parent-container'));
});


