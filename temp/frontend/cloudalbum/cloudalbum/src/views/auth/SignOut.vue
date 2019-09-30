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
import { mapMutations } from 'vuex';
import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN } from '@/vuex/mutation-types';
import service from '@/service';

export default {
  name: 'SignOut',
  methods: {
    ...mapMutations('Auth', [SET_ACCESS_TOKEN, SET_REFRESH_TOKEN]),
    async signOut() {
      try {
        const resp = await service.Auth.signOut();
        if (!resp.data.ok) return;
        console.log('Signout successfully ✨');
        this[SET_ACCESS_TOKEN](null);
        this[SET_REFRESH_TOKEN](null);
        this.$swal(
          {
            title: 'Success!',
            text: 'Your account has been signed out successfully.',
            type: 'success',
            onClose: () => {
              this.$router.push({ name: 'signin' });
            },
          },
        );
      } catch (error) {
        console.log(error.response);
        this[SET_ACCESS_TOKEN](null);
        this[SET_REFRESH_TOKEN](null);
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
      } else {
        this.$router.push({ name: 'photolist' });
      }
    });
  },
};
</script>
