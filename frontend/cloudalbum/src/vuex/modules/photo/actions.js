import service from '@/service';
import { SET_ALL_PHOTO_LIST, DELETE_ONE_PHOTO } from '@/vuex/mutation-types';

const setAllPhotoList = ({ commit }, data) => {
  commit(SET_ALL_PHOTO_LIST, data);
};

const deleteOnePhoto = ({ commit }, id) => {
  commit(DELETE_ONE_PHOTO, id);
};

const buildImgSrc = async (id, mode) => {
  const res = await service.Photo.getPhotoBlob(id, mode);
  return URL.createObjectURL(res.data);
};

const getAllPhotoList = async (store) => {
  try {
    const resp = await service.Photo.photoList();
    if (resp.data.ok !== true) return;
    console.log('Photo list retrieved successfully ✨');
    const photoList = await Promise.all(resp.data.photos.map(async (obj) => {
      const thumbnailBlobUrl = await buildImgSrc(obj.id, 'thmubnail');
      const originalBlobUrl = await buildImgSrc(obj.id, 'original');
      return { ...obj, thumbSrc: thumbnailBlobUrl, originalSrc: originalBlobUrl };
    }));
    setAllPhotoList(store, photoList);
  } catch (error) {
    console.error(error);
  }
};

const deletePhoto = async (store, id) => {
  try {
    const resp = await service.Photo.deletePhoto(id);
    if (!resp.data.ok) throw new Error(resp);
    deleteOnePhoto(store, id);
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
};

export default {
  getAllPhotoList,
  deletePhoto,
};
