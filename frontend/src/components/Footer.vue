<template>
  <footer class="bg-gray-800 p-4 text-white text-center">
    <div class="container mx-auto">
      <p>&copy; {{ currentYear }} webFire. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';

const currentYear = ref(new Date().getFullYear());
</script>

<style scoped>
/* Add any specific styles for the footer here */
</style>
