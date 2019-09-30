<template>
  <v-app>
    <layout-header></layout-header>
    <layout-body></layout-body>
    <layout-footer></layout-footer>
  </v-app>
</template>

<script>
import LayoutHeader from './components/layout/LayoutHeader.vue';
import LayoutBody from './components/layout/LayoutBody.vue';
import LayoutFooter from './components/layout/LayoutFooter.vue';

export default {
  name: 'App',
  components: { LayoutFooter, LayoutBody, LayoutHeader },
  data: () => ({
    //
  }),
};
</script>
