export default {
  getIsAuth: (state) => {
    console.log(`state.accessToken: ${state.accessToken}`);
    console.log(`state.refreshToken: ${state.refreshToken}`);

    if (!state.accessToken || !state.refreshToken) return false;
    return true;
  },
};
