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
              <v-list-item
                v-on:click="selectRecipe(position)"
                :key="position"
              >
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

                <v-list-item-action>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="primary" dark icon v-bind="attrs" v-on="on">
                        <v-icon>mdi-pencil-outline</v-icon>
                      </v-btn>
                    </template>
                    <span>Edit</span>
                  </v-tooltip>
                </v-list-item-action>

                <v-list-item-action>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="primary" dark icon v-bind="attrs" v-on="on">
                        <v-icon>mdi-calendar</v-icon>
                      </v-btn>
                    </template>
                    <span>Add to meal plan</span>
                  </v-tooltip>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="8">
        <v-card class="mx-auto" v-if="selected">
          <v-img height="250" :src="selected.image"></v-img>
          <v-card-title v-html="selected.title"></v-card-title>

          <v-col cols="8" offset="2">
            <v-list class="mx-15" three-line>
              <template v-for="item in selected.ingredients">
                <v-list-item :key="item.name">
                  <v-list-item-avatar>
                    <v-img :src="item.image"></v-img>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>
                      <span v-html="item.name"></span> &mdash;

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

                  <v-list-item-action>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="primary"
                          dark
                          icon
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon v-if="item.stock">mdi-cart</v-icon>
                          <v-icon v-if="!item.stock">mdi-cart-off</v-icon>
                        </v-btn>
                      </template>
                      <span v-if="item.stock">Enough in stock</span>
                      <span v-if="!item.stock">Not enough in stock</span>
                    </v-tooltip>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </v-list>
          </v-col>

          <v-card-text>
            <span class="text--secondary" v-html="selected.total_time"></span
            >&mdash;
            <span v-html="selected.description"></span>
          </v-card-text>

          <v-timeline>
            <v-timeline-item
              v-for="(step, i) in selected.steps"
              :key="i"
              color="lightgreen"
              small
              class="mx-15"
            >
              <template v-slot:opposite>
                <span
                  v-if="i != selectedAlarm"
                  :class="
                    `headline font-weight-bold lightgreen--text` +
                    (i !== selectedStep)
                      ? 'text--disabled'
                      : ''
                  "
                  v-text="step.time + `m`"
                ></span>

                <v-progress-circular
                  v-if="i == selectedAlarm"
                  :size="80"
                  :rotate="180"
                  :width=8
                  class="mx-5"
                  color=purple
                  :value="currentTimer"
                >{{step.time}}m</v-progress-circular>

                <v-tooltip
                  v-if="i != selectedAlarm && i == selectedStep"
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
              </template>

              <div class="py-4">
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
                  v-if="i == selectedStep && selectedStep != (selected.steps.length - 1)"
                  v-on:click="
                    selectedStep++;
                    selectedAlarm = null;
                  "
                >
                  <v-btn class="" fab dark small color="teal">
                    <v-icon dark> mdi-chevron-right </v-icon>
                  </v-btn>
                </v-col>
              </div>
            </v-timeline-item>
          </v-timeline>

          <v-card-title>Next scheduled meals</v-card-title>
          <v-card-text :key="date.date" v-for="date in selected.scheduled">
            <v-chip v-text="date.date"></v-chip>
          </v-card-text>
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
    selectRecipe: function (position) {
      this.selected = this.recipes[position];
    },
    updateTimer: function () {
      console.log(this.currentTimer);
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
  },

  data: () => {
    return {
      timerAlert: null,
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
          description: `<span class=text--primary>Receta sencilla de fabada asturiana.</span>`,
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
        {
          id: 1,
          image:
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Fabada_en_cazuela_de_barro.jpg/1200px-Fabada_en_cazuela_de_barro.jpg",
          title: "Fabada",
          kind: "Legumbre",
          description: `<span class=text--primary>blah, blah</span>`,
        },
        {
          id: 2,
          image:
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Fabada_en_cazuela_de_barro.jpg/1200px-Fabada_en_cazuela_de_barro.jpg",
          title: "Fabada",
          kind: "Legumbre",
          description: `<span class=text--primary>blah, blah</span>`,
        },
      ],
    };
  },
};
</script>
