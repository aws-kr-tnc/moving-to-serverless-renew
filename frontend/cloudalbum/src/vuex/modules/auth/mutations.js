import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN } from '@/vuex/mutation-types';

export default {
  [SET_ACCESS_TOKEN](state, data) {
    state.accessToken = data;
  },
  [SET_REFRESH_TOKEN](state, data) {
    state.refreshToken = data;
  },
};
