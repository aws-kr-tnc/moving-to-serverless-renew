import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN, SET_ERROR_MESSAGE } from '@/vuex/mutation-types';

export default {
  [SET_ACCESS_TOKEN](state, data) {
    state.accessToken = data;
  },
  [SET_REFRESH_TOKEN](state, data) {
    state.refreshToken = data;
  },
  [SET_ERROR_MESSAGE](state, data) {
    state.errorMessage = data;
  },
};
