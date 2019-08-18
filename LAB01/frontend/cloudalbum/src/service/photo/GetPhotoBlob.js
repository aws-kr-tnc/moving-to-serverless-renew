import axiosInstance from '@/plugins/axios';

const getPhotoBlob = (id, mode) => {
  return axiosInstance.get(`/photos/${id}?mode=${mode}`, {
    responseType: 'blob',
    timeout: 10000,
  });
}

export default getPhotoBlob;
