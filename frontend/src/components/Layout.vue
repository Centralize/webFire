<template>
  <div class="min-h-screen flex flex-col">
    <header>
      <slot name="header"></slot>
    </header>
    <main class="flex-grow">
      <slot></slot>
    </main>
    <footer>
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
