const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});
$("#deleteIncomeModal").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget);
  var incomeId = button.data("income-id");
  var modal = $(this);
  modal.find("#income-id").val(incomeId);
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
