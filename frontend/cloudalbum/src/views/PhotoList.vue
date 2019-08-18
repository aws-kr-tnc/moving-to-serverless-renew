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
                @click="originalSize(photo.id)"
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
          <v-flex v-if="photoList.length === 0">
            <v-alert
              v-model="alert"
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
import service from '@/service';
import MapDialog from '@/components/map/MapDialog';

export default {
  name: 'PhotoList',
  components: {
    MapDialog,
  },
  data: () => ({
    photoList: [],
    showMapDialog: false,
    mapDialogLat: 0,
    mapDialogLng: 0,
    mapDialogDesc: '',
    mapDialogTags: '',
  }),
  methods: {
    async buildImgSrc(id) {
      const res = await service.Photo.getPhotoBlob(id);
      return URL.createObjectURL(res.data);
    },
    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok !== true) return;
        console.log('Photo list retrieved successfully ✨');
        this.photoList = await Promise.all(resp.data.photos.map(async (obj) => {
          const blobUrl = await this.buildImgSrc(obj.id, 'thmubnail');
          return { ...obj, src: blobUrl };
        }));
      } catch (error) {
        console.error(error);
      }
    },
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
        this.deletePhoto(id);
      });
    },
    async deletePhoto(id) {
      try {
        const resp = await service.Photo.deletePhoto(id);
        if (!resp.data.ok) throw new Error(resp);
        console.log('Image deleted successfully ✨');
        this.$swal(
          {
            title: 'Success!',
            text: 'Your photo has been deleted successfully.',
            type: 'success',
          },
        );
        this.getPhotos();
      } catch (error) {
        console.error(error);
      }
    },
    async originalSize(id) {
      console.log(id);
      const blobUrl = await this.buildImgSrc(id, 'original');
      this.$swal(
        {
          width: '95%',
          height: '95%',
          html: `<div>
                   <a href='${blobUrl}' target=_blank>
                     <img src='${blobUrl}' width=90%>
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
    this.getPhotos();
  },
};
</script>
