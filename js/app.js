// Datos del carrusel
const carouselData = [
  {
    id: 1,
    imageUrl: "imagenes/cuped.webp",
    title: "Mundo Acuatico Cupe",
    description: "Centro Turístico de recreación acuática, diversas actividades recreativas para niños y todo publico en general. ",
    locationUrl: "https://maps.app.goo.gl/QbLQA4gXM8ta9cZF7",
  },
  {
    id: 2,
    imageUrl: "imagenes/encuentro.webp",
    title: "El Encuentro",
    description:
      "Centro recreacional turístico cuenta con ríos naturales y cristalinos, áreas de recreación, juegos deportivos parrilladas y más.",
    locationUrl: "https://maps.app.goo.gl/n7Hs4tWvTsFLe9W26",
  },
  {
    id: 3,
    imageUrl: "imagenes/paseos.webp",
    title: "Puerto villarroel",
    description: "Río navegable, se realizan paseos en barcos, botes y canoas. Pesca deportiva (Pacú, Surubí y más), aprecia la flora y fauna.",
    locationUrl: "https://maps.app.goo.gl/UoiAPn369XuysTbv8",
  },
  {
    id: 3,
    imageUrl: "imagenes/valleencanto.webp",
    title: "Valle Encanto",
    description: "Centro turístico que cuenta con parqueos, parrilleros, juegos deportivos, saltos en cuerda al río, paseos en botes y más.",
    locationUrl: "https://maps.app.goo.gl/4RiBDLaHShRUDZKC7",
  },
]

// Elementos del DOM
const heroCarousel = document.getElementById("heroCarousel")
const slidesContainer = document.getElementById("slidesContainer")
const prevButton = document.getElementById("prevButton")
const nextButton = document.getElementById("nextButton")
const slideIndicators = document.getElementById("slideIndicators")

// Variables de estado
let currentSlide = 0
let isPaused = false
let touchCount = 0
let autoPlayTimer = null
const autoPlayInterval = 5000 // 5 segundos

// Inicializar el carrusel
function initCarousel() {
  // Crear slides
  carouselData.forEach((slide, index) => {
    const slideElement = document.createElement("div")
    slideElement.className = `slide ${index === 0 ? "active" : ""}`

    slideElement.innerHTML = `
      <img src="${slide.imageUrl}" alt="${slide.title}" class="slide-image">
      <div class="slide-overlay"></div>
      <div class="slide-content">
        <div class="slide-content-inner">
          <h2 class="slide-title">${slide.title}</h2>
          <p class="slide-description">${slide.description}</p>
        </div>
      </div>
      <div class="location-link">
        <a href="${slide.locationUrl}" target="_blank" rel="noopener noreferrer">
          <img src="imagenes/ubicacion.avif" alt="Ubicación" class="location-image">
          <span class="location-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            Ver ubicación
          </span>
        </a>
      </div>
    `

    slidesContainer.appendChild(slideElement)
  })

  // Crear indicadores
  carouselData.forEach((_, index) => {
    const indicator = document.createElement("button")
    indicator.className = `indicator ${index === 0 ? "active" : ""}`
    indicator.setAttribute("aria-label", `Ir al slide ${index + 1}`)
    indicator.addEventListener("click", () => goToSlide(index))

    slideIndicators.appendChild(indicator)
  })

  // Iniciar autoplay
  startAutoPlay()

  // Agregar event listeners
  prevButton.addEventListener("click", prevSlide)
  nextButton.addEventListener("click", nextSlide)

  // Event listeners para pausar/reanudar
  heroCarousel.addEventListener("mouseenter", pauseCarousel)
  heroCarousel.addEventListener("mouseleave", resumeCarousel)

}

// Funciones de navegación
function nextSlide() {
  goToSlide((currentSlide + 1) % carouselData.length)
}

function prevSlide() {
  goToSlide(currentSlide === 0 ? carouselData.length - 1 : currentSlide - 1)
}

