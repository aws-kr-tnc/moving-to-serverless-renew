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
                :src="photo.src"
                class="white--text"
                height="200px"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              >
                <v-card-title
                  class="fill-height align-end"
                  v-text="photo.desc"
                ></v-card-title>
              </v-img>
                <div class="text--primary">
                  <v-chip
                    class="ma-2"
                    x-small
                    color="primary"
                    label
                    text-color="white"
                  >
                    <v-icon left>mdi-tag-multiple</v-icon>
                    TAGS
                  </v-chip>
                  <v-chip v-for="tag in (photo.tags.split(','))"
                    class="ma-2"
                    color="teal"
                    label
                    text-color="white"
                    x-small
                  >
                    {{tag}}
                  </v-chip>
                </div >

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on" @click="showMap(photo.geotag_lat, photo.geotag_lng)">
                      <v-icon>mdi-map-marker-check</v-icon>
                    </v-btn>
                  </template>
                  <span>Show map</span>
                </v-tooltip>

                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on" @click="deleteConfirm(photo.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <span>Delete photo</span>
                </v-tooltip>
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
    photoList: [],
  }),
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),
    async buildImgSrc(id) {
      const res = await service.Photo.getPhotoBlob(id);
      const blobImgUrl = URL.createObjectURL(res.data);
      return blobImgUrl;
    },
    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok !== true) return;
        console.log('Photo list retrieved successfully ✨');
        this.photoList = await Promise.all(resp.data.photos.map(async (obj) => {
          const blobUrl = await this.buildImgSrc(obj.id);
          return { ...obj, src: blobUrl };
        }));
        // console.log(`photosList: ${this.photoList}`);
      } catch (error) {
        console.error(error);
      }
    },
    showMap(lat, lng) {
      console.log(lat);
      console.log(lng);
      this.$router.push({ name: 'map', params: { gps_lat: lat, gps_lng: lng } });
    },
    deleteConfirm(id) {
      console.log(id);
      console.log('deletePhoto loaded');
      this.$swal({
        title: 'Are you sure?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes!',
      }).then((result) => {
        if (result.value) {
          this.deletePhoto(id);
        }
        this.$router.push({ name: 'photolist' });
      });
    },

    async deletePhoto(id) {
      try {
        const resp = await service.Photo.deletePhoto(id);
        if (resp.data.ok === true) {
          console.log('Image deleted successfully ✨');
          this.$swal(
            {
              title: 'Success!',
              text: 'Your photo has been deleted successfully.',
              type: 'success',
              onClose: () => {
                this.$router.push({ name: 'photolist' });
              },
            },
          );
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
