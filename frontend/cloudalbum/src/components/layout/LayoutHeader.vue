<template>
  <div>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <v-list-item @click="">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>HOME</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="">
          <v-list-item-action>
            <v-icon>mdi-shield-account</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Hello, USERNAME</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="">
          <v-list-item-action>
            <v-icon>mdi-map-marker</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Map</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click="">
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Sign out</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>CloudAlbum</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-layout
        align-center
        style="max-width: 650px"
      >
        <v-text-field
          :append-icon-cb="() => {}"
          placeholder="Search..."
          single-line
          append-icon="mdi-file-search"
          color="white"
          hide-details
        ></v-text-field>
      </v-layout>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "LayoutHeader",
  data: () => ({
    drawer: null
  })
}
</script>

<style scoped>

</style>
