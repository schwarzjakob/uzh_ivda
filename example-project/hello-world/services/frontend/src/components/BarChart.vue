<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>
        Comparing Profit per Employee at {{ capitalizedCompanyName }} vs
        Category Average
      </h3>
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
  computed: {
    capitalizedCompanyName() {
      if (!this.selectedCompanyName) return "";
      return (
        this.selectedCompanyName.charAt(0).toUpperCase() +
        this.selectedCompanyName.slice(1)
      );
    },
  },
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

      // Fetch industry standard data
      const industryReqUrl =
        `http://127.0.0.1:5000/industry_standard/` + companyData.category;
      const industryResponse = await fetch(industryReqUrl);
      const industryData = await industryResponse.json();

      // Set company name for the header
      this.selectedCompanyName = companyData.name;

      // Clear previous chart data
      this.barChartData.x = [];
      this.barChartData.y = [];
      this.barChartData.color = [];
      const industryStandard = { x: [], y: [] };

      // Loop through the company's profit data and calculate profit per employee
      companyData.profit.forEach((profit) => {
        const profitPerEmployee = profit.value / companyData.employees;
        this.barChartData.x.push(profit.year);
        this.barChartData.y.push(profitPerEmployee);
        this.barChartData.color.push(this.colors[companyData.category]);

        // Add industry standard value for the year if available
        const industryProfit = industryData.find(
          (item) => item.year === profit.year
        );
        if (industryProfit) {
          industryStandard.x.push(profit.year);
          industryStandard.y.push(industryProfit.value);
        }
      });

      // Draw the bar chart with the industry standard
      this.drawBarChart(industryStandard);
    },

    drawBarChart(industryStandard) {
      const companyTrace = {
        x: this.barChartData.x, // Years
        y: this.barChartData.y, // Profit per employee
        type: "bar",
        text: this.barChartData.y.map((value) => value.toFixed(2)), // Round to 2 decimal places
        marker: {
          color: this.barChartData.color,
        },
        name: this.capitalizedCompanyName,
      };

      const industryTrace = {
        x: industryStandard.x, // Years
        y: industryStandard.y, // Industry standard profit per employee
        type: "scatter", // Change from 'bar' to 'scatter'
        mode: "lines", // Set mode to 'lines' for a line plot
        text: industryStandard.y.map((value) => value.toFixed(2)), // Round to 2 decimal places
        line: {
          color: "#bd3902", // Grey color for industry standard
          width: 2, // Line width
        },
        name: "Category Average",
      };

      const data = [companyTrace, industryTrace];
      const layout = {
        barmode: "group", // Show bars side by side
        xaxis: { title: "Fiscal Year" },
        yaxis: { title: "Profit per Employee" },
        showlegend: true,
      };

      const config = { responsive: true, displayModeBar: false };
      Plotly.newPlot("myBarChart", data, layout, config);
    },
  },
};
</script>
