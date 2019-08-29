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
              <v-form
                ref="form"
                lazy-validation
              >
                <v-text-field
                  v-model="inputUsername"
                  i="username"
                  label="Name"
                  name="username"
                  prepend-icon="mdi-account"
                  type="text"
                  :rules="requiredRule"
                  @keyup.enter="userSignUp()"
                ></v-text-field>
                <v-text-field
                  v-model="inputEmail"
                  id="email"
                  label="Email"
                  name="email"
                  prepend-icon="mdi-email"
                  type="text"
                  :rules="requiredRule"
                  @keyup.enter="userSignUp()"
                ></v-text-field>
                <v-text-field
                  v-model="inputPassword"
                  id="password"
                  label="Password"
                  name="password"
                  prepend-icon="mdi-lock"
                  type="password"
                  :rules="requiredRule"
                  @keyup.enter="userSignUp()"
                ></v-text-field>
                <v-text-field
                  v-model="passwordConfirm"
                  id="password-confirm"
                  label="Password Confirm"
                  name="password-confirm"
                  prepend-icon="mdi-check-bold"
                  type="password"
                  :rules="passwordConfirmationRules"
                  @keyup.enter="userSignUp()"
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
                     @click="moveToSignin"
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
      passwordConfirm: '',
      requiredRule: [v => !!v || 'Required!'],
    };
  },
  computed: {
    passwordConfirmationRules() {
      return [
        () => (this.inputPassword === this.passwordConfirm) || 'Password must match',
        v => !!v || 'Confirmation password is required',
      ];
    },
  },
  methods: {
    async userSignUp() {
      if (!this.isValide()) return false;
      try {
        // eslint-disable-next-line max-len
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
        let errMsg = '';
        if (!err.response) errMsg = 'Error: Network Connection Error!';
        else errMsg = err.response.data.Message;
        this.$swal(
          {
            type: 'error',
            title: 'Something went wrong!',
            text: errMsg,
          },
        );
      }
      return true;
    },
    moveToSignin() {
      this.$router.push({ name: 'signin' });
    },
    isValide() {
      if (this.$refs.form.validate()) return true;
      this.$swal({
        title: 'Please check your input value.',
        type: 'warning',
      });
      return false;
    },
  },
};
</script>

<style scoped>

</style>
