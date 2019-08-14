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
            v-for="photo in photoList"
            :key="photo.desc"
            v-bind="{ [xs4]: true }"
          >
            <v-card>
              <v-img
                :src="photo.src"
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
                  <v-icon>mdi-map-marker-check</v-icon>
                </v-btn>

                <v-btn icon>
                  <v-icon>mdi-delete</v-icon>
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
import { mapActions, mapGetters } from 'vuex';
import service from '@/service';

export default {
  name: 'PhotoList',

  data: () => ({
    cards: [
      { title: '1Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 4 },
      { title: '2Best ', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '3Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '4Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 4 },
      { title: '5Best ', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
      { title: '6Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 4 },
    ],
    photoList: [],
  }),
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),

    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok === true) {
          console.log('Photo list retrieved successfully ✨');
          this.photoList = JSON.stringify(resp.data.photos);
        }
      } catch (error) {
        console.error(error);
      }
    },

    popupAlert(resp) {
      let msg = '';
      if (resp.status === 400) msg = '400 error';
      if (resp.status === 500) msg = resp.body;
      if (resp.status === undefined) msg = resp;
      this.$swal(
        {
          type: 'error',
          title: 'Oops...',
          text: `Something went wrong! (${msg})`,
        },
      );
    },
  },

  created() {
    this.getPhotos();
  },


};
</script>
