<template>
  <div class="min-vh-100 d-flex flex-column">
    <header>
      <slot name="header"></slot>
    </header>
    <main class="flex-grow-1">
      <slot></slot>
    </main>
    <footer class="mt-auto">
      <slot name="footer"></slot>
    </footer>
  </div>
</template>

<script setup>
// No script logic needed for a simple layout component
</script>

<style scoped>
/* Basic styling for layout */
</style>
<!-- (C) 2025 by OPNLAB Development. All rights reserved. -->
