<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Recipes</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-12">
        <v-data-table
          :headers="headers"
          :items="recipes"
          item-key="name"
          class="elevation-1"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Recipes",

  data: () => {
    return {
      headers: [
        {
          text: "Recipe name",
          align: "start",
          sortable: false,
          value: "name",
        },
        {
          text: "Calories",
          value: "calories",
          filter: (value) => {
            if (!this.calories) return true;

            return value < parseInt(this.calories);
          },
        },
      ],
      recipes: [],
    };
  },
};
</script>
