import { SET_ALL_PHOTO_LIST, DELETE_ONE_PHOTO, SET_IS_LOADING } from '@/vuex/mutation-types';

export default {
  [SET_ALL_PHOTO_LIST](state, data) {
    state.photoList = data;
  },
  [DELETE_ONE_PHOTO](state, id) {
    state.photoList = state.photoList.filter(p => p.id !== id);
  },
  [SET_IS_LOADING](state, data) {
    state.isLoading = data;
  },
};
