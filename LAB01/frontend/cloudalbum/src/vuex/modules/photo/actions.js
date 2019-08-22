import service from '@/service';
import { SET_ALL_PHOTO_LIST, DELETE_ONE_PHOTO, SET_IS_LOADING } from '@/vuex/mutation-types';

const setIsLoading = ({ commit }, data) => {
  commit(SET_IS_LOADING, data);
};

const setAllPhotoList = ({ commit }, data) => {
  commit(SET_ALL_PHOTO_LIST, data);
};

const deleteOnePhoto = ({ commit }, id) => {
  commit(DELETE_ONE_PHOTO, id);
};

const buildImgSrc = async (id, mode) => {

  console.log(`id: ${id}`);
  console.log(`mode: ${mode}`);

  const res = await service.Photo.getPhotoBlob(id, mode);
  return URL.createObjectURL(res.data);
};

const getAllPhotoList = async (store) => {
  try {
    setIsLoading(store, true);
    const resp = await service.Photo.photoList();
    if (resp.data.ok !== true) return;
    console.log('Photo list retrieved successfully ✨');

    const photoList = await Promise.all(resp.data.photos.map(async (obj) => {
      const thumbnailBlobUrl = await buildImgSrc(obj.id, 'thumbnail');
      // const originalBlobUrl = await buildImgSrc(obj.id, 'original');
      return { ...obj, thumbSrc: thumbnailBlobUrl };
    }));

    setAllPhotoList(store, photoList);
    setIsLoading(store, false);
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
  buildImgSrc,
};
