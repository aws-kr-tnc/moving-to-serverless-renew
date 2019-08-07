import axios from '@/plugins/axios';
import Swal from 'sweetalert2'

const signIn = (email, password) => {
  const apiUri = '/users/signin';
  console.log(`API URI: ${apiUri}`);

  axios.post(apiUri, {
    email,
    password,
  }, {
    dataType: 'json',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  })
    .then((resp) => {
      console.log(resp.data);
      console.log(resp.status);
      console.log(resp.statusText);
      // this.$swal(resp.data);
    })
    .catch((err) => {
      console.error(err);
      // this.$swal(`Error:${err.response.status}`);
    });
};

export default signIn;
