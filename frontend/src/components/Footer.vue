<template>
  <footer class="bg-dark text-white text-center py-3">
    <div class="container">
      <small class="text-muted">
        &copy; {{ currentYear }} webFire. All rights reserved.
      </small>
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
<!-- (C) 2025 by OPNLAB Development. All rights reserved. -->