function goToSlide(index) {
  // Actualizar slides
  const slides = document.querySelectorAll(".slide")
  slides[currentSlide].classList.remove("active")
  slides[index].classList.add("active")

  // Actualizar indicadores
  const indicators = document.querySelectorAll(".indicator")
  indicators[currentSlide].classList.remove("active")
  indicators[index].classList.add("active")

  // Actualizar índice actual
  currentSlide = index
}

// Funciones de autoplay
function startAutoPlay() {
  if (!isPaused) {
    stopAutoPlay() // Limpiar cualquier timer existente
    autoPlayTimer = setInterval(nextSlide, autoPlayInterval)
  }
}

function stopAutoPlay() {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
    autoPlayTimer = null
  }
}

function pauseCarousel() {
  isPaused = true
  stopAutoPlay()
  // Mostrar botones en móvil
  if (isMobileDevice()) {
    heroCarousel.classList.add("paused-mobile")
  }
}

function resumeCarousel() {
  isPaused = false
  startAutoPlay()
    // Ocultar botones en móvil
  if (isMobileDevice()) {
    heroCarousel.classList.remove("paused-mobile")
  }
}

// Manejo de eventos táctiles para móvil



// Detectar si es dispositivo móvil
function isMobileDevice() {
  return window.innerWidth <= 768
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", initCarousel)

// Reiniciar autoplay cuando la ventana vuelve a estar activa
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible" && !isPaused) {
    startAutoPlay()
  } else {
    stopAutoPlay()
  }
})

  
// nabvar//

document.addEventListener("DOMContentLoaded", () => {
  const navLinks = document.querySelector(".nav-links");
  const menuBtn = document.getElementById("menu-btn");
  const closeBtn = document.getElementById("close-btn");
  const heroCarousel = document.getElementById("heroCarousel");

  let touchCount = 0;

  // Cerrar el menú
  function closeMenu() {
    menuBtn.checked = false;
    closeBtn.checked = false;
  }

  document.addEventListener("click", (event) => {
    const isClickInsideMenu = navLinks.contains(event.target);
    const isMenuBtnClicked =
      event.target === menuBtn || event.target.closest(".btn.menu-btn");

    // Objetivo 1: Cerrar el menú si se hace clic fuera y está abierto
    if (!isClickInsideMenu && !isMenuBtnClicked && menuBtn.checked) {
      closeMenu();
      return; // Se cierra el menú y se detiene aquí
    }

    // Objetivo 2: Lógica para Hero
    const isInHero = heroCarousel.contains(event.target);
    const isNavButton =
      event.target.closest("#prevButton") ||
      event.target.closest("#nextButton");

    if (isInHero && !isClickInsideMenu && !isMenuBtnClicked && !isNavButton) {
      if (menuBtn.checked) {
        // Si el menú está abierto, se cierra y se espera el siguiente toque
        closeMenu();
        return;
      }

      // Si el menú ya estaba cerrado y se toca por segunda vez en Hero → handleTouch
      if (touchCount === 0) {
        pauseCarousel();
        touchCount = 1;
      } else {
        resumeCarousel();
        touchCount = 0;
      }
    }
  });
});
  


  document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".fade-in-up, .about-text, .about-image");
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target); // Deja de observar una vez activado
            }
        });
    }, { threshold: 0.2 }); // Se activa cuando al menos el 20% del elemento es visible

    elements.forEach((el) => observer.observe(el));
});
    

      //section about//
      // Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", () => {
  const learnMoreBtn = document.getElementById("learn-more-btn");
  const extraInfo = document.getElementById("extra-info");

  // Add click event listener to the "Learn More" button
  learnMoreBtn.addEventListener("click", () => {
    if (extraInfo.classList.contains("hidden")) {
      extraInfo.classList.remove("hidden");
      extraInfo.style.display = "block";
    } else {
      extraInfo.classList.add("hidden");
      extraInfo.style.display = "none";
    }
  });

  // Add hover effect to the campus image
  const campusImage = document.getElementById("campus-image");
  campusImage.addEventListener("mouseenter", () => {
    campusImage.style.transform = "scale(1.05)";
  });

  campusImage.addEventListener("mouseleave", () => {
    campusImage.style.transform = "scale(1)";
  });
});
    

    