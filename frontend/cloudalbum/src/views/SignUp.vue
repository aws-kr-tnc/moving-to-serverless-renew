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
import service from '@/service';

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
    async userSignUp() {
      try {
        const resp = await service.Auth.signUp(this.inputEmail, this.inputUsername, this.inputPassword);
        console.log(resp);
        this.$swal(
          {
            title: 'Sign-up completed!',
            type: 'success',
            onClose: () => {
              this.$router.push({ name: 'signin' });
            },
          },
        );
      } catch (err) {
        this.$swal(
          {
            type: 'error',
            title: 'Oops...',
            text: 'Already registerd? or something went wrong!',
            footer: '<a href="/users/signup">Retry</a>',
          },
        );
      }
    },
  },
};
</script>

<style scoped>

</style>
