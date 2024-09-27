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
            <v-card-text>
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-btn
                    class="btn"
                    width="100%"
                    v-bind="attrs"
                    v-on="on || {}"
                    @click="openPoemDialog"
                  >
                    {{
                      companies.values
                        .find(
                          (company) => company.id === companies.selectedValue
                        )
                        ?.name.charAt(0)
                        .toUpperCase() +
                      companies.values
                        .find(
                          (company) => company.id === companies.selectedValue
                        )
                        ?.name.slice(1) +
                      " Poem"
                    }}
                  </v-btn>
                </template>
                <span>
                  <strong>Query Parameters:</strong>
                  <ul class="mt-2">
                    <li>Company Name</li>
                  </ul>
                </span>
              </v-tooltip>
            </v-card-text>
          </v-card>

          <!-- Generate Additional Information Button -->
          <v-card class="mb-4">
            <v-card-text>
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-btn
                    class="btn"
                    width="100%"
                    v-bind="attrs"
                    v-on="on || {}"
                    @click="openAdditionalInfoDialog"
                  >
                    Additional
                    {{
                      companies.values
                        .find(
                          (company) => company.id === companies.selectedValue
                        )
                        ?.name.charAt(0)
                        .toUpperCase() +
                      companies.values
                        .find(
                          (company) => company.id === companies.selectedValue
                        )
                        ?.name.slice(1)
                    }}
                    Information
                  </v-btn>
                </template>
                <span>
                  <strong>Query Parameters:</strong>
                  <ul class="mt-2">
                    <li>Company Name</li>
                    <li>Founding Year</li>
                    <li>Number of Employees</li>
                  </ul>
                </span>
              </v-tooltip>
            </v-card-text>
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
    <v-dialog v-model="poemDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline">
            {{
              companies.values
                .find((company) => company.id === companies.selectedValue)
                ?.name.charAt(0)
                .toUpperCase() +
              companies.values
                .find((company) => company.id === companies.selectedValue)
                ?.name.slice(1) +
              " Poem"
            }}
          </span>
        </v-card-title>

        <v-card-text>
          <!-- Generated Poem Section -->
          <div>
            <strong>Generated Poem:</strong>
            <br />
            <div v-if="isPoemLoading" class="d-flex justify-center">
              <v-progress-circular
                indeterminate
                color="primary"
              ></v-progress-circular>
            </div>
            <div
              v-else-if="poem"
              class="poem-content"
              v-html="parsedPoem"
            ></div>
            <div v-else>
              <p>No poem available. Please generate one.</p>
            </div>
          </div>
          <br />
          <!-- Prompt and Parameters Section -->
          <div>
            <strong>Prompt Sent to API:</strong>
            <p>{{ poemPrompt }}</p>
            <strong>Params:</strong>
            <p>company name</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closePoemDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Additional Information Dialog -->
    <v-dialog v-model="additionalInfoDialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline">
            Additional
            {{
              companies.values
                .find((company) => company.id === companies.selectedValue)
                ?.name.charAt(0)
                .toUpperCase() +
              companies.values
                .find((company) => company.id === companies.selectedValue)
                ?.name.slice(1)
            }}
            Information
          </span>
        </v-card-title>

        <v-card-text>
          <!-- Generated Additional Information Section -->
          <div>
            <strong>Generated Information:</strong>
            <br />
            <div v-if="isAdditionalInfoLoading" class="d-flex justify-center">
              <v-progress-circular
                indeterminate
                color="primary"
              ></v-progress-circular>
            </div>
            <div
              v-else-if="additionalInformation"
              class="additional-info-content"
              v-html="parsedAdditionalInformation"
            ></div>
            <div v-else>
              <p>No additional information available. Please generate one.</p>
            </div>
          </div>
          <br />
          <!-- Prompt and Parameters Section -->
          <div>
            <strong>Prompt Sent to API:</strong>
            <p>{{ additionalInfoPrompt }}</p>
            <strong>Params:</strong>
            <p>company name, founding year, number of employees</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeAdditionalInfoDialog"
            >Close</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ScatterPlot from "./ScatterPlot";
