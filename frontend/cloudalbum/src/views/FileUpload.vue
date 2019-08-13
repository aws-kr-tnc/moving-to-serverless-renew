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
              zIndex="0"
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
                  v-model = "tags"
                  id="tags"
                  label="Tags (separated by comma)"
                  name="tags"
                  prepend-icon="mdi-tag-multiple"
                  type="text"
                ></v-text-field>

                <v-text-field
                  v-model = "description"
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
      zoom: 14,
      center: [45.43163333333333, 12.320180555555556],
      markerLatLng: [45.43163333333333, 12.320180555555556],
      exifObj: {},
      tags: '',
      description: '',
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
      let self = this;
      if (this.$refs.pictureInput.file) {
        EXIF.getData(this.$refs.pictureInput.file, function () {
          self.tags = '';
          console.log(self);
          console.log(this.exifdata);
          self.exifObj = this.exifdata;

          if (Object.keys(self.exifObj).length === 0) {
            self.image = '';
            self.$swal(
              {
                title: 'WARNING',
                text: 'This image has no EXIF information!',
                type: 'warning',
                onClose: () => {
                  self.$router.push({ name: 'upload' });
                },
              },
            );
          } else {
            const latitude = service.Photo.gpsConverter(self.exifObj.GPSLatitude, self.exifObj.GPSLatitudeRef);
            const longitude = service.Photo.gpsConverter(self.exifObj.GPSLongitude, self.exifObj.GPSLongitudeRef);
            self.center = [latitude, longitude];
            self.markerLatLng = [latitude, longitude];
            self.tags = `EXIF, ${self.exifObj.Make}, ${self.exifObj.Model}, ${self.exifObj.DateTime}`;
            console.log(self.tags);
          }
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
      let self = this;
      const param = {};
      if (this.image) {
        EXIF.getData(this.image, function () {
          console.log('image info', this);
          console.log('exif data', this.exifdata);
          const exif = this.exifdata;
          param.make = exif.Make;
          param.model = exif.Model;
          param.width = exif.PixelXDimension;
          param.height = exif.PixelYDimension;
          param.GPSLatitude = service.Photo.gpsConverter(exif.GPSLatitude, exif.GPSLatitudeRef);
          param.GPSLongitude = service.Photo.gpsConverter(exif.GPSLongitude, exif.GPSLongitudeRef);
          param.takenDate = exif.DateTime;
          param.tags = self.tags;
          param.description = self.description;
          console.log(param);

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
