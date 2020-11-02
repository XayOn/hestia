<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Events calendar</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-12">
        <v-sheet height="400">
          <v-calendar
            ref="calendar"
            :now="today"
            :value="today"
            :events="events"
            color="primary"
            type="week"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Calendar",

  data: () => {
    return {
      events: [],
    };
  },
};
</script>
