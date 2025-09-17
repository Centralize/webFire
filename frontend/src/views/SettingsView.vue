<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Settings</h1>
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 class="text-xl font-bold mb-4">UFW Control</h2>
      <button @click="enableUfw" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-4">
        Enable UFW
      </button>
      <button @click="disableUfw" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Disable UFW
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from '../api/axios';

const enableUfw = async () => {
  if (confirm('Are you sure you want to ENABLE UFW? This might disconnect you if not configured correctly.')) {
    try {
      const response = await axios.post('http://localhost:8000/api/enable');
      if (response.data.status === 'success') {
        alert('UFW enabled successfully!');
      } else {
        alert('Error enabling UFW: ' + response.data.message);
      }
    } catch (error) {
      console.error('Error enabling UFW:', error);
      alert('Failed to enable UFW. Check console for details.');
    }
  }
};

const disableUfw = async () => {
  if (confirm('Are you sure you want to DISABLE UFW? This will open all ports.')) {
    try {
      const response = await axios.post('http://localhost:8000/api/disable');
      if (response.data.status === 'success') {
        alert('UFW disabled successfully!');
      } else {
        alert('Error disabling UFW: ' + response.data.message);
      }
    } catch (error) {
      console.error('Error disabling UFW:', error);
      alert('Failed to disable UFW. Check console for details.');
    }
  }
};
</script>

<style scoped>
/* Styles for Settings View */
</style>