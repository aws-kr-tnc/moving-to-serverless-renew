<template>
  <v-container grid-list-md text-center>
    <v-layout wrap>
      <v-flex xs12>
        <v-card dark color="secondary">
          <v-container>
            <picture-input
              ref="pictureInput"
              margin="16"
              width="300"
              height="300"
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
          <v-container v-if="seen">
              <l-map
                class="l-map"
                :zoom="zoom"
                :center="center"
              >
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="center" ></l-marker>
              </l-map>
             <v-layout align-left>
              <v-chip
                class="ma-2"
                label
                text-color="white"
                small
                color="primary"
              >
                <v-icon left>mdi-map</v-icon>
                {{address}}
              </v-chip>
             </v-layout>
          </v-container>
        </v-card>
      </v-flex>
      <v-flex xs12>
        <v-card dark color="secondary">
            <v-card-text>
              <v-container v-if="seen">
                <v-layout align-left>
                  <v-chip
                    class="ma-2"
                    small
                    color="primary"
                    label
                    text-color="white"
                  >
                    <v-icon left>mdi-tag-multiple</v-icon>
                    EXIF
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    close
                    color="teal"
                    text-color="white"
                    close-icon="mdi-check-circle"
                  >
                    {{country}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    close
                    color="teal"
                    text-color="white"
                    close-icon="mdi-check-circle"
                  >
                    {{city}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    close
                    color="teal"
                    text-color="white"
                    close-icon="mdi-check-circle"
                  >
                    {{make}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    close
                    color="teal"
                    text-color="white"
                    close-icon="mdi-check-circle"
                  >
                    {{model}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    close
                    color="teal"
                    text-color="white"
                    close-icon="mdi-check-circle"
                  >
                    {{width}} x {{height}}
                  </v-chip>
                </v-layout>
              </v-container>
              <v-form
                ref="form"
                lazy-validation>
                <v-text-field
                  v-model = "tags"
                  :rules="requiredRule"
                  id="tags"
                  label="Tags (separated by comma)"
                  name="tags"
                  prepend-icon="mdi-tag-multiple"
                  type="text"
                ></v-text-field>
                <v-text-field
                  v-model = "description"
                  :rules="requiredRule"
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
              <v-btn color="secondary" target="_blank"
                     href="https://d2r3btx883i63b.cloudfront.net/temp/sample-photo.zip" >
                <v-icon>mdi-arrow-down-bold-circle</v-icon> Sample photo DOWN
              </v-btn>
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
import PictureInput from 'vue-picture-input';
import EXIF from 'exif-js';
import * as esri from 'esri-leaflet-geocoder';
import service from '@/service';

const photoApi = service.Photo;

export default {
  name: 'FileUpload',
  components: {
    PictureInput,
  },
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 14,
      exifObj: {},
      tags: '',
      description: '',
      seen: false,
      address: '',
      city: '',
      country: '',
      model: '',
      make: '',
      width: '',
      height: '',
      filename_orig: '',
      requiredRule: [v => !!v || 'Required!'],
    };
  },
  computed: {
    latitude() {
      if (JSON.stringify(this.exifObj) === JSON.stringify({})) return 0;
      let result;
      try {
        result = photoApi.gpsConverter(this.exifObj.GPSLatitude, this.exifObj.GPSLatitudeRef);
      } catch (e) {
        console.error(e);
        this.noLatLng();
      }
      return result;
    },
    longitude() {
      if (JSON.stringify(this.exifObj) === JSON.stringify({})) return 0;
      let result;
      try {
        result = photoApi.gpsConverter(this.exifObj.GPSLongitude, this.exifObj.GPSLongitudeRef);
      } catch (e) {
        console.error(e);
        this.noLatLng();
      }
      return result;
    },
    center() {
      return [this.latitude, this.longitude];
    },
  },
  methods: {
    onChange() {
      console.log('New picture loaded');
      const self = this;
      try {
        if (!this.$refs.pictureInput.file) throw new Error('Old browser. No support for Filereader API');

        EXIF.getData(this.$refs.pictureInput.file, function () {
          self.exifObj = this.exifdata;
          self.filename_orig = this.name;

          if (Object.keys(self.exifObj).length === 0) {
            self.popupNoExif();
            self.seen = false;
            return;
          }
          self.reverseGeocoding(this.exifdata);
          self.seen = true;
        });
      } catch (error) {
        console.error(error);
      }
    },
    removeImage() {
      this.$refs.pictureInput.removeImage();
    },
    async attemptUpload() {
      if (!this.isValide()) return false;
      console.log('Attempting uploading..');
      const params = this.makeParam();
      try {
        const resp = await photoApi.fileUpload(this.$refs.pictureInput.file, 'file', params);
        console.log(resp);
        // console.log(resp.data.ok);
        // if (resp.data.ok !== true) throw new Error(resp);
        console.log('Image uploaded successfully ✨');
        this.$swal(
          {
            title: 'Upload completed!',
            type: 'success',
            onClose: () => {
              this.$router.push({ name: 'photolist' });
            },
          },
        );
      } catch (error) {
        console.log(error);
      }
    },
    popupNoExif() {
      this.removeImage();
      this.$swal(
        {
          title: 'WARNING',
          text: 'This image has no EXIF information!',
          type: 'warning',
          onClose: () => {
            this.seen = false;
            this.$router.push({ name: 'upload' });
          },
        },
      );
    },
    reverseGeocoding(exif) {
      try {
        esri.reverseGeocode()
          .latlng([
            photoApi.gpsConverter(exif.GPSLatitude, exif.GPSLatitudeRef),
            photoApi.gpsConverter(exif.GPSLongitude, exif.GPSLongitudeRef),
          ])
          .run((error, result) => {
            console.log(result);
            this.address = result.address.LongLabel;
            this.city = result.address.City;
            this.country = result.address.CountryCode;
            // Additional information assign from EXIF.
            this.make = exif.Make;
            this.model = exif.Model;
            this.width = exif.PixelXDimension;
            this.height = exif.PixelYDimension;
            this.tags = `${this.country}, ${this.city}, ${this.exifObj.Make}, ${this.exifObj.Model}, ${this.width} x ${this.height}`;
          });
      } catch (error) {
        console.error(error);
        this.noLatLng();
      }
    },
    makeParam() {
      const param = {};
      param.make = this.exifObj.Make;
      param.model = this.exifObj.Model;
      param.width = this.exifObj.PixelXDimension;
      param.height = this.exifObj.PixelYDimension;
      param.geotag_lat = photoApi.gpsConverter(this.exifObj.GPSLatitude, this.exifObj.GPSLatitudeRef);
      param.geotag_lng = photoApi.gpsConverter(this.exifObj.GPSLongitude, this.exifObj.GPSLongitudeRef);
      param.takenDate = this.exifObj.DateTimeOriginal;
      param.tags = this.tags;
      param.desc = this.description;
      param.city = this.city;
      param.address = this.address;
      param.nation = this.country;
      param.filename_orig = this.filename_orig;

      console.log(`param: ${param}`);

      return param;
    },
    isValide() {
      if (!this.$refs.form.validate() || !this.$refs.pictureInput.file) {
        this.$swal(
          {
            title: 'Please insert your tags and description',
            type: 'warning',
          },
        );
        return false;
      }
      return true;
    },
    noLatLng() {
      console.log('This image has no GPS information!');
    },
  },
};
</script>
<style scoped>
.l-map {
  height: 305px;
  width: 100%;
}
</style>
