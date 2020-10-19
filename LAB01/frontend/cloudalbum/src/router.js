import Vue from 'vue';
import Router from 'vue-router';
import store from '@/vuex';
import SignIn from './views/auth/SignIn.vue';

Vue.use(Router);

const requireAuth = () => (from, to, next) => {
  if (store.getters['Auth/isAuthenticated']) return next();
  return next('/');
};

export default new Router({
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
      component: () => import('@/views/auth/SignOut'),
      beforeEnter: requireAuth(),
    },
    {
      path: '/users/signup',
      name: 'signup',
      component: () => import('@/views/auth/SignUp'),
    },
    {
      path: '/photos/upload',
      name: 'upload',
      component: () => import('@/views/FileUpload'),
      beforeEnter: requireAuth(),
    },
    {
      path: '/photos',
      name: 'photolist',
      component: () => import('@/views/PhotoList'),
      beforeEnter: requireAuth(),
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('@/views/Map'),
      beforeEnter: requireAuth(),
    },
  ],
});
