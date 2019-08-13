import axiosInstance from '@/plugins/axios';


const fileUpload = (file, name = 'file', param) => {
  const apiUri = '/photos/file';
  const formData = new FormData();
  formData.append(name, file);

  const config = {
    headers: {
      'content-type': 'multipart/form-data',
    },
  };

  console.log('upload');
  console.log(param);
  console.log(axiosInstance.defaults.headers.common.Authorization);


  return axiosInstance.post(apiUri, formData, config);
};

export default fileUpload;
