import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Signin from './views/SignIn.vue';
import Signup from './views/SignUp.vue';
import FileUpload from './views/FileUpload.vue';
import PhotoList from './views/PhotoList.vue';
import store from '@/vuex';

Vue.use(Router);

const requireAuth = () => (from, to, next) => {
  if (store.getters['Auth/getIsAuth']) return next();
  return next('/');
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/users/signin',
      name: 'signin',
      component: Signin,
    },
    {
      path: '/users/signup',
      name: 'signup',
      component: Signup,
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
  ],
});
