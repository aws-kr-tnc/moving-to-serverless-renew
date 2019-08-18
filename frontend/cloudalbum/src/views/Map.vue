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
          <v-flex xs4 v-for="(photo, index) in photoList" :key="index">
            <v-card class="ma-0">
              <v-container>
                <l-map
                  class="l-map"
                  :zoom="zoom"
                  :center="getCenterGps(photo.geotag_lat, photo.geotag_lng)"
                >
                  <l-tile-layer :url="url"></l-tile-layer>
                  <l-marker :lat-lng="getCenterGps(photo.geotag_lat, photo.geotag_lng)" ></l-marker>
                </l-map>
              </v-container>
              <v-container class="ma-0 pa-2">
                <v-icon left>mdi-map-marker-check</v-icon>
                {{photo.address}}
              </v-container>
              <v-card-title
                class="pa-1 ma-0 fill-height align-end"
                v-text="photo.desc"
              ></v-card-title>
              <div class="text--primary">
                <v-chip
                  class="ma-1"
                  small
                  color="primary"
                  label
                  text-color="white"
                >    if (this.photoList.length !== 0) return;

                  <v-icon left>mdi-tag-multiple</v-icon>
                  TAGS
                </v-chip>
                <v-chip
                  :key="index"
                  class="ma-1"
                  color="teal"
                  label
                  small
                  text-color="white"
                  v-for="(tag, index) in (photo.tags.split(','))"
                >
                  {{tag}}
                </v-chip>
              </div >
            </v-card>
          </v-flex>
          <v-flex v-if="photoList.length === 0">
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
  </v-container>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'PhotoList',
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [47.413220, -1.219482],
      markerLatLng: [47.313220, -1.319482],
    };
  },
  computed: {
    ...mapState('Photo', [
      'photoList',
    ]),
  },
  methods: {
    ...mapActions('Photo', ['getAllPhotoList']),
    getCenterGps(lat, lng) {
      return [lat, lng];
    },
  },
  created() {
    if (this.photoList.length !== 0) return;
    this.getAllPhotoList();
  },
};
</script>
<style scoped>
.l-map {
  height: 300px;
  width: 100%;
  z-index: 0;
}
</style>
