import services from '@/service';
import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN } from '@/vuex/mutation-types';

const setAccessToken = ({ commit }, data) => {
  commit(SET_ACCESS_TOKEN, data);
};

const setRefreshToken = ({ commit }, data) => {
  commit(SET_REFRESH_TOKEN, data);
};

const getTokens = (store, { email, password }) => {
  services.Auth.signIn(email, password)
    .then((resp) => {
      setAccessToken(store, resp.data.accessToken);
      setRefreshToken(store, resp.data.refreshToken);
    })
    .catch((err) => {
      console.error(err);
    });
};

export default {
  getTokens,
};
