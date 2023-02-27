const navbarToggle = document.getElementById('navbar-toggle');
const navbarMenu = document.getElementById('navbar-menu');
const closeBtn = document.getElementById('close-btn');

navbarToggle.addEventListener('click', () => {
  navbarMenu.classList.toggle('active');
  navbarToggle.classList.toggle('hide');
});

closeBtn.addEventListener('click', () => {
  navbarMenu.classList.remove('active');
  navbarToggle.classList.remove('hide');
});
