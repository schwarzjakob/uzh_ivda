<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Profit per Employee: {{ selectedCompanyName }}</h3>
    </v-row>
    <div style="height: 100%">
      <div id="myBarChart" style="height: inherit"></div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  name: "BarChart",
  props: ["selectedCategory", "selectedCompany"],
  data() {
    return {
      barChartData: { x: [], y: [], color: [], name: [] },
      selectedCompanyName: "",
      colors: {
        tech: "#1f77b4",
        health: "#ff7f0e",
        bank: "#2ca02c",
      },
    };
  },
  watch: {
    selectedCategory() {
      this.fetchData();
    },
    selectedCompany() {
      this.fetchData();
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      // Fetch data from the backend for the selected company
      const reqUrl = `http://127.0.0.1:5000/companies/` + this.selectedCompany;
      const response = await fetch(reqUrl);
      const companyData = await response.json();

      // Set company name for the header
      this.selectedCompanyName = companyData.name;

      // Clear previous chart data
      this.barChartData.x = [];
      this.barChartData.y = [];
      this.barChartData.color = [];

      // Loop through the company's profit data and calculate profit per employee
      companyData.profit.forEach((profit) => {
        const profitPerEmployee = profit.value / companyData.employees;
        this.barChartData.x.push(profit.year);
        this.barChartData.y.push(profitPerEmployee);
        this.barChartData.color.push(this.colors[companyData.category]);
      });

      // Draw the bar chart
      this.drawBarChart();
    },
    drawBarChart() {
      const trace = {
        x: this.barChartData.x, // Years
        y: this.barChartData.y, // Profit per employee
        type: "bar",
        text: this.barChartData.y.map((value) => value.toFixed(2)), // Round to 2 decimal places and convert to string
        marker: {
          color: this.barChartData.color,
        },
      };

      const data = [trace];
      const layout = {
        xaxis: { title: "Year" },
        yaxis: { title: "Profit per Employee" },
        showlegend: false,
      };

      const config = { responsive: true, displayModeBar: false };
      Plotly.newPlot("myBarChart", data, layout, config);
    },
  },
};
</script>
