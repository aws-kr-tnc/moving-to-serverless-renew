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
              :zIndex=0
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
      const self = this;
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
                  this.$router.push({ name: 'upload' });
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
    removeImage() {
      this.$refs.pictureInput.removeImage();
    },
    onRemoved() {
      this.removeImage();
    },
    async attemptUpload() {
      console.log('Attempting uploading..');
      const params = this.makeParam();
      try {
        const resp = await service.Photo.fileUpload(this.$refs.pictureInput.file, 'file', params);
        if (resp.data.ok === true) {
          console.log('Image uploaded successfully ✨');
          this.$router.push({ name: 'photolist' });
        }
      } catch (error) {
        console.error(error);
      }
    },
    makeParam() {
      const param = {};
      param.make = this.exifObj.Make;
      param.model = this.exifObj.Model;
      param.width = this.exifObj.PixelXDimension;
      param.height = this.exifObj.PixelYDimension;
      param.GPSLatitude = service.Photo.gpsConverter(this.exifObj.GPSLatitude, this.exifObj.GPSLatitudeRef);
      param.GPSLongitude = service.Photo.gpsConverter(this.exifObj.GPSLongitude, this.exifObj.GPSLongitudeRef);
      param.takenDate = this.exifObj.DateTimeOriginal;
      param.tags = this.exifObj.tags;
      param.description = this.exifObj.description;

      console.log(`param: ${param}`);

      return param;
    }
  },
};

</script>


<style scoped>

</style>
