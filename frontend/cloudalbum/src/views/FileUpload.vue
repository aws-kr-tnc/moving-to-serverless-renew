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
              <l-map style="height: 305px; width: 100%" :zoom="zoom" :center="center">
                <l-tile-layer :url="url"></l-tile-layer>
                <l-marker :lat-lng="markerLatLng" ></l-marker>
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
<!--          <v-container v-if="seen === false">-->
<!--            <div style="border: 1px solid gray; padding: 10px; height: 350px; overflow: auto;">-->
<!--              MAP-->
<!--            </div>-->
<!--          </v-container>-->
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card dark color="secondary">
            <v-card-text>
              <v-form>

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
                      @click:close="addTag;"
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
                      @click:close="addTag"
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
                      @click:close="addTag"
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
                      @click:close="addTag"
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
                      @click:close="addTag"
                    >
                      {{width}} x {{height}}
                    </v-chip>

                  </v-layout>
                </v-container>

                <v-text-field
                  v-model = "tags"
                  :rules="['Required']"
                  id="tags"
                  label="Tags (separated by comma)"
                  name="tags"
                  prepend-icon="mdi-tag-multiple"
                  type="text"
                ></v-text-field>

                <v-text-field
                  v-model = "description"
                  :rules="['Required']"
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
import * as esri from 'esri-leaflet-geocoder';
import service from '@/service';

export default {
  name: 'FileUpload',
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 14,
      // center: [45.43163333333333, 12.320180555555556],
      // markerLatLng: [45.43163333333333, 12.320180555555556],
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
    };
  },
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
    latitude() {
      let result;
      try {
        result = service.Photo.gpsConverter(this.exifObj.GPSLatitude, this.exifObj.GPSLatitudeRef);
      } catch (e) {
        console.log(e);
        this.noLatLng();
      }
      return result;
    },
    longitude() {
      let result;
      try {
        result = service.Photo.gpsConverter(this.exifObj.GPSLongitude, this.exifObj.GPSLongitudeRef);
      } catch (e) {
        console.log(e);
        this.noLatLng();
      }
      return result;
    },
    center() {
      if (JSON.stringify(this.exifObj) === JSON.stringify({})) {
        return [45.43163333333333, 12.320180555555556];
      }
      return [this.latitude, this.longitude];
    },
    markerLatLng() {
      return this.center;
    },
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
          console.log(self);
          console.log(this.exifdata);
          self.exifObj = this.exifdata;
          if (Object.keys(self.exifObj).length === 0) {
            self.popupNoExif();
          }
          self.reverseGeocoding(this.exifdata);
          self.seen = true;
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
      if (!this.isValide()) return false;
      console.log('Attempting uploading..');
      const params = this.makeParam();
      try {
        const resp = await service.Photo.fileUpload(this.$refs.pictureInput.file, 'file', params);
        if (resp.data.ok === true) {
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
        }
      } catch (error) {
        console.error(error);
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
            service.Photo.gpsConverter(exif.GPSLatitude, exif.GPSLatitudeRef),
            service.Photo.gpsConverter(exif.GPSLongitude, exif.GPSLongitudeRef),
          ])
          .run((error, result, response) => {
            console.log(result)
            this.address = result.address.LongLabel;
            this.city = result.address.City;
            this.country = result.address.CountryCode;
            //Additional information assign from EXIF.
            this.make = exif.Make;
            this.model = exif.Model;
            this.width = exif.PixelXDimension;
            this.height = exif.PixelYDimension;
            this.tags = `${this.country}, ${this.city}, ${this.exifObj.Make}, ${this.exifObj.Model}, ${this.width} x ${this.height}`;
          });
      } catch {
        this.noLatLng();
      }
    },
    addTag(tag) {
      console.log(tag);
    },
    makeParam() {
      const param = {};
      param.make = this.exifObj.Make;
      param.model = this.exifObj.Model;
      param.width = this.exifObj.PixelXDimension;
      param.height = this.exifObj.PixelYDimension;
      param.geotag_lat = service.Photo.gpsConverter(this.exifObj.GPSLatitude, this.exifObj.GPSLatitudeRef);
      param.geotag_lng = service.Photo.gpsConverter(this.exifObj.GPSLongitude, this.exifObj.GPSLongitudeRef);
      param.takenDate = this.exifObj.DateTimeOriginal;
      param.tags = this.tags;
      param.desc = this.description;
      param.city = this.city;
      param.address = this.address;
      param.nation = this.country;

      console.log(`param: ${param}`);

      return param;
    },
    isValide() {
      if (this.tags.length === 0 || this.description.length === 0 || this.$refs.pictureInput.file === undefined) {
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
      // this.$swal(
      //   {
      //     title: 'WARNING',
      //     text: 'This image has no GPS information!',
      //     type: 'warning',
      //     onClose: () => {
      //       this.$router.push({ name: 'upload' });
      //     },
      //   },
      // );
    },
  },
};

</script>


<style scoped>

</style>
