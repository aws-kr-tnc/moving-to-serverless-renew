export default {
  isNoData: (state) => {
    if (state.photoList.length === 0) return true;
    return false;
  },
};
