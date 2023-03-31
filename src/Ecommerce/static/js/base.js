const hamburgerMenu = document.querySelector('.nav__hamburger-menu');
const toggleMenu = document.querySelector('.toggle-menu')
console.log(toggleMenu)
hamburgerMenu.addEventListener('click', function() {
  this.classList.toggle('active');
  toggleMenu.classList.toggle('active');
  console.log(this)
  console.log(toggleMenu)
});