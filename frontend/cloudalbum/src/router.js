import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Signin from "./views/SignIn.vue"
import Signup from "./views/SignUp.vue"
import FileUpload from "./views/FileUpload.vue"

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/users/signin',
      name: 'signin',
      component: Signin
    },
    {
      path: '/users/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/photos/upload',
      name: 'upload',
      component: FileUpload
    }

  ]
})
