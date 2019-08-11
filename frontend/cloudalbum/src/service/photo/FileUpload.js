import axiosInstance from '@/plugins/axios';


const fileUpload = (file, name = 'file', exif) => {
  const apiUri = '/photos/file';
  const formData = new FormData();
  formData.append(name, file);

  if (typeof exif === 'undefined' || exif === null) {

  } else {
    formData.append()
    // console.log(`make: ${this.exifdata.Make}`);
    // console.log(`model: ${this.exifdata.Model}`);
    // console.log(`width: ${this.exifdata.PixelXDimension}`);
    // console.log(`height: ${this.exifdata.PixelYDimension}`);
    // console.log(`GPSLatitude: ${this.exifdata.GPSLatitude}`);
    // console.log(`GPSLatitudeRef: ${this.exifdata.GPSLatitudeRef}`);
    // console.log(`GPSLongitude: ${this.exifdata.GPSLongitude}`);
    // console.log(`GPSLongitudeRef: ${this.exifdata.GPSLongitudeRef}`);
    // console.log(`converted GPSLatitude: ${service.Photo.gpsConverter(this.exifdata.GPSLatitude, this.exifdata.GPSLatitudeRef)}`);
    // console.log(`converted GPSLongitude: ${service.Photo.gpsConverter(this.exifdata.GPSLongitude, this.exifdata.GPSLongitudeRef)}`);
    // console.log(`taken_date: ${this.exifdata.DateTime}`);
  }


  const config = {
    headers: {
      'content-type': 'multipart/form-data',
    },
  };

  console.log('upload');
  console.log(exif);
  console.log(axiosInstance.defaults.headers.common.Authorization);


  return axiosInstance.post(apiUri, formData, config);
};

export default fileUpload;
