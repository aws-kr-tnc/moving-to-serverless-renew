import axiosInstance from '@/plugins/axios';


const fileUpload = (file, name = 'myfile.jpg') => {
  const apiUri = '/photos/file';
  const formData = new FormData();
  formData.append(name, file);

  const config = {
    headers: {
      'content-type': 'multipart/form-data',
    },
  };

  console.log('upload');
  console.log(axiosInstance.defaults.headers.common.Authorization);


  return axiosInstance.post(apiUri, formData, config);
};

export default fileUpload;


// export default function (url, file, name = 'avatar') {
//   if (typeof url !== 'string') {
//     throw new TypeError(`Expected a string, got ${typeof url}`);
//   }
//
//   // You can add checks to ensure the url is valid, if you wish
//
//   const formData = new FormData();
//   formData.append(name, file);
//   const config = {
//     headers: {
//       'content-type': 'multipart/form-data'
//     }
//   };
//   return axios.post(url, formData, config);
// };
