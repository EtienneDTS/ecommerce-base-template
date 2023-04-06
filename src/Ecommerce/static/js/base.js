const hamburgerMenu = document.querySelector('.nav__hamburger-menu');
const toggleMenu = document.querySelector('.toggle-menu')

hamburgerMenu.addEventListener('click', function() {
  this.classList.toggle('active');
  toggleMenu.classList.toggle('active');
});