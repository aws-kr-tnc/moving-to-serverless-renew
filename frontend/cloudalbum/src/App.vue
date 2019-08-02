<template>
  <v-app>
    <layout-header></layout-header>
    <layout-body></layout-body>
    <layout-footer></layout-footer>
  </v-app>
</template>

<script>
import LayoutHeader from "./components/layout/LayoutHeader";
import LayoutBody from "./components/layout/LayoutBody";
import LayoutFooter from "./components/layout/LayoutFooter";

export default {
  name: 'App',
	components: {LayoutFooter, LayoutBody, LayoutHeader},
	data: () => ({
    //
  })
}
</script>
