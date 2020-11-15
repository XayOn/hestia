<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant.sync="mini"
      permanent
      app
    >
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-title>Hestia</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item
          v-for="item in items"
          v-on:click="
            mini = true;
            selected = item.value;
          "
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <dashboard v-if="selected == 'home'"></dashboard>
      <recipes v-if="selected == 'recipes'"></recipes>
      <calendar v-if="selected == 'calendar'"></calendar>
      <tasks v-if="selected == 'tasks'"></tasks>
    </v-main>
  </v-app>
</template>

<script>
import Calendar from "./components/Calendar.vue";
import Dashboard from "./components/Dashboard.vue";
import Tasks from "./components/Tasks.vue";
import Recipes from "./components/Recipes.vue";

export default {
  name: "App",

  components: {
    calendar: Calendar,
    recipes: Recipes,
    dashboard: Dashboard,
    tasks: Tasks,
  },
  methods: {
    select: () => {
      console.log(this);
    },
  },

  data: () => ({
    selected: "home",
    drawer: true,
    items: [
      { title: "Home", value: "home", icon: "mdi-home-city" },
      { title: "Calendar", value: "calendar", icon: "mdi-calendar" },
      { title: "Recipes", value: "recipes", icon: "mdi-food-apple-outline" },
      { title: "Tasks", value: "tasks", icon: "mdi-calendar-check-outline" },
    ],
    mini: true,
  }),
};
</script>
