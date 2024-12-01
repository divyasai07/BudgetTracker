/*const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});*/

const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.querySelector("#sidebar");

sidebar.classList.add("expand");

hamBurger.addEventListener("click", function () {
  sidebar.classList.toggle("compress");
  sidebar.classList.toggle("expand");
});
