<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
    </v-row>
    <div style="height: 90vh">
      <div id="myScatterPlot" style="height: inherit"></div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  name: "ScatterPlot",
  props: ["selectedCategory"],
  watch: {
    selectedCategory: function () {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = []; // Ensure to clear the names as well
      this.ScatterPlotData.color = [];
      this.fetchData();
    },
  },
  data: () => ({
    ScatterPlotData: { x: [], y: [], name: [], color: [] },
    colors: {
      tech: "#1f77b4",
      health: "#ff7f0e",
      bank: "#2ca02c",
    },
  }),

  mounted() {
    this.fetchData();
  },

  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl =
        "http://127.0.0.1:5000/companies?category=" +
        this.$props.selectedCategory;
      const response = await fetch(reqUrl);
      const responseData = await response.json();

      // transform data to usable by scatterplot
      responseData.forEach((company) => {
        this.ScatterPlotData.name.push(company.name);
        this.ScatterPlotData.x.push(company.founding_year);
        this.ScatterPlotData.y.push(company.employees);

        // Assign color based on the company's category
        if (this.$props.selectedCategory === "All") {
          this.ScatterPlotData.color.push(this.colors[company.category]);
        } else {
          this.ScatterPlotData.color.push(
            this.colors[this.$props.selectedCategory]
          );
        }
      });

      this.drawScatterPlot();
    },
    drawScatterPlot() {
      var trace1 = {
        x: this.ScatterPlotData.x,
        y: this.ScatterPlotData.y,
        mode: "markers",
        type: "scatter",
        text: this.ScatterPlotData.name,
        marker: {
          color: this.ScatterPlotData.color,
          size: 12,
        },
      };
      var data = [trace1];
      var layout = {
        xaxis: { title: "Founding Year", zeroline: false },
        yaxis: { title: "Employees", zeroline: false },
      };
      var config = { responsive: true, displayModeBar: false };
      Plotly.newPlot("myScatterPlot", data, layout, config);
      this.clickScatterPlot();
    },
    clickScatterPlot() {
      var that = this;
      var myPlot = document.getElementById("myScatterPlot");
      myPlot.on("plotly_click", function (data) {
        for (var i = 0; i < data.points.length; i++) {
          let pn = data.points[i].pointNumber;
          that.$emit("changeCurrentlySelectedCompany", pn + 1);

          var colors = ["#00000" * 15];
          colors[pn] = "#3777ee";

          var update = { marker: { color: colors, size: 12 } };
          Plotly.restyle("myScatterPlot", update);
        }
      });
    },
  },
};
</script>
