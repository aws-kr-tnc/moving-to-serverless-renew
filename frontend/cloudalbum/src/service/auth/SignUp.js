import axios from '@/plugins/axios';

const signUp = (email, username, password) => {
  const apiUri = '/users/signup';
  console.log(`API URI: ${apiUri}`);

  axios.post(apiUri, {
    email,
    username,
    password,
  }, {
    dataType: 'json',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  })
    .then((resp) => {
      console.log(resp.data);
      console.log(resp.status);
      console.log(resp.statusText);
      this.$swal(resp.data);
    })
    .catch((err) => {
      console.error(err);
      this.$swal(`Error:${err.response.status}`);
    });
};

export default signUp;
