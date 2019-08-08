import services from '@/service';
import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN, SET_ERROR_MESSAGE } from '@/vuex/mutation-types';

const setAccessToken = ({ commit }, data) => {
  commit(SET_ACCESS_TOKEN, data);
};

const setRefreshToken = ({ commit }, data) => {
  commit(SET_REFRESH_TOKEN, data);
};

const setErrorMessage = ({ commit }, data) => {
  commit(SET_ERROR_MESSAGE, data);
};

const responseCheck = (error) => {
  let msg = 'Something went wrong!';
  if (typeof error.response.data !== 'undefined') {
    if (error.response.data.ok === false) msg = 'Already registerd!';
    return msg;
  }
  return msg;
};

const getTokens = (store, { email, password }) => {
  services.Auth.signIn(email, password)
    .then((resp) => {
      setAccessToken(store, resp.data.accessToken);
      setRefreshToken(store, resp.data.refreshToken);
    })
    .catch((err) => {
      const msg = responseCheck(err);
      setErrorMessage(store, msg);
    });
};

export default {
  getTokens,
};
