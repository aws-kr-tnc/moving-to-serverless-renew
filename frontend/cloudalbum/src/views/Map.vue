<template>
  <v-container grid-list-md text-center>
    <v-layout wrap>
      <v-flex xs12 v-if="$route.params.gps_lat">
        <v-card height="100%" dark color="secondary">
          <v-container>
              <l-map style="height: 550px; width: 100%" :zoom="zoom" :center="center">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="markerLatLng" ></l-marker>
              </l-map>
          </v-container>
        </v-card>
      </v-flex>

      <v-flex xs4 v-for="photo in photoList">
        <v-card height="100%" dark color="secondary">
          <v-container>
              <l-map style="height: 300px; width: 100%" :zoom="zoom" :center="center">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="markerLatLng" ></l-marker>
              </l-map>
          </v-container>
        </v-card>
      </v-flex>


    </v-layout>
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
    async getPhotos() {
      console.log('Get photo list..');
      try {
        const resp = await service.Photo.photoList();
        if (resp.data.ok !== true) return;
        console.log('Photo list retrieved successfully ✨');
        this.photoList = resp.data;
        console.log(this.photoList);
      } catch (error) {
        console.error(error);
      }
    },
  },

};
</script>
