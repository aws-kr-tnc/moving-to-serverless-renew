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
            <v-card-text>
              MAP
            </v-card-text>
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
              <v-btn color="primary" @click="attemptUpload" v-bind:class="{ disabled: !image }">
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
    onChange(image) {
      console.log('New picture selected!');
      this.image = image;
      console.log(`image: ${this.image}`);

      if (image) {
        EXIF.getData(this.$refs.pictureInput.file, function () {
          console.log('image info', this);
          console.log('exif data', this.exifdata);
        });

        console.log('Picture loaded.');
        console.log();
        this.image = image;
        service.Photo.fileUpload();
      } else {
        console.log('FileReader API not supported: use the <form>, Luke!');
      }
    },
    onRemoved() {
      this.image = '';
    },
    attemptUpload() {
      if (this.image) {
        service.Photo.fileUpload(this.image, 'myfile.jpg')
          .then((response) => {
            if (response.data.success) {
              this.image = '';
              console.log('Image uploaded successfully ✨');
            }
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
  },
};

</script>


<style scoped>

</style>
