<template>
  <div>
    <v-container fluid>
      <v-row>
        <!-- Sidebar with separate cards -->
        <v-col cols="12" md="2" class="sideBar">
          <!-- Company Overview Card -->
          <v-card class="mb-4">
            <v-row>
              <v-col cols="12" sm="12">
                <div class="control-panel-font">Company Overview</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="12">
                <v-select
                  :items="categories.values"
                  label="Category"
                  dense
                  v-model="categories.selectedValue"
                  @change="changeCategory"
                ></v-select>
              </v-col>
            </v-row>
          </v-card>

          <!-- Profit View Card -->
          <v-card>
            <v-row>
              <v-col cols="12" sm="12">
                <div class="control-panel-font">Profit View of Company</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="12">
                <v-select
                  :items="companies.values"
                  label="Company"
                  dense
                  v-model="companies.selectedValue"
                  @change="changeCompany"
                ></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="12">
                <v-select
                  :items="algorithm.values"
                  label="Prediction Algorithm"
                  dense
                  v-model="algorithm.selectedValue"
                  @change="changeAlgorithm"
                ></v-select>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <!-- Scatter Plot -->
        <v-col cols="12" md="5">
          <ScatterPlot
            :key="scatterPlotId"
            :selectedCategory="categories.selectedValue"
            @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
          />
        </v-col>

        <!-- Line Plot -->
        <v-col cols="12" md="5">
          <LinePlot
            :key="linePlotId"
            :selectedCompany="companies.selectedValue"
            :selectedAlgorithm="algorithm.selectedValue"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ScatterPlot from "./ScatterPlot";
import LinePlot from "./LinePlot";
export default {
  components: { ScatterPlot, LinePlot },
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    categories: {
      values: ["All", "tech", "health", "bank"],
      selectedValue: "All",
    },
    companies: {
      values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      selectedValue: 1,
    },
    algorithm: {
      values: ["none", "random", "regression"],
      selectedValue: "none",
    },
    methods: {
      changeCategory() {
        this.scatterPlotId += 1;
      },
      changeCompany() {
        this.linePlotId += 1;
      },
      changeAlgorithm() {
        this.linePlotId += 1;
      },
      changeCurrentlySelectedCompany(companyId) {
        this.companies.selectedValue = companyId;
        this.changeCompany();
      },
    },
  }),
};
</script>
