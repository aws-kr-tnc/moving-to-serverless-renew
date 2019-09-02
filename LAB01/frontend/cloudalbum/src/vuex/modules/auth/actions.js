import services from '@/service';
import axios from '@/plugins/axios';
import { SET_ACCESS_TOKEN, SET_REFRESH_TOKEN } from '@/vuex/mutation-types';

const setAccessToken = ({ commit }, data) => {
  commit(SET_ACCESS_TOKEN, data);
  axios.defaults.headers.common.Authorization = `Bearer ${data}`;
};

const setRefreshToken = ({ commit }, data) => {
  commit(SET_REFRESH_TOKEN, data);
};

// eslint-disable-next-line consistent-return
const getTokens = async (store, { email, password }) => {
  try {
    const resp = await services.Auth.signIn(email, password);
    setAccessToken(store, resp.data.accessToken);
    setRefreshToken(store, resp.data.refreshToken);
    console.log(resp);
    return resp;
  } catch (error) {
    return error;
  }
};

export default {
  getTokens,
};