import LinePlot from "./LinePlot";
import BarChart from "./BarChart";
import { marked } from "marked"; // Import marked

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
    poemDialog: false, // Control poem dialog visibility
    isPoemLoading: false, // Loading state for poem generation
    additionalInformation: "", // Initialize additional information data
    additionalInfoDialog: false, // Control additional info dialog visibility
    isAdditionalInfoLoading: false, // Loading state for additional info generation
  }),
  computed: {
    parsedPoem() {
      return marked(this.poem);
    },
    parsedAdditionalInformation() {
      return marked(this.additionalInformation);
    },
    poemPrompt() {
      if (!this.companies.selectedValue) return "No company selected.";
      const companyName = this.companies.values.find(
        (company) => company.id === this.companies.selectedValue
      )?.name;
      return `Please provide a poem or information about the company ${companyName}.`;
    },
    additionalInfoPrompt() {
      if (!this.companies.selectedValue) return "No company selected.";
      const company = this.companies.values.find(
        (company) => company.id === this.companies.selectedValue
      );

      const foundingYear = company.founding_year || "unknown";
      const employees = company.employees || "unknown";

      return `Provide an overview of the company ${company.name}, including its founding year ${foundingYear} and the number of employees ${employees}.`;
    },
  },
  watch: {
    "companies.selectedValue"(newVal, oldVal) {
      console.log(
        `Company changed from ${oldVal} to ${newVal}. Clearing poem and additional information.`
      );
      this.poem = ""; // Clear the poem when a new company is selected
      this.additionalInformation = ""; // Clear additional information
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
          return response.json();
        })
        .then((data) => {
          const updatedCompanies = data.map((company) => ({
            id: company.id,
            name: company.name,
            founding_year: company.founding_year, // Ensure these fields are present
            employees: company.employees, // Ensure these fields are present
          }));

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
    // Poem Dialog Methods
    openPoemDialog() {
      this.poemDialog = true; // Open the dialog
      this.fetchPoem(); // Fetch the poem when dialog opens
    },
    closePoemDialog() {
      this.poemDialog = false; // Close the dialog
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
      this.isPoemLoading = true; // Start loading
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
          this.isPoemLoading = false; // End loading
        });
    },

    // Additional Information Dialog Methods
    openAdditionalInfoDialog() {
      this.additionalInfoDialog = true; // Open the dialog
      this.fetchAdditionalInformation(); // Fetch the additional information when dialog opens
    },
    closeAdditionalInfoDialog() {
      this.additionalInfoDialog = false; // Close the dialog
    },
    fetchAdditionalInformation() {
      console.log(
        "Fetching additional information for company:",
        this.companies.selectedValue
      );
      if (!this.companies.selectedValue) {
        console.error("No company selected");
        this.additionalInformation =
          "No company selected. Please select a company to generate additional information.";
        return;
      }
      const companyId = this.companies.selectedValue;
      this.isAdditionalInfoLoading = true; // Start loading
      fetch(
        `http://localhost:5000/llm/groq/additional_information/${companyId}`
      )
        .then((response) => response.json())
        .then((data) => {
          if (data.additional_information) {
            console.log(
              "Received additional information:",
              data.additional_information
            );
            this.additionalInformation = data.additional_information;
          } else {
            console.error("Error fetching the additional information:", data);
            this.additionalInformation =
              "Sorry, I couldn't generate additional information at this time.";
          }
        })
        .catch((error) => {
          console.error("Error fetching the additional information:", error);
          this.additionalInformation =
            "An error occurred while generating the additional information.";
        })
        .finally(() => {
          this.isAdditionalInfoLoading = false; // End loading
        });
    },
  },
};
</script>
