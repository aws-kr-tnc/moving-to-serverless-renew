import axios from '@/plugins/axios';

const signUp = (email, username, password) => {
  const apiUri = '/users/signup';
  console.log(`API URI: ${apiUri}`);

  return axios.post(apiUri, {
    email,
    username,
    password,
  }, {
    dataType: 'json',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};

export default signUp;
