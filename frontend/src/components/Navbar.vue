<template>
  <nav class="bg-gray-800 p-4 text-white">
    <div class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-xl font-bold">webFire</router-link>
      <div>
        <router-link to="/status" class="px-3 py-2 rounded hover:bg-gray-700">Status</router-link>
        <router-link to="/rules" class="px-3 py-2 rounded hover:bg-gray-700 ml-4">Rules</router-link>
        <router-link to="/settings" class="px-3 py-2 rounded hover:bg-gray-700 ml-4">Settings</router-link>
        <button @click="authStore.logout()" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-4">
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
/* Add any specific styles for the navbar here */
</style>