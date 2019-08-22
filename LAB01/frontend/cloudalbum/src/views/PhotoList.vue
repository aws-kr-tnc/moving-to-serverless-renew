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
                @click="showOriginalPhoto(photo.id)"
                ref="photos"
                :src="photo.thumbSrc"
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
                    class="ma-1"
                    small
                    color="primary"
                    label
                    text-color="white"
                  >
                    <v-icon left>mdi-tag-multiple</v-icon>
                    TAGS
                  </v-chip>
                  <v-chip
                    v-for="(tag, index) in (photo.tags.split(','))"
                    :key="index"
                    class="ma-1"
                    color="teal"
                    label
                    text-color="white"
                    small
                  >
                    {{tag}}
                  </v-chip>
                </div >
              <v-card-actions class="ma-0 pa-0">
                <v-spacer></v-spacer>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      icon v-on="on"
                      @click="showOriginalPhoto(photo.id)"
                    >
                      <v-icon>mdi-image-area</v-icon>
                    </v-btn>
                  </template>
                  <span>Show large image</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      icon v-on="on"
                      @click="showMap(photo.geotag_lat, photo.geotag_lng, photo.desc, photo.tags)"
                    >
                      <v-icon>mdi-map-marker-check</v-icon>
                    </v-btn>
                  </template>
                  <span>Show map</span>
                </v-tooltip>
                <v-tooltip bottom>
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
          <v-flex v-if="isLoading">
            <div class="text-center">
              <v-progress-circular
                :size="70"
                :width="7"
                color="purple"
                indeterminate
              ></v-progress-circular>
            </div>
          </v-flex>
          <v-flex v-if="isNoData && !isLoading">
            <v-alert
              dismissible
              color="primary"
              border="left"
              elevation="2"
              colored-border
              icon="mdi-information"
            >
              <strong>No data! Pleas upload your photos. (Click <v-icon>mdi-cloud-upload</v-icon> icon above)</strong>
            </v-alert>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
    <map-dialog
      v-model="showMapDialog"
      :latitude="mapDialogLat"
      :longitude="mapDialogLng"
      :description="mapDialogDesc"
      :tags="mapDialogTags"
      v-on:close="cloeMapDialog"
    />
  </v-container>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
import MapDialog from '@/components/map/MapDialog';

export default {
  name: 'PhotoList',
  components: {
    MapDialog,
  },
  data: () => ({
    showMapDialog: false,
    mapDialogLat: 0,
    mapDialogLng: 0,
    mapDialogDesc: '',
    mapDialogTags: '',
  }),
  computed: {
    ...mapState('Photo', [
      'photoList',
      'isLoading',
    ]),
    ...mapGetters('Photo', [
      'isNoData',
    ]),
  },
  methods: {
    ...mapActions('Photo', ['getAllPhotoList', 'deletePhoto', 'buildImgSrc']),
    showMap(latitude, longitude, description, tags) {
      this.mapDialogLat = latitude;
      this.mapDialogLng = longitude;
      this.mapDialogDesc = description;
      this.mapDialogTags = tags;
      this.showMapDialog = true;
    },
    cloeMapDialog() {
      this.showMapDialog = false;
      this.mapDialogLat = 0;
      this.mapDialogLng = 0;
      this.mapDialogDesc = '';
      this.mapDialogTags = '';
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
        if (!result.value) return;
        this.requestDeletePhoto(id);
      });
    },
    async requestDeletePhoto(id) {
      try {
        const isSuccess = await this.deletePhoto(id);
        if (!isSuccess) throw new Error('Error on deletePhoto in PhotoList.vue');
        console.log('Image deleted successfully ✨');
        this.$swal(
          {
            title: 'Success!',
            text: 'Your photo has been deleted successfully.',
            type: 'success',
          },
        );
      } catch (error) {
        console.error(error);
      }
    },
    async showOriginalPhoto(id) {
      console.log(`showOriginalPhoto: ${id}`);
      const mode = 'original';
      const originalSrc = this.buildImgSrc(id, mode);
      this.$swal(
        {
          width: '95%',
          height: '95%',
          html: `<div>
                   <a href='${originalSrc}' target=_blank>
                     <img src='${originalSrc}' width=90%>
                   </a>
                 </div>`,
        },
      );
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
    this.getAllPhotoList();
  },
};
</script>
