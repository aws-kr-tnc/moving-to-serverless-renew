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
          <!-- MAP for specific photos -->
          <v-flex xs12 v-if="$route.params.gps_lat">
            <v-card height="100%" dark color="secondary">
              <v-container>
                <l-map class="mapCards" :zoom="zoom" :center="center">
                  <l-tile-layer :url="url"></l-tile-layer>
                  <l-marker :lat-lng="markerLatLng" ></l-marker>
                </l-map>
              </v-container>
              <v-container>
                <p>{{$route.params.desc}}</p>
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
                <v-chip v-for="tag in ($route.params.tags.split(','))"
                  class="ma-1"
                  color="teal"
                  label
                  text-color="white"
                  small
                >
                  {{tag}}
                </v-chip>
              </v-container>
            </v-card>
          </v-flex>

          <!-- MAP list for all photos -->
          <v-flex xs4 v-for="photo in photoList">
            <v-card class="ma-0">
              <v-container>
                <l-map style="height: 300px; width: 100%; z-index: 0;" :zoom="zoom" :center="getCenterGps(photo.geotag_lat, photo.geotag_lng)">
                  <l-tile-layer :url="url"></l-tile-layer>
                  <l-marker :lat-lng="getCenterGps(photo.geotag_lat, photo.geotag_lng)" ></l-marker>
                </l-map>
              </v-container>
              <v-container class="ma-0 pa-2">
                <kbd><v-icon left>mdi-map-marker-check</v-icon>{{photo.address}}</kbd>
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
                >
                  <v-icon left>mdi-tag-multiple</v-icon>
                  TAGS
                </v-chip>
                <v-chip v-for="tag in (photo.tags.split(','))"
                  class="ma-1"
                  color="teal"
                  label
                  text-color="white"
                  small
                >
                  {{tag}}
                </v-chip>
              </div >
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

  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [47.413220, -1.219482],
      markerLatLng: [47.313220, -1.319482],
      photoList: [],
    };
  },
  created() {
    if (typeof (this.$route.params.gps_lat) === 'undefined') {
      this.getPhotos();
    } else {
      this.center = [this.$route.params.gps_lat, this.$route.params.gps_lng];
      this.markerLatLng = [this.$route.params.gps_lat, this.$route.params.gps_lng];
    }
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),

    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok !== true) return;
        console.log('Photo list retrieved successfully ✨');
        this.photoList = resp.data.photos;
        console.log(this.photoList);
      } catch (error) {
        console.error(error);
      }
    },
    getCenterGps(lat, lng) {
      return [lat, lng];
    },
  },
};
</script>
<style scoped>
  .mapCards {
    height: 300px;
    width: 100%;
    z-index: 0;
  }
</style>
