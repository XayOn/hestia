<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Tasks</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-list subheader two-line flat>
          <v-list-item v-for="item in tasks" :key="item.id">
            <template>

              <v-list-item-action>
                <v-checkbox
                  v-model="item.complete"
                  color="primary"
                ></v-checkbox>
              </v-list-item-action>

              <v-list-item-content
                :class="item.complete ? `text-decoration-line-through` : ''"
              >
                <v-list-item-title v-html="item.task"></v-list-item-title>
              </v-list-item-content>
		
              <v-list-item-content v-if="item.repeat">
                <v-list-item-title v-html="'Repeats every ' + item.repeat"></v-list-item-title>
              </v-list-item-content>
	
              <v-list-item-content v-if="item.repeat">
                <v-list-item-title v-html="'Due on tuesday'"></v-list-item-title>
              </v-list-item-content>




            </template>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="message"
          prepend-icon="mdi-calendar"
          filled
          clear-icon="mdi-close-circle"
          clearable
          label="Task"
          @click:prepend="openCalendar"
          type="text"
        ></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="repeat"
          append-outer-icon="mdi-plus"
          filled
          @click:append-outer="addTask"
          clear-icon="mdi-close-circle"
          clearable
          label="Repeat"
          placeholder="Never"
          @click:prepend="openCalendar"
          type="text"
          >Never</v-text-field
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Tasks",

  methods: {
    openCalendar: function () {},
    addTask: function () {
      this.tasks.push({
        id: this.tasks.length,
        complete: false,
        task: this.message,
        due: this.currentDue,
        repeat: this.repeat,
      });
      this.message = null;
      this.currentDue = null;
    },
  },

  data: () => {
    return {
      repeat: null,
      currentDue: null,
      message: null,
      tasks: [
        { id: 0, complete: false, task: "foo bar baz", due: new Date() },
        { id: 1, complete: false, task: "foo bar", due: new Date() },
        {
          id: 2,
          complete: false,
          task: "fregar",
          repeat: "2d",
          due: new Date(),
        },
      ],
    };
  },
};
</script>
