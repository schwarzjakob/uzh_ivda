<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Profit View of Company: {{ $props.selectedCompany }}</h3>
    </v-row>
    <div style="height: 100%">
      <div id="myLinePlot" style="height: inherit"></div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
export default {
  name: "LinePlot",
  props: ["selectedCompany", "selectedAlgorithm"],
  watch: {
    selectedCompany() {
      this.LinePlotData.x = [];
      this.LinePlotData.y = [];
      this.LinePlotData.predictedX = [];
      this.LinePlotData.predictedY = [];

      this.fetchData();
    },
    selectedAlgorithm() {
      this.LinePlotData.x = [];
      this.LinePlotData.y = [];
      this.LinePlotData.predictedX = [];
      this.LinePlotData.predictedY = [];

      this.fetchData();
    },
  },
  data: () => ({
    LinePlotData: {
      x: [],
      y: [],
      predictedX: [],
      predictedY: [],
    },
  }),
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      // req URL to retrieve single company from backend
      var reqUrl =
        "http://127.0.0.1:5000/companies/" +
        this.$props.selectedCompany +
        "?algorithm=" +
        this.$props.selectedAlgorithm;
      console.log("ReqURL " + reqUrl);
      // await response and data
      const response = await fetch(reqUrl);
      const responseData = await response.json();

      // Console log to inspect the data structure
      responseData.profit.forEach((profit) => {
        console.log(
          `Year: ${profit.year}, Value: ${profit.value}, Predicted: ${profit.is_predicted}`
        );
      });

      // transform data to usable by lineplot
      responseData.profit.forEach((profit) => {
        if (profit.is_predicted) {
          // Predicted data
          this.LinePlotData.predictedX.push(profit.year);
          this.LinePlotData.predictedY.push(profit.value);
        } else {
          // Real data
          this.LinePlotData.x.push(profit.year);
          this.LinePlotData.y.push(profit.value);
        }
      });
      // draw the lineplot after the data is transformed
      this.drawLinePlot();
    },
    drawLinePlot() {
      // Trace for actual profit data (blue curve)
      var actualProfitTrace = {
        x: this.LinePlotData.x, // x values for actual years (up to the last year of actual data)
        y: this.LinePlotData.y, // y values for actual profits
        mode: "lines+markers",
        name: "Actual Profit",
        line: { color: "0028a5", width: 2 },
      };

      // Trace for the predicted profit point (red point)
      var predictedProfitTrace = {
        x: this.LinePlotData.predictedX, // x value for the predicted year (2022)
        y: this.LinePlotData.predictedY, // y value for the predicted profit
        mode: "lines+markers",
        name: "Predicted Profit",
        line: { color: "7596ff", width: 2, dash: "dash" },
        marker: { color: "7596ff", width: 2 },
      };

      // Trace for the dashed line connecting the last actual point to the predicted point
      var connectingLineTrace = {
        x: [
          this.LinePlotData.x[0], // Last actual year
          this.LinePlotData.predictedX[0], // Predicted year
        ],
        y: [
          this.LinePlotData.y[0], // Last actual profit
          this.LinePlotData.predictedY[0], // Predicted profit
        ],
        mode: "lines",
        name: "Connecting Line",
        line: { color: "7596ff", width: 2, dash: "dash" }, // Dashed line
        showlegend: false, // No need to show this in the legend
      };

      // Combine all traces into the data array
      var data = [actualProfitTrace, predictedProfitTrace, connectingLineTrace];

      var layout = {
        xaxis: {
          title: "Year",
          zeroline: false,
        },
        yaxis: {
          title: "Profit",
          zeroline: false,
        },
        showlegend: true, // Show legend for actual and predicted data
      };
      var config = { responsive: true, displayModeBar: false };
      Plotly.newPlot("myLinePlot", data, layout, config);
    },
  },
};
</script>
