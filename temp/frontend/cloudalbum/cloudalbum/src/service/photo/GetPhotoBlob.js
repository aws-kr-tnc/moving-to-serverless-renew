import axiosInstance from '@/plugins/axios';

const getPhotoBlob = (id, mode) => axiosInstance.get(`/photos/${id}?mode=${mode}`, {
  responseType: 'blob',
  timeout: process.env.VUE_APP_TIMEOUT,
});

export default getPhotoBlob;
