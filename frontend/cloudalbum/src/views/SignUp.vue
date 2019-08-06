<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        align-center
        justify-center
      >
        <v-flex
          xs12
          sm8
          md4
        >
          <v-card class="elevation-12">
            <v-toolbar
              color="primary"
              dark
              flat
            >
              <v-toolbar-title>Sign up</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="inputUsername"
                  i="username"
                  label="Name"
                  name="username"
                  prepend-icon="mdi-account"
                  type="text"
                ></v-text-field>

                <v-text-field
                  v-model="inputEmail"
                  id="email"
                  label="Email"
                  name="email"
                  prepend-icon="mdi-email"
                  type="text"
                ></v-text-field>

                <v-text-field
                  v-model="inputPassword"
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>

                <v-text-field
                  id="password-confirm"
                  label="Password Confirm"
                  name="password-confirm"
                  prepend-icon="mdi-check-bold"
                  type="password"
                ></v-text-field>


              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary"
                     @click="userSignUp()"
              ><v-icon>mdi-send</v-icon> Submit</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-spacer></v-spacer>
              Have already registered?
              <v-btn text small
                     href="/users/signin"
                     color="primary">
                <v-icon>mdi-login</v-icon>Sign in
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>

import axios from 'axios';

export default {
  name: 'SignUp',

  data() {
    return {
      inputUsername: '',
      inputEmail: '',
      inputPassword: '',
    };
  },

  methods: {
    userSignUp() {
      const apiUri = `${process.env.VUE_APP_API}/users/signup`;
      console.log(`API URI: ${apiUri}`);

      axios.post(apiUri, {
        email: this.inputEmail,
        username: this.inputUsername,
        password: this.inputPassword,
      }, {
        dataType: 'json',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
      })
        .then((resp) => {
          console.log(resp.data);
          console.log(resp.status);
          console.log(resp.statusText);
          this.$swal(resp.data);
        })
        .catch((err) => {
          console.error(err);
          this.$swal(`Error:${err.response.status}`);
        });
    },
  },


};


</script>

<style scoped>

</style>
