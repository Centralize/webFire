<template>
  <div v-if="isOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center">
    <div class="relative p-5 border w-96 shadow-lg rounded-md bg-white">
      <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">Add New UFW Rule</h3>
      <form @submit.prevent="submitForm">
        <div class="mb-4">
          <label for="action" class="block text-gray-700 text-sm font-bold mb-2">Action:</label>
          <select v-model="rule.action" id="action" class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            <option value="allow">ALLOW</option>
            <option value="deny">DENY</option>
            <option value="reject">REJECT</option>
            <option value="limit">LIMIT</option>
          </select>
        </div>
        <div class="mb-4">
          <label for="port" class="block text-gray-700 text-sm font-bold mb-2">Port:</label>
          <input v-model="rule.port" type="text" id="port" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="e.g., 80, 443, 22">
        </div>
        <div class="mb-4">
          <label for="protocol" class="block text-gray-700 text-sm font-bold mb-2">Protocol (optional):</label>
          <input v-model="rule.protocol" type="text" id="protocol" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="e.g., tcp, udp">
        </div>
        <div class="mb-4">
          <label for="direction" class="block text-gray-700 text-sm font-bold mb-2">Direction:</label>
          <select v-model="rule.direction" id="direction" class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            <option value="in">IN</option>
            <option value="out">OUT</option>
          </select>
        </div>
        <div class="mb-4">
          <label for="from_ip" class="block text-gray-700 text-sm font-bold mb-2">From IP (optional, default: any):</label>
          <input v-model="rule.from_ip" type="text" id="from_ip" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="e.g., 192.168.1.1">
        </div>
        <div class="flex items-center justify-between">
          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Add Rule
          </button>
          <button type="button" @click="closeModal" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import axios from '../api/axios';

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(['close', 'ruleAdded']);

const rule = ref({
  action: 'allow',
  port: '',
  protocol: '',
  direction: 'in',
  from_ip: 'any',
});

const submitForm = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/rules', rule.value);
    if (response.data.status === 'success') {
      alert('Rule added successfully!');
      emit('ruleAdded');
      closeModal();
    } else {
      alert('Error adding rule: ' + response.data.message);
    }
  } catch (error) {
    console.error('Error adding rule:', error);
    alert('Failed to add rule. Check console for details.');
  }
};

const closeModal = () => {
  emit('close');
  // Reset form
  rule.value = {
    action: 'allow',
    port: '',
    protocol: '',
    direction: 'in',
    from_ip: 'any',
  };
};
</script>

<style scoped>
/* Add any specific styles for the modal here */
</style>
