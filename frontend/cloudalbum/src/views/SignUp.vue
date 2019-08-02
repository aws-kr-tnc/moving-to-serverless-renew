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
                  i="name"
                  label="Name"
                  name="name"
                  prepend-icon="mdi-account"
                  type="text"
                ></v-text-field>

                <v-text-field
                  id="email"
                  label="Email"
                  name="email"
                  prepend-icon="mdi-email"
                  type="text"
                ></v-text-field>

                <v-text-field
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
              <v-btn color="primary"><v-icon>mdi-send</v-icon> Submit</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-spacer></v-spacer>
              Have already registered?
              <v-btn text small href="/users/signin" color="primary"><v-icon>mdi-login</v-icon>Sign in</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
    export default {
        name: "SignUp"
    }
</script>

<style scoped>

</style>
