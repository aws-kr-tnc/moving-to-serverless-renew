import axiosInstance from '@/plugins/axios';


const signOut = () => {
  const apiUri = '/users/signout';

  const config = {
    headers: {
      dataType: 'json',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
    },
  };

  console.log(axiosInstance.defaults.headers.common.Authorization);

  return axiosInstance.post(apiUri, config);
};

export default signOut;
