import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API,
  timeout: process.env.VUE_APP_TIMEOUT,
});

export default axiosInstance;
