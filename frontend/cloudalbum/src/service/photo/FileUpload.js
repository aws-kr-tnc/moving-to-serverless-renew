import axiosInstance from '@/plugins/axios';


const fileUpload = (file, name = 'file', param) => {
  const apiUri = '/photos/file';
  const formData = new FormData();
  formData.append(name, file);
  formData.append('tags', param.tags);
  formData.append('desc', param.description);
  formData.append('make', param.make);
  formData.append('model', param.model);
  formData.append('width', param.width);
  formData.append('height', param.height);
  formData.append('geotag_lat', param.GPSLatitude);
  formData.append('geotag_lng', param.GPSLongitude);

  console.log(formData.getAll());



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
