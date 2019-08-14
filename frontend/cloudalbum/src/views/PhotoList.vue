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
            :key="photo.id"
            v-bind="{ ['xs4']: true }"
          >
            <v-card>
              <v-img
                ref="photos"
                lazy-src="https://cdn.vuetifyjs.com/images/cards/road.jpg"
                class="white--text"
                height="200px"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              >
                <v-card-title
                  class="fill-height align-end"
                  v-text="photo.title"
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
import axiosInstance from '@/plugins/axios';
import service from '@/service';

export default {
  name: 'PhotoList',

  data: () => ({
    photoList: [{
      address: null,
      city: null,
      desc: 'undefined',
      filename: '2c78ab7d-9cf4-49e1-a740-289fc3ee2e0c.jpg',
      filename_orig: 'DSC07570.jpg',
      filesize: 850996,
      geotag_lat: 45.43472222222222,
      geotag_lng: 12.346736111111111,
      height: '1371',
      id: 1,
      make: 'SONY ',
      model: 'DSLR-A300',
      nation: null,
      tags: 'undefined',
      taken_date: '2012-07-15 09:46:46',
      upload_date: '2019-08-13 07:25:55.770169',
      user_id: '1',
      width: '2048',
    }],
  }),
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),
    async buildImgSrc(id) {
      const res = await this.getBlobAxios(id);
      const blobImgUrl = URL.createObjectURL(res.data);
      return blobImgUrl;
    },
    getBlobAxios(id) {
      return axiosInstance.get(`/photos/${id}?mode=original`, {
        responseType: 'blob',
        timeout: 10000,
      });
    },
    setImgSrc() {
      let self = this
      this.photoList.map(async (elem, index) => {
        self.$refs.photos[index]._props.src = await self.buildImgSrc(elem.id);
      });
    },
    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok !== true) return;
        console.log('Photo list retrieved successfully ✨');
        this.photoList = resp.data.photos;
        console.log(`photosList: ${this.photoList}`);
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

  updated() {
    this.setImgSrc();
  },

};
</script>
