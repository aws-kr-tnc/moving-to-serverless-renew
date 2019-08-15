import axiosInstance from '@/plugins/axios';

const getPhotoBlob = (id) => {
  return axiosInstance.get(`/photos/${id}?mode=original`, {
    responseType: 'blob',
    timeout: 10000,
  });
}

export default getPhotoBlob;
