const menu = document.querySelector('.hamburguesa');
const navegacion = document.querySelector('.navegacion');
const imagenes = document.querySelectorAll('img');

document.addEventListener('DOMContentLoaded', () => {
  eventos();
});

const eventos = () => {
  menu.addEventListener('click', abrirMenu);
};

const abrirMenu = () => {
  navegacion.classList.remove('ocultar');
  botonCerrar();
};

const botonCerrar = () => {
  const btnCerrar = document.createElement('p');
  const overlay = document.createElement('div');
  overlay.classList.add('pantalla-completa');
  const body = document.querySelector('body');
  if (document.querySelectorAll('.pantalla-completa').length > 0) return;
  body.appendChild(overlay);
  btnCerrar.textContent = 'x';
  btnCerrar.classList.add('btn-cerrar');
  navegacion.appendChild(btnCerrar);
  cerrarMenu(btnCerrar, overlay);
};

const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const imagen = entry.target;
      imagen.src = imagen.dataset.src;
      observer.unobserve(imagen);
    }
  });
});

imagenes.forEach(imagen => {
  observer.observe(imagen);
});

const cerrarMenu = (boton, overlay) => {
  boton.addEventListener('click', () => {
    navegacion.classList.add('ocultar');
    overlay.remove();
    boton.remove();
  });

  overlay.onclick = function() {
    overlay.remove();
    navegacion.classList.add('ocultar');
    boton.remove();
  };
};
/*h2 de hero*/
document.addEventListener("DOMContentLoaded", function() {
  let h2 = document.querySelector(".hero h2"),
      h2_width = h2.getBoundingClientRect().width;

  function addBubbles() {
      for (var i = 0; i < h2_width / 15; i++) {
          let b = document.createElement("div");
          b.className = "bubble";
          b.style.width = Math.random() < 0.5 ? "20px" : "10px";
          b.style.left = Math.random() * (h2_width - 20) + "px";
          b.style.animationDelay = 4 * Math.random() + "s";
          h2.appendChild(b);
      }
  }
  addBubbles();
});