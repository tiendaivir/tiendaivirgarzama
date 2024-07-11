document.addEventListener("DOMContentLoaded", function() {
    const particleContainer = document.getElementById('particle-container');
    const numParticles = 300;
  
    for (let i = 0; i < numParticles; i++) {
      let particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.width = particle.style.height = `${Math.random() * 3 + 1}px`;
      particle.style.top = `${Math.random() * 100}%`;
      particle.style.left = `${Math.random() * 100}%`;
      particleContainer.appendChild(particle);
  
      animateParticle(particle);
    }
  
    function animateParticle(particle) {
      const duration = Math.random() * 7000 + 7000;
      const delay = Math.random() * 5000;
      const initialTop = parseFloat(particle.style.top);
      const initialLeft = parseFloat(particle.style.left);
      const finalTop = initialTop + Math.random() * 20 - 10;
      const finalLeft = initialLeft + Math.random() * 20 - 10;
  
      particle.animate([
        { transform: `translate(${initialLeft}vw, ${initialTop}vh)` },
        { transform: `translate(${finalLeft}vw, ${finalTop}vh)` }
      ], {
        duration: duration,
        easing: 'linear',
        iterations: Infinity,
        delay: delay
      });
    }
  });
  