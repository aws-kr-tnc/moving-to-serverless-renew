import { SET_ALL_PHOTO_LIST } from '@/vuex/mutation-types';

export default {
  [SET_ALL_PHOTO_LIST](state, data) {
    state.photoList = data;
  },
};
