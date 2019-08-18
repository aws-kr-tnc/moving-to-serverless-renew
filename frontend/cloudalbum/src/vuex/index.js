import Vue from 'vue';
import Vuex from 'vuex';
import Auth from '@/vuex//modules/auth';
import Photo from '@/vuex/modules/photo';

Vue.use(Vuex);

export default new Vuex.Store({
  namespaced: true,
  modules: {
    Auth,
    Photo,
  },
});
