import axiosInstance from '@/plugins/axios';

const signUp = (email, username, password) => {
  const apiUri = '/users/signup';

  return axiosInstance.post(apiUri, {
    email,
    username,
    password,
  }, {
    dataType: 'json',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};

export default signUp;
