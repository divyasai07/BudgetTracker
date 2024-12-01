const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.querySelector("#sidebar");

sidebar.classList.add("expand");

hamBurger.addEventListener("click", function () {
  sidebar.classList.toggle("compress");
  sidebar.classList.toggle("expand");
});

$("#deleteIncomeModal").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget);
  var incomeId = button.data("income-id");
  var modal = $(this);
  modal.find("#income-id").val(incomeId);
});
document.querySelectorAll(".delete-icon[data-expense-id]").forEach((icon) => {
  icon.addEventListener("click", function () {
    const expenseId = this.getAttribute("data-expense-id");
    document.getElementById("expense-id").value = expenseId;
  });
});

const editIcons = document.querySelectorAll(".edit-icon");

editIcons.forEach((icon) => {
  icon.addEventListener("click", function () {
    const incomeId = this.getAttribute("data-income-id");
    const amount = this.getAttribute("data-amount");
    const description = this.getAttribute("data-description");
    const category = this.getAttribute("data-category");
    const date = this.getAttribute("data-date");

    document.getElementById("income-id").value = incomeId;
    document.getElementById("amount").value = amount;
    document.getElementById("description").value = description;
    document.getElementById("category").value = category;
    document.getElementById("date").value = date;
  });
});
