document.addEventListener('DOMContentLoaded', () => {
    updateCounts();
  });
  
  function updateCounts() {
    const allJobs = document.querySelectorAll('.job').length;
    document.getElementById('all-count').textContent = `(${allJobs})`;
     // aquí se agregan los nuevos tipos
const parttimeJobs = document.querySelectorAll('.job.parttime').length;
document.getElementById('parttime-count').textContent = `(${parttimeJobs})`;
const freelanceJobs = document.querySelectorAll('.job.freelance').length;
document.getElementById('freelance-count').textContent = `(${freelanceJobs})`;
const fulltimeJobs = document.querySelectorAll('.job.fulltime').length;
document.getElementById('fulltime-count').textContent = `(${fulltimeJobs})`;
const albañilJobs = document.querySelectorAll('.job.albañil').length;
document.getElementById('albañil-count').textContent = `(${albañilJobs})`;
const dfdJobs = document.querySelectorAll('.job.dfd').length;
document.getElementById('dfd-count').textContent = `(${dfdJobs})`;
const asi_es_loJobs = document.querySelectorAll('.job.asi_es_lo').length;
document.getElementById('asi_es_lo-count').textContent = `(${asi_es_loJobs})`;
const nuevo_tipoJobs = document.querySelectorAll('.job.nuevo_tipo').length;
document.getElementById('nuevo_tipo-count').textContent = `(${nuevo_tipoJobs})`;
// fin de los nuevos tipos
  }
  
  function filterJobs(type) {
    const jobs = document.querySelectorAll('.job');
    jobs.forEach(job => {
      if (type === 'all') {
        job.style.display = 'block';
      } else {
        job.style.display = job.classList.contains(type) ? 'block' : 'none';
      }
    });

       // Ocultar el contenedor de filtros en dispositivos móviles después de seleccionar una opción
       if (window.innerWidth <= 768) {
        document.querySelector('.filter-container').style.display = 'none';
        document.querySelector('.filter-toggle').style.display = 'block';
    }
  }

   // Función para alternar la visibilidad del contenedor de filtros en dispositivos móviles
   document.querySelector('.filter-toggle').addEventListener('click', function() {
    const filterContainer = document.querySelector('.filter-container');
    if (filterContainer.style.display === 'block') {
        filterContainer.style.display = 'none';
    } else {
        filterContainer.style.display = 'block';
    }
});

// Restaurar la visibilidad del contenedor de filtros en dispositivos más grandes
window.addEventListener('resize', function() {
    const filterContainer = document.querySelector('.filter-container');
    const filterToggle = document.querySelector('.filter-toggle');
    if (window.innerWidth > 768) {
        filterContainer.style.display = 'block';
        filterToggle.style.display = 'none';
    } else {
        filterContainer.style.display = 'none';
        filterToggle.style.display = 'block';
    }
});

// Inicializar la visibilidad correcta al cargar la página
window.addEventListener('load', function() {
    const filterContainer = document.querySelector('.filter-container');
    const filterToggle = document.querySelector('.filter-toggle');
    if (window.innerWidth > 768) {
        filterContainer.style.display = 'block';
        filterToggle.style.display = 'none';
    } else {
        filterContainer.style.display = 'none';
        filterToggle.style.display = 'block';
    }
});

  function filterJobs(type) {
    const jobs = document.querySelectorAll('.job');
    jobs.forEach(job => {
      if (type === 'all') {
        job.style.display = 'block';
      } else {
        job.style.display = job.classList.contains(type) ? 'block' : 'none';
      }
    });

       // Ocultar el contenedor de filtros en dispositivos móviles después de seleccionar una opción
       if (window.innerWidth <= 768) {
        document.querySelector('.filter-container').style.display = 'none';
        document.querySelector('.filter-toggle').style.display = 'block';
    }
  }

   // Función para alternar la visibilidad del contenedor de filtros en dispositivos móviles
   document.querySelector('.filter-toggle').addEventListener('click', function() {
    const filterContainer = document.querySelector('.filter-container');
    if (filterContainer.style.display === 'block') {
        filterContainer.style.display = 'none';
    } else {
        filterContainer.style.display = 'block';
    }
});

// Restaurar la visibilidad del contenedor de filtros en dispositivos más grandes
window.addEventListener('resize', function() {
    const filterContainer = document.querySelector('.filter-container');
    const filterToggle = document.querySelector('.filter-toggle');
    if (window.innerWidth > 768) {
        filterContainer.style.display = 'block';
        filterToggle.style.display = 'none';
    } else {
        filterContainer.style.display = 'none';
        filterToggle.style.display = 'block';
    }
});

// Inicializar la visibilidad correcta al cargar la página
window.addEventListener('load', function() {
    const filterContainer = document.querySelector('.filter-container');
    const filterToggle = document.querySelector('.filter-toggle');
    if (window.innerWidth > 768) {
        filterContainer.style.display = 'block';
        filterToggle.style.display = 'none';
    } else {
        filterContainer.style.display = 'none';
        filterToggle.style.display = 'block';
    }
});
  