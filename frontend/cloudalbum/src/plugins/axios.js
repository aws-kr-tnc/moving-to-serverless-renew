import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API,
  timeout: 1500,
  withCredentials: true,
});

export default {
  name: 'axiosInstance',

};
