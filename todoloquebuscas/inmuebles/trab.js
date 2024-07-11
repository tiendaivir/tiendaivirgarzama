document.addEventListener('DOMContentLoaded', () => {
    updateCounts();
  });
  
  function updateCounts() {
    const allJobs = document.querySelectorAll('.job').length;
    const fulltimeJobs = document.querySelectorAll('.job.fulltime').length;
    const parttimeJobs = document.querySelectorAll('.job.parttime').length;
    const freelanceJobs = document.querySelectorAll('.job.freelance').length;
    const albañilJobs = document.querySelectorAll('.job.albañil').length;
  
    document.getElementById('all-count').textContent = `(${allJobs})`;
    document.getElementById('fulltime-count').textContent = `(${fulltimeJobs})`;
    document.getElementById('parttime-count').textContent = `(${parttimeJobs})`;
    document.getElementById('freelance-count').textContent = `(${freelanceJobs})`;
    document.getElementById('albañil-count').textContent = `(${albañilJobs})`;
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
  }
  