const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.querySelector("#sidebar");

sidebar.classList.add("expand");

hamBurger.addEventListener("click", function () {
  sidebar.classList.toggle("compress");
  sidebar.classList.toggle("expand");
});
const incomeLabels = JSON.parse("{{labels|safe}}");
const incomeValues = JSON.parse("{{data|safe}}");
const c1 = document.getElementById("pie_chart").getContext("2d");
new Chart(c1, {
  type: "pie",
  data: {
    labels: incomeLabels,
    datasets: [
      {
        label: "income by category",
        data: incomeValues,
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",
        ],
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Income by Category",
      },
    },
  },
});

const expenseLabels = JSON.parse("{{labels2|safe}}");
const expenseValues = JSON.parse("{{data2|safe}}");
const c2 = document.getElementById("expense_chart").getContext("2d");
new Chart(c2, {
  type: "pie",
  data: {
    labels: expenseLabels,
    datasets: [
      {
        label: "expense by category",
        data: expenseValues,
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",
        ],
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Expense by category",
      },
    },
  },
});
