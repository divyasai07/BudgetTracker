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
function clearNotifications(event) {
  event.preventDefault();
  const notificationCount = document.getElementById("notification-count");
  if (notificationCount) {
    notificationCount.style.display = "none";
  }
  window.location.href = event.currentTarget.href;
}
