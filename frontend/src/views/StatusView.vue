<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">UFW Status</h1>
    <div v-if="status.status === 'active'" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">UFW is Active!</strong>
      <span class="block sm:inline">Your firewall is currently enabled.</span>
    </div>
    <div v-else-if="status.status === 'inactive'" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">UFW is Inactive!</strong>
      <span class="block sm:inline">Your firewall is currently disabled.</span>
    </div>
    <div v-else class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">UFW Status Unknown!</strong>
      <span class="block sm:inline">Could not determine UFW status. {{ status.message }}</span>
    </div>

    <div class="mt-8">
      <RuleSummary :rules="rules" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../api/axios';
import RuleSummary from '../components/RuleSummary.vue';

const status = ref({ status: 'loading', message: '' });
const rules = ref([]);

const fetchUfwStatus = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/status');
    status.value = response.data;
  } catch (error) {
    console.error('Error fetching UFW status:', error);
    status.value = { status: 'error', message: error.message || 'Failed to fetch status.' };
  }
};

const fetchUfwRules = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/rules');
    rules.value = response.data.rules;
  } catch (error) {
    console.error('Error fetching UFW rules:', error);
  }
};

onMounted(() => {
  fetchUfwStatus();
  fetchUfwRules();
});
</script>

<style scoped>
/* Styles for Status View */
</style>
