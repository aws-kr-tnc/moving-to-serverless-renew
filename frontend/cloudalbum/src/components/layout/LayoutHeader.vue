<template>
  <div>
<!--    <v-navigation-drawer-->
<!--      v-model="drawer"-->
<!--      app-->
<!--      clipped-->
<!--    >-->
<!--      <v-list dense>-->
<!--        <v-list-item @click="">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-home</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>HOME</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->

<!--        <v-list-item @click="">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-shield-account</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>Hello, USERNAME</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->

<!--        <v-list-item @click="moveToUpload">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-cloud-upload</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>Upload</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->

<!--        <v-list-item @click="">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-map-marker</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>Map</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->

<!--        <v-list-item @click="">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-logout</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>Sign out</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->

<!--      </v-list>-->
<!--    </v-navigation-drawer>-->

    <v-app-bar
      app
      clipped-left
    >
<!--      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>-->
      <v-toolbar-title>
        <v-icon>mdi-image-plus</v-icon>
        CloudAlbum
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-layout
        align-center
        style="max-width: 650px"
      >
      <v-spacer></v-spacer>
<!--        <v-text-field-->
<!--          :append-icon-cb="() => {}"-->
<!--          placeholder="Search..."-->
<!--          single-line-->
<!--          append-icon="mdi-file-search"-->
<!--          color="white"-->
<!--          hide-details-->
<!--        ></v-text-field>-->

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" @click="moveToList">
          <v-icon>mdi-format-list-bulleted-square</v-icon>
        </v-btn>
      </template>
      <span>List</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" @click="moveToUpload">
          <v-icon>mdi-cloud-upload</v-icon>
        </v-btn>
      </template>
      <span>Upload</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" @click="moveToMap">
          <v-icon>mdi-map-marker</v-icon>
        </v-btn>
      </template>
      <span>Map</span>
    </v-tooltip>

<!--    <v-tooltip bottom>-->
<!--      <template v-slot:activator="{ on }">-->
<!--        <v-btn icon v-on="on">-->
<!--          <v-icon>mdi-magnify</v-icon>-->
<!--        </v-btn>-->
<!--      </template>-->
<!--      <span>Search</span>-->
<!--    </v-tooltip>-->

    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" @click="signOut">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </template>
      <span>Sign-out</span>
    </v-tooltip>

      </v-layout>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: 'LayoutHeader',
  data: () => ({
    drawer: null,
  }),
  methods: {
    moveToUpload() {
      this.$router.push({ name: 'upload' });
    },
    moveToList() {
      this.$router.push({ name: 'photolist' });
    },
    moveToMap() {
      this.$router.push({ name: 'map' });
    },
    signOut() {
      // this.$swal({
      //   title: 'Are you sure?',
      //   type: 'warning',
      //   showCancelButton: true,
      //   confirmButtonColor: '#3085d6',
      //   cancelButtonColor: '#d33',
      //   confirmButtonText: 'Yes, sign-out!'
      // }).then((result) => {
      //   if (result.value) {
      //     this.$swal(
      //       'Success!',
      //       'Your account has been signed out successfully.',
      //       'success',
      //     );
      //   }
      //   this.$router.push({ name: 'signin' });
      // });
      this.$router.push({ name: 'signout' });
    },
  },
};
</script>

<style scoped>

</style>
