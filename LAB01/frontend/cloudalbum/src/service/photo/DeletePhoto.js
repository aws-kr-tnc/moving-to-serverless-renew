import axiosInstance from '@/plugins/axios';

const deletePhoto = (id) => {
  const apiUri = `/photos/${id}`;

  const config = {
    headers: {
      dataType: 'json',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
    },
  };

  console.log(axiosInstance.defaults.headers.common.Authorization);

  return axiosInstance.delete(apiUri, config);
};

export default deletePhoto;
