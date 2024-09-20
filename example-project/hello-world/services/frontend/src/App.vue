<template>
  <v-app>
    <v-app-bar app dark>
      <!-- UZH logo -->
      <img
        :src="require('@/assets/uzh.png')"
        alt="UZH Logo"
        class="logoMarginLeft smallPaddingTop"
      />

      <!-- Header text -->
      <h2><span>Jakob Schwarz | 24-720-252</span></h2>
    </v-app-bar>

    <v-main>
      <ConfigurationPanel />
    </v-main>
  </v-app>
</template>

<script>
import ConfigurationPanel from "./components/ConfigurationPanel.vue";

export default {
  name: "App",

  components: {
    ConfigurationPanel,
  },

  data: () => ({
    //
  }),
};
</script>
