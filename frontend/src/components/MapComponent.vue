<template>
  <l-map :zoom="zoom" :center="center">
    <l-tile-layer :url="url"></l-tile-layer>
    <l-marker :lat-lng="marker"></l-marker>
  </l-map>
</template>

<script setup>
import { ref } from 'vue';
import { LMarker, LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

const zoom = ref(13);
const center = ref([51.505, -0.09]);
const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const marker = ref([51.505, -0.09]);
</script>

<style scoped>
/* Add any relevant styles here */
</style>
