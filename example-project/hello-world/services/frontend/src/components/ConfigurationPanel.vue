<template>
  <div>
    <v-container fluid fill-height>
      <v-row class="fill-height">
        <!-- Sidebar -->
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
                  @update:model-value="changeCategory"
                ></v-select>
              </v-col>
            </v-row>
          </v-card>

          <!-- Profit View Card -->
          <v-card class="mb-4">
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

          <!-- Generate Poem Button -->
          <v-card class="mb-4">
            <v-row>
              <v-col cols="12" sm="12">
                <v-btn class="btn" width="100%" @click="openPoemDialog">
                  Generate Poem
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <!-- Charts Container (Right side) -->
        <v-col cols="12" md="10" class="d-flex flex-column fill-height charts">
          <v-row class="fill-height">
            <!-- Scatter Plot -->
            <v-col cols="6" md="6" class="d-flex flex-column">
              <ScatterPlot
                :key="scatterPlotId"
                :selectedCategory="categories.selectedValue"
                @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
                style="flex-grow: 1; max-height: 100%"
              />
            </v-col>

            <!-- Line Plot -->
            <v-col cols="6" md="6" class="d-flex flex-column">
              <LinePlot
                :key="linePlotId"
                :selectedCompany="companies.selectedValue"
                :selectedCompanyName="
                  companies.values.find(
                    (company) => company.id === companies.selectedValue
                  )?.name
                "
                :selectedAlgorithm="algorithm.selectedValue"
                style="flex-grow: 1; max-height: 100%"
              />
            </v-col>
          </v-row>

          <!-- Bar Chart (Below the Scatter and Line Plot) -->
          <v-row class="fill-height">
            <v-col cols="12" md="12" class="d-flex flex-column">
              <BarChart
                :selectedCategory="categories.selectedValue"
                :selectedCompany="companies.selectedValue"
                style="flex-grow: 1; max-height: 100%"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>

    <!-- Poem Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Company Poem</span>
        </v-card-title>

        <v-card-text>
          <div v-if="isLoading" class="d-flex justify-center">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </div>
          <div v-else-if="poem">
            <p>{{ poem }}</p>
          </div>
          <div v-else>
            <p>No poem available. Please generate one.</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closePoemDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ScatterPlot from "./ScatterPlot";
import LinePlot from "./LinePlot";
import BarChart from "./BarChart";

export default {
  components: { ScatterPlot, LinePlot, BarChart },
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    categories: {
      values: ["All", "tech", "health", "bank"],
      selectedValue: "All",
    },
    companies: {
      values: [], // Initialize empty array for companies
      selectedValue: 1, // Set default selected company value
    },
    algorithm: {
      values: ["none", "random", "regression"],
      selectedValue: "none",
    },
    poem: "", // Initialize poem data
    dialog: false, // Control dialog visibility
    isLoading: false, // Loading state for poem generation
  }),
  watch: {
    "companies.selectedValue"(newVal, oldVal) {
      console.log(
        `Company changed from ${oldVal} to ${newVal}. Clearing poem.`
      );
      this.poem = ""; // Clear the poem when a new company is selected
    },
  },
  mounted() {
    console.log("Component mounted. Now fetching companies.");
    this.fetchCompanies();
  },
  methods: {
    fetchCompanies() {
      const category = this.categories.selectedValue; // Ensure this value is reactive
      console.log("Fetching companies for category:", category);

      fetch(`http://localhost:5000/companies?category=${category}`)
        .then((response) => {
          console.log("API response received:", response);
          return response.json();
        })
        .then((data) => {
          console.log("Parsed JSON data:", data);
          const updatedCompanies = data.map((company) => ({
            id: company.id,
            name: company.name,
          }));
          console.log("Fetched companies:", updatedCompanies);

          this.companies.values = [...updatedCompanies];
          if (this.companies.values.length > 0) {
            if (
              !this.companies.values.some(
                (company) => company.id === this.companies.selectedValue
              )
            ) {
              this.companies.selectedValue = this.companies.values[0].id;
            }
          } else {
            this.companies.selectedValue = null;
          }
        })
        .catch((error) => {
          console.error("Error fetching companies:", error);
        });
    },
    changeCategory() {
      console.log("Category changed to:", this.categories.selectedValue);
      // Refetch companies when category changes
      this.fetchCompanies(); // Use the selected category directly

      // Update scatterPlotId to refresh scatter plot
      this.scatterPlotId += 1;

      console.log("Category changed to:", this.categories.selectedValue);
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
    openPoemDialog() {
      this.dialog = true; // Open the dialog
      this.fetchPoem(); // Fetch the poem when dialog opens
    },
    closePoemDialog() {
      this.dialog = false; // Close the dialog
    },
    fetchPoem() {
      console.log("Fetching poem for company:", this.companies.selectedValue);
      if (!this.companies.selectedValue) {
        console.error("No company selected");
        this.poem =
          "No company selected. Please select a company to generate a poem.";
        return;
      }
      const companyId = this.companies.selectedValue;
      this.isLoading = true; // Start loading
      fetch(`http://localhost:5000/llm/groq/poem/${companyId}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.poem) {
            console.log("Received poem:", data.poem);
            this.poem = data.poem;
          } else {
            console.error("Error fetching the poem:", data);
            this.poem = "Sorry, I couldn't generate a poem at this time.";
          }
        })
        .catch((error) => {
          console.error("Error fetching the poem:", error);
          this.poem = "An error occurred while generating the poem.";
        })
        .finally(() => {
          this.isLoading = false; // End loading
        });
    },
  },
};
</script>
