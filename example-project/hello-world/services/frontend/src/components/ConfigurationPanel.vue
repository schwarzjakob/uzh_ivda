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
                  item-value="id"
                  item-title="name"
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
      values: [], // Initialize empty array for companies
      selectedValue: 1, // Set default selected company value to null
    },
    algorithm: {
      values: ["none", "random", "regression"],
      selectedValue: "none",
    },
  }),
  created() {
    // Fetch companies from backend
    this.fetchCompanies();
  },
  methods: {
    fetchCompanies() {
      // Use fetch API to retrieve data from your Flask backend
      fetch("http://localhost:5000/companies?category=All")
        .then((response) => response.json())
        .then((data) => {
          // Map the response to fit the structure of the v-select
          this.companies.values = data.map((company) => ({
            id: company.id, // Will be passed as v-select value
            name: company.name, // Will be displayed in v-select dropdown
          }));

          // Set default selected value to the first company in the list if not already set
          if (
            !this.companies.selectedValue &&
            this.companies.values.length > 0
          ) {
            this.companies.selectedValue = this.companies.values[0].id;
          }

          console.log("Fetched companies:", this.companies.values);
        })
        .catch((error) => {
          console.error("Error fetching companies:", error);
        });
    },
    changeCategory() {
      this.scatterPlotId += 1;
      console.log("Category changed to:", this.categories.selectedValue);
      // Fetch companies based on the new selected category
      fetch(
        `http://localhost:5000/companies?category=${this.categories.selectedValue}`
      )
        .then((response) => response.json())
        .then((data) => {
          this.companies.values = data.map((company) => ({
            id: company.id, // Set ID as item value
            name: company.name, // Set name as item text
          }));

          // Set default selected value to the first company in the list
          if (this.companies.values.length > 0) {
            this.companies.selectedValue = this.companies.values[0].id;
          } else {
            this.companies.selectedValue = null;
          }

          console.log(
            "Fetched companies after category change:",
            this.companies.values
          );
        })
        .catch((error) => {
          console.error("Error fetching companies:", error);
        });
    },
    changeCompany() {
      this.linePlotId += 1;
      console.log("Company selected:", this.companies.selectedValue);
      // Add logic to call the backend with the selected company
      fetch(
        `http://localhost:5000/companies/${this.companies.selectedValue}?algorithm=${this.algorithm.selectedValue}`
      )
        .then((response) => response.json())
        .then((data) => {
          console.log("Fetched company data:", data);
        })
        .catch((error) => {
          console.error("Error fetching company data:", error);
        });
    },
    changeAlgorithm() {
      this.linePlotId += 1;
      console.log("Algorithm changed to:", this.algorithm.selectedValue);
    },
    changeCurrentlySelectedCompany(companyId) {
      this.companies.selectedValue = companyId;
      this.changeCompany();
    },
  },
};
</script>
