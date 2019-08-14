<template>
    <div>
      <img v-auth-img="http://127.0.0.1:5000/photos/1">
    </div>

</template>

<script>

export default {
  data() {
    return {
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 3,
      center: [47.413220, -1.219482],
      markerLatLng: [47.313220, -1.319482],
    };
  },
};
</script>
