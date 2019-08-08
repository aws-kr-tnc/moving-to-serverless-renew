export default {
  getIsAuth: (state) => {
    if (!state.accessToken || !state.refreshToken) return false;
    return true;
  },
};
