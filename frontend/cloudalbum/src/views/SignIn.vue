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
              <v-toolbar-title>Sign in</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  label="Login (Email)"
                  name="email"
                  v-model="inputEmail"
                  prepend-icon="mdi-account"
                  type="text"
                ></v-text-field>

                <v-text-field
                  id="password"
                  label="Password"
                  name="password"
                  v-model="inputPassword"
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="userSignIn()"><v-icon>mdi-send</v-icon> Submit</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-spacer></v-spacer>
              Not yet registered?
              <v-btn text small href="/users/signup"
                     color="primary">
                <v-icon>mdi-account-plus</v-icon>Sign up</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import { signIn } from '@/service';

export default {
  name: 'SignIn',

  data() {
    return {
      inputEmail: '',
      inputPassword: '',
    };
  },

  methods: {
    async userSignIn() {
      try {
        const resp = await signIn(this.inputEmail, this.inputPassword);
        console.log(resp.data)
        this.$router.push({ name: 'photolist' });
      } catch (err) {
        this.$swal(`Error:${err.response.status}`);
      }
    },
  },

};
</script>

<style scoped>

</style>
