$("#deleteIncomeModal").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget);
  var incomeId = button.data("income-id");
  var modal = $(this);
  modal.find("#income-id").val(incomeId);
});
