<template>
  <v-container>

    <v-card
      class="mx-auto"
      max-width="95%"
    >
      <v-container
        fluid
        grid-list-md
        pa-2
      >
        <v-layout
          wrap
        >
          <v-flex
            v-for="card in cards"
            :key="card.title"
            v-bind="{ [`xs${card.flex}`]: true }"
          >
            <v-card>
              <v-img
                :src="card.src"
                class="white--text"
                height="200px"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              >
                <v-card-title
                  class="fill-height align-end"
                  v-text="card.title"
                ></v-card-title>
              </v-img>
              <v-card-text>
                <div class="text--primary">
                  well meaning and kindly.<br>
                  "a benevolent smile"
                </div>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn icon>
                  <v-icon>mdi-favorite</v-icon>
                </v-btn>

                <v-btn icon>
                  <v-icon>mdi-bookmark</v-icon>
                </v-btn>

                <v-btn icon>
                  <v-icon>mdi-share</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    cards: [
      { title: '1Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 4 },
      { title: '2Best ', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '3Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '4Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 4 },
      { title: '5Best ', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '6Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
    ],
  }),
};
</script>
