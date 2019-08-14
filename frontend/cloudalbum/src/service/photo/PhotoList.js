import axiosInstance from '@/plugins/axios';


const photoList = () => {
  const apiUri = '/photos/';

  const config = {
    headers: {
      dataType: 'json',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
    },
  };

  console.log(axiosInstance.defaults.headers.common.Authorization);

  return axiosInstance.get(apiUri, config);
};

export default photoList;
