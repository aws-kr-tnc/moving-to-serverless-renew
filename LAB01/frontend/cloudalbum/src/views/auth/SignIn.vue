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
              <v-form
                ref="form"
                lazy-validation
              >
                <v-text-field
                  label="Login (Email)"
                  name="email"
                  v-model="inputEmail"
                  prepend-icon="mdi-account"
                  type="text"
                  :rules="requiredRule"
                  @keyup.enter="userSignIn()"
                ></v-text-field>
                <v-text-field
                  id="password"
                  label="Password"
                  name="password"
                  v-model="inputPassword"
                  prepend-icon="mdi-lock"
                  type="password"
                  :rules="requiredRule"
                  @keyup.enter="userSignIn()"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                @click="userSignIn()"
              >
                <v-icon>mdi-send</v-icon> Submit
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-spacer></v-spacer>
              Not yet registered?
              <v-btn text small @click="moveToSignup"
                     color="primary">
                <v-icon>mdi-account-plus</v-icon>Sign up
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'SignIn',

  data() {
    return {
      inputEmail: '',
      inputPassword: '',
      requiredRule: [v => !!v || 'Required!'],
    };
  },
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),
    async userSignIn() {
      if (!this.isValide()) return false;
      try {
        const resp = await this.getTokens({ email: this.inputEmail, password: this.inputPassword });
        if (resp.status !== 200) this.popupAlert(resp);
        if (this.isAuthenticated) this.$router.push({ name: 'photolist' });
      } catch (err) {
        this.popupAlert(err);
      }
      return true;
    },
    popupAlert(resp) {
      let msg = '';
      if (resp.status === 400) msg = '400 error';
      if (resp.status === 500) msg = resp.body;
      if (resp.status === undefined) msg = resp;
      this.$swal(
        {
          type: 'error',
          title: 'Oops...',
          text: `Something went wrong! (${msg})`,
        },
      );
    },
    isValide() {
      if (this.$refs.form.validate()) return true;
      this.$swal({
        title: 'Please check your input value.',
        type: 'warning',
      });
      return false;
    },
    moveToSignup() {
      this.$router.push({ name: 'signup' });
    },
  },
};
</script>
