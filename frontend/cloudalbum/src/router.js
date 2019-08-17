import Vue from 'vue';
import Router from 'vue-router';
import Map from './views/Map.vue';
import SignIn from './views/SignIn.vue';
import SignOut from './views/SignOut.vue';
import SignUp from './views/SignUp.vue';
import FileUpload from './views/FileUpload.vue';
import PhotoList from './views/PhotoList.vue';
import store from '@/vuex';

Vue.use(Router);

const requireAuth = () => (from, to, next) => {
  if (store.getters['Auth/isAuthenticated']) return next();
  return next('/');
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: SignIn,
    },
    {
      path: '/users/signin',
      name: 'signin',
      component: SignIn,
    },
    {
      path: '/users/signout',
      name: 'signout',
      component: SignOut,
      beforeEnter: requireAuth(),
    },
    {
      path: '/users/signup',
      name: 'signup',
      component: SignUp,
    },
    {
      path: '/photos/upload',
      name: 'upload',
      component: FileUpload,
      beforeEnter: requireAuth(),
    },
    {
      path: '/photos',
      name: 'photolist',
      component: PhotoList,
      beforeEnter: requireAuth(),
    },
    {
      path: '/map',
      name: 'map',
      component: Map,
      beforeEnter: requireAuth(),
    },
  ],
});
