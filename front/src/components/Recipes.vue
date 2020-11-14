<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <h1 class="display-2 font-weight-bold mb-3">Recipes</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-card class="mx-auto" tile>
          <v-list three-line>
            <template v-for="(item, position) in recipes">
              <v-list-item v-on:click="selectRecipe(position)" :key="position">
                <v-list-item-avatar>
                  <v-img :src="item.image"></v-img>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title
                    ><span v-html="item.title"></span> &mdash;
                    <span
                      class="text--secondary text-overline"
                      v-html="item.kind"
                    ></span
                  ></v-list-item-title>
                  <v-list-item-subtitle
                    v-html="item.description"
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="8">
        <v-card class="mx-auto" v-if="selected">
          <v-img height="250" :src="selected.image"></v-img>
          <v-card-title v-if="!edit" v-html="selected.title"></v-card-title>

          <v-card-title v-if="edit">
            <v-text-field
              v-model="selected.title"
              outlined
              clearable
              label="Title"
              type="text"
            ></v-text-field>
          </v-card-title>

          <v-col cols="8" offset="2">
            <v-card>
              <v-fab-transition>
                <v-btn
                  v-show="edit"
                  v-on:click="addIngredient()"
                  color="pink"
                  dark
                  absolute
                  bottom
                  right
                  fab
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-fab-transition>
              <v-list class="mx-15" three-line>
                <v-subheader>Ingredients</v-subheader>
                <template v-for="(item, num) in selected.ingredients">
                  <v-list-item :key="num">
                    <v-list-item-avatar>
                      <v-img
                        :src="item.image"
                        v-on:click="changeIngredientImage(num)"
                      ></v-img>
                    </v-list-item-avatar>

                    <v-list-item-content v-if="!edit">
                      <v-list-item-title>
                        <span v-html="item.name"></span>

                        &mdash;

                        <span
                          class="text--secondary text-overline"
                          v-html="item.quantity"
                        ></span>

                        <span
                          class="text--secondary text-overline"
                          v-html="item.unit"
                        ></span>
                      </v-list-item-title>

                      <v-list-item-subtitle
                        v-html="item.description"
                      ></v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-content v-if="edit">
                      <v-list-item-subtitle>
                        <v-row>
                          <v-col cols="6">
                            <v-text-field
                              v-if="edit"
                              v-model="item.name"
                              label="Name"
                            >
                            </v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="6">
                            <v-text-field
                              v-if="edit"
                              v-model="item.quantity"
                              color="blue darken-2"
                              label="Quantity"
                            >
                            </v-text-field>
                          </v-col>

                          <v-col cols="6">
                            <v-text-field
                              v-if="edit"
                              v-model="item.unit"
                              label="Unit name"
                            >
                            </v-text-field>
                          </v-col>
                        </v-row>

                        <v-row>
                          <v-col cols="12">
                            <v-text-field
                              v-if="edit"
                              v-model="item.description"
                              label="Description"
                            >
                            </v-text-field>
                          </v-col>
                        </v-row>
                      </v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="edit"
                            color="pink"
                            dark
                            icon
                            v-bind="attrs"
                            v-on="on"
                            v-on:click="removeIngredient(num)"
                          >
                            <v-icon>mdi-minus-circle</v-icon>
                          </v-btn>
                        </template>

                        <span>Remove ingredient</span>
                      </v-tooltip>
                    </v-list-item-action>
                  </v-list-item>
                </template>
              </v-list>
            </v-card>
          </v-col>

          <v-card-text>
            <div v-if="!edit">
              <span class="text--secondary" v-html="selected.total_time"></span>
              &mdash;
              <span class="text--primary" v-html="selected.description"></span>
            </div>

            <v-row>
              <v-col cols="2">
                <v-text-field
                  v-if="edit"
                  v-model="selected.total_time"
                  outlined
                  clearable
                  label="Total time"
                  type="text"
                >
                </v-text-field>
              </v-col>
              <v-col cols="10">
                <v-text-field
                  v-if="edit"
                  v-model="selected.description"
                  outlined
                  clearable
                  label="Description"
                  type="text"
                >
                </v-text-field>
              </v-col>
            </v-row>
          </v-card-text>

          <v-timeline>
            <v-timeline-item
              v-for="(step, i) in selected.steps"
              :key="i"
              color="purple"
              icon="mdi-chef-hat"
              class="mx-15"
              fill-dot
            >
              <template v-slot:opposite>
                <v-row>
                  <v-col cols="5">
                    <span
                      v-if="!edit && i != selectedAlarm"
                      :class="
                        `headline font-weight-bold lightgreen--text` +
                        (i !== selectedStep)
                          ? 'text--disabled'
                          : ''
                      "
                      v-text="step.time + `m`"
                    ></span>

                    <span v-if="edit">
                      <v-text-field
                        v-model="step.time"
                        clearable
                        label="Time"
                        type="text"
                      >
                      </v-text-field>
                    </span>
                  </v-col>

                  <v-col cols="2">
                    <v-progress-circular
                      v-if="!edit && i == selectedAlarm"
                      :size="80"
                      :rotate="180"
                      :width="8"
                      class="mx-5"
                      color="purple"
                      :value="currentTimer"
                    >
                      {{ step.time }}m
                    </v-progress-circular>

                    <v-tooltip
                      v-if="!edit && i != selectedAlarm && i == selectedStep"
                      bottom
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          class="mx-5"
                          fab
                          color="light-green"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon
                            dark
                            v-on:click="
                              selectedAlarm = selectedStep;
                              startTimer();
                            "
                          >
                            mdi-alarm-plus
                          </v-icon>
                        </v-btn>
                      </template>
                      <span>Start timer</span>
                    </v-tooltip>
                  </v-col>
                </v-row>
              </template>

              <div v-if="edit" class="py-4">
                <v-text-field
                  v-model="step.name"
                  clearable
                  label="Step name"
                  type="text"
                >
                </v-text-field>

                <v-textarea
                  v-model="step.description"
                  clearable
                  label="Step description"
                  type="text"
                >
                </v-textarea>
              </div>

              <div v-if="!edit" class="py-4">
                <h2
                  :class="
                    i !== selectedStep
                      ? 'text--disabled'
                      : 'text--primary' +
                        `headline font-weight-light mb-4 lightgreen--text `
                  "
                  v-html="step.name"
                ></h2>
                <div
                  :class="
                    i !== selectedStep ? 'text--disabled' : 'text--primary'
                  "
                  v-html="step.description"
                ></div>
                <br />
                <v-col
                  offset="4"
                  cols="1"
                  v-if="
                    i == selectedStep &&
                    selectedStep != selected.steps.length - 1
                  "
                  v-on:click="
                    selectedStep++;
                    selectedAlarm = null;
                  "
                >
                  <v-btn class="" fab dark small color="teal">
                    <v-icon dark> mdi-step-forward </v-icon>
                  </v-btn>
                </v-col>
              </div>
            </v-timeline-item>

            <v-btn
              color="pink"
              class="float-center"
              float-center
              v-if="edit"
              :style="{ left: '50%', transform: 'translateX(-50%)' }"
              v-on:click="addStep()"
              fab
              large
              dark
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-timeline>

          <div v-if="selected && !edit">
            <v-divider></v-divider>
            <v-card-title class=justify-center>Next scheduled meals</v-card-title>
            <v-card-text class=text-center :key="date.date" v-for="date in selected.scheduled">
              <v-chip v-text="date.date"></v-chip>
            </v-card-text>
          </div>

          <v-row v-if="edit" style="margin-top: 20px; margin-bottom: -45px">
            <v-col cols="2" offset="5">
              <v-btn class="mx-3" v-on:click="save()" color="primary">
                Save
              </v-btn>
            </v-col>
          </v-row>
          <div style="width: 55px">
            <v-speed-dial
              v-model="fab"
              :bottom="true"
              :right="true"
              :left="false"
              :top="false"
              direction="top"
              :open-on-hover="false"
              transition="slide-y-reverse"
              style="width: 55px"
            >
              <template v-slot:activator>
                <v-btn v-model="fab" color="blue darken-2" dark fab>
                  <v-icon v-if="fab">mdi-close</v-icon>
                  <v-icon v-else>mdi-account-circle</v-icon>
                </v-btn>
              </template>
              <v-btn v-on:click="edit = true" fab dark small color="green">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn fab dark small v-on:click="sheet = true" color="red">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-speed-dial>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <div class="text-center ma-2">
      <v-snackbar v-model="timerAlert">
        <span v-html="currentAlarmText"> </span>
        <template v-slot:action="{ attrs }">
          <v-btn color="pink" text v-bind="attrs" @click="timerAlert = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>

    <div class="text-center">
      <v-bottom-sheet v-model="sheet" persistent>
        <v-sheet class="text-center" height="200px">
          <v-btn class="mt-6" text color="accent" @click="sheet = false">
            cancel
          </v-btn>
          <v-btn class="mt-6" text color="error" @click="deleteRecipe()">
            delete
          </v-btn>
          <div class="py-3">Confirm recipe deletion</div>
        </v-sheet>
      </v-bottom-sheet>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "Recipes",
  computed: {
    currentAlarmText: function () {
      if (this.selected !== null && this.selectedAlarm !== null) {
        return `${this.selected.steps[this.selectedAlarm].name} has finished`;
      } else {
        return "";
      }
    },
  },

  methods: {
    save: function () {
      this.edit = false;
    },
    changeIngredientImage: function (num) {
      const ing = this.selected.ingredients[num];
      if (!this.edit) {
        return;
      }
      return ing
    },
    addStep: function () {
      this.selected.steps.push({
        name: "",
        description: "",
        time: "",
      });
    },
    addIngredient: function () {
      this.selected.ingredients.push({
        name: "",
        description: "",
        quantity: "",
        unit: "",
        image: "",
      });
    },
    selectRecipe: function (position, edit) {
      this.selected = this.recipes[position];
      if (edit) {
        this.edit = true;
      }
    },
    updateTimer: function () {
      if (this.currentTimer < 100) {
        this.currentTimer = Math.round(this.currentTimer + this.currentStep);
        this.selected.steps[this.selectedAlarm].time -= 1;
        setTimeout(this.updateTimer, 60 * 1000);
      } else {
        this.timerAlert = true;
      }
    },
    startTimer: function () {
      this.currentStep = 100 / this.selected.steps[this.selectedAlarm].time;
      setTimeout(this.updateTimer, 60 * 1000);
    },
    deleteRecipe: function () {
      this.sheet = false;
    },
    removeIngredient: function (ingredient) {
      this.selected.ingredients.splice(ingredient, 1);
    },
  },

  data: () => {
    return {
      sheet: false,
      edit: false,
      timerAlert: null,
      fab: false,
      selectedAlarm: null,
      currentStep: 1,
      currentTimer: 0,
      selectedStep: 0,
      selected: null,
      recipes: [
        {
          id: 0,
          image:
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Fabada_en_cazuela_de_barro.jpg/1200px-Fabada_en_cazuela_de_barro.jpg",
          title: "Fabada",
          kind: "Legumbre",
          description: `Receta sencilla de fabada asturiana.`,
          scheduled: [{ date: "2020-01-01 15:00" }],
          total_time: "10m",
          ingredients: [
            {
              name: "Alubias",
              kind: "Legumbres",
              description: "Alubias asturianas",
              quantity: "200",
              unit: "gramos",
              stock: true,
              image:
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Cocina_Palentina_-_Alubias_de_Salda%C3%B1a_001.JPG/1200px-Cocina_Palentina_-_Alubias_de_Salda%C3%B1a_001.JPG",
            },
            {
              name: "Chorizo",
              kind: "Embutidos",
              description: "Chorizo de leon",
              quantity: "50",
              unit: "gramos",
              stock: false,
              image:
                "https://upload.wikimedia.org/wikipedia/commons/f/f1/Aspecto_al_corte_del_Chorizo_de_Le%C3%B3n.jpg",
            },
          ],
          steps: [
            {
              name: "Poner a remojo las alubias",
              description:
                "En un cazo grande, dejamos las alubias a remojo toda la noche, en acido de baterias o grog.",
              time: "120",
            },
            {
              name: "Ordeñar el chorizo",
              description: "Claramente, se ordeña el chorizo, nada raro aqui",
              time: "10",
            },
          ],
        },
      ],
    };
  },
};
</script>
<style>
.v-speed-dial--direction-top {
  width: inherit !important;
}
</style>
