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

        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import service from '@/service';

export default {
  name: 'SignOut',

  data() {
    return {
    };
  },
  computed: {
    ...mapGetters('Auth', [
      'isAuthenticated',
    ]),
  },
  methods: {
    ...mapActions('Auth', ['getTokens']),

    async signOut() {
      try {
        const resp = await service.Auth.signOut();
        if (resp.data.ok === true) {
          console.log('Signout successfully ✨');
          this.$swal(
            {
              title: 'Success!',
              text: 'Your account has been signed out successfully.',
              type: 'success',
              onClose: () => {
                this.$store.state.accessToken = null;
                this.$router.push({ name: 'signin' });
              },
            },
          );
        }
      } catch (error) {
        console.log(error.response);
        this.$store.state.accessToken = null;
        this.$router.push({ name: 'signin' });
      }
    },
  },

  mounted() {
    console.log('signout loaded');
    this.$swal({
      title: 'Are you sure?',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, sign-out!',
    }).then((result) => {
      if (result.value) {
        this.signOut();
        // this.$swal({
        //   title: 'Success!',
        //   text: 'Your account has been signed out successfully.',
        //   type: 'success',
        //   onClose: () => {
        //     this.signOut();
        //     // this.$router.push({ name: 'signin' });
        //   },
        // });
      } else {
        this.$router.push({ name: 'photolist' });
      }
    });
  },
};
</script>

<style scoped>

</style>
