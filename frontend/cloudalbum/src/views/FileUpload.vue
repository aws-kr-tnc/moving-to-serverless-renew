<template>
  <v-container grid-list-md text-center>
    <v-layout wrap>

      <v-flex xs12>
        <v-card dark color="secondary">
          <v-container>
            <picture-input
              ref="pictureInput"
              margin="16"
              width="450"
              height="450"
              accept="image/jpeg,image/png"
              size="10"
              button-class="btn"
              :custom-strings="{
                upload: '<h1>Bummer!</h1>',
                drag: 'Drag your photo =)'
              }"
              @change="onChange">
            </picture-input>
          </v-container>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card dark color="secondary">
          <v-container>
              <l-map style="height: 300px; width: 100%" :zoom="zoom" :center="center">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="markerLatLng" ></l-marker>
              </l-map>
          </v-container>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card dark color="secondary">
            <v-card-text>
              <v-form>
                <v-text-field
                  id="tags"
                  label="Tags (separated by comma)"
                  name="tags"
                  prepend-icon="mdi-tag-multiple"
                  type="text"
                ></v-text-field>

                <v-text-field
                  id="description"
                  label="Description"
                  name="description"
                  prepend-icon="mdi-comment-text-multiple-outline"
                  type="text"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="attemptUpload">
                <v-icon>mdi-upload</v-icon> Submit
              </v-btn>
            </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import PictureInput from 'vue-picture-input';
import EXIF from 'exif-js';
import service from '@/service';

export default {
  name: 'FileUpload',
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 15,
      center: [45.43163333333333, 12.320180555555556],
      markerLatLng: [45.43163333333333, 12.320180555555556],
    };
  },
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  components: {
    PictureInput,
  },
  methods: {

    onChange() {
      console.log('New picture loaded');
      if (this.$refs.pictureInput.file) {
        this.image = this.$refs.pictureInput.file;
        EXIF.getData(this.image, function () {
          console.log(this.exifdata);
          console.log(this.exifdata.GPSLatitude);
          console.log(this.exifdata.GPSLatitudeRef);
          console.log(this.exifdata.GPSLongitude);
          console.log(this.exifdata.GPSLongitudeRef);

          let latitude = service.Photo.gpsConverter(this.exifdata.GPSLatitude, this.exifdata.GPSLatitudeRef);
          let longitude = service.Photo.gpsConverter(this.exifdata.GPSLongitude, this.exifdata.GPSLongitudeRef);

          console.log(`GPSLatitude: ${latitude}`);
          console.log(`GPSLongitude: ${longitude}`);

          this.center = [latitude, longitude];
          this.markerLatLng = [latitude, longitude];

        });
     } else {
        console.log('Old browser. No support for Filereader API');
      }
    },
    onRemoved() {
      this.image = '';
    },
    attemptUpload() {
      console.log('Attempting uploading..');
      const param = {};
      if (this.image) {
        EXIF.getData(this.image, function () {
          console.log('image info', this);
          console.log('exif data', this.exifdata);

          param.make = this.exifdata.Make;
          param.model = this.exifdata.Model;
          param.width = this.exifdata.PixelXDimension;
          param.height = this.exifdata.PixelYDimension;
          param.GPSLatitude = service.Photo.gpsConverter(this.exifdata.GPSLatitude, this.exifdata.GPSLatitudeRef);
          param.GPSLongitude = service.Photo.gpsConverter(this.exifdata.GPSLongitude, this.exifdata.GPSLongitudeRef);
          param.takenDate = this.exifdata.DateTime;

          this.center = [param.GPSLatitude, param.GPSLongitude];
          this.markerLatLng = [param.GPSLatitude, param.GPSLongitude];

          // console.log(`make: ${this.exifdata.Make}`);
          // console.log(`model: ${this.exifdata.Model}`);
          // console.log(`width: ${this.exifdata.PixelXDimension}`);
          // console.log(`height: ${this.exifdata.PixelYDimension}`);
          // console.log(`GPSLatitude: ${this.exifdata.GPSLatitude}`);
          // console.log(`GPSLatitudeRef: ${this.exifdata.GPSLatitudeRef}`);
          // console.log(`GPSLongitude: ${this.exifdata.GPSLongitude}`);
          // console.log(`GPSLongitudeRef: ${this.exifdata.GPSLongitudeRef}`);
          // console.log(`converted GPSLatitude: ${service.Photo.gpsConverter(this.exifdata.GPSLatitude, this.exifdata.GPSLatitudeRef)}`);
          // console.log(`converted GPSLongitude: ${service.Photo.gpsConverter(this.exifdata.GPSLongitude, this.exifdata.GPSLongitudeRef)}`);
          // console.log(`taken_date: ${this.exifdata.DateTime}`);

          console.log(param);
          console.log(this);

          service.Photo.fileUpload(this, 'file', param)
            .then((response) => {
              if (response.data.success) {
                this.image = '';
                console.log('Image uploaded successfully ✨');
              }
            })
            .catch((err) => {
              console.error(err);
            });
        });
      }
    },
  },
};

</script>


<style scoped>

</style>
