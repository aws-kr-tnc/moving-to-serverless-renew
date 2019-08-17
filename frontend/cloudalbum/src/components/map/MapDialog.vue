<template>
  <v-dialog
    :value="value"
    @input="close"
  >
    <v-layout
      wrap
    >
      <v-flex xs12>
        <v-card dark color="secondary">
          <v-container
            class="mapContainer"
            fluid
            grid-list-md
            pa-2
          >
            <l-map
              :zoom="zoom"
              :center="center">
              <l-tile-layer :url="url"></l-tile-layer>
              <l-marker :lat-lng="center" ></l-marker>
            </l-map>
          </v-container>
          <v-container>
            <p>{{description}}</p>
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
            <v-chip v-for="(tag, index) in (tags.split(','))"
                    :key="index"
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
    </v-layout>
  </v-dialog>
</template>

<script>
export default {
  name: 'MapDialog',
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    latitude: {
      type: Number,
      default: 0,
    },
    longitude: {
      type: Number,
      default: 0,
    },
    description: {
      type: String,
      default: '',
    },
    tags: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 14,
    };
  },
  computed: {
    center() {
      return [this.latitude, this.longitude];
    },
  },
  methods: {
    getCenterGps(lat, lng) {
      return [lat, lng];
    },
    close() {
      this.$emit('close');
    },
  },
};
</script>

<style scoped>
.mapContainer {
  height: 600px;
  width: 100%;
}
</style>
