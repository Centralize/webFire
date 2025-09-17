<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">UFW Rules</h1>
    <button @click="isModalOpen = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
      Add New Rule
    </button>

    <!-- Filter and Search Inputs -->
    <div class="mb-4 p-4 border rounded shadow-sm bg-gray-50">
      <h2 class="text-xl font-bold mb-2">Filter and Search Rules</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label for="filterAction" class="block text-gray-700 text-sm font-bold mb-2">Action:</label>
          <select v-model="filterAction" id="filterAction" class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            <option value="">All</option>
            <option value="ALLOW">ALLOW</option>
            <option value="DENY">DENY</option>
            <option value="REJECT">REJECT</option>
            <option value="LIMIT">LIMIT</option>
          </select>
        </div>
        <div>
          <label for="filterDirection" class="block text-gray-700 text-sm font-bold mb-2">Direction:</label>
          <select v-model="filterDirection" id="filterDirection" class="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
            <option value="">All</option>
            <option value="IN">IN</option>
            <option value="OUT">OUT</option>
          </select>
        </div>
        <div>
          <label for="searchQuery" class="block text-gray-700 text-sm font-bold mb-2">Search:</label>
          <input v-model="searchQuery" type="text" id="searchQuery" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" placeholder="Search all fields">
        </div>
      </div>
    </div>

    <div v-if="filteredRules.length > 0" class="overflow-x-auto">
      <table class="min-w-full bg-white border border-gray-300">
        <thead>
          <tr>
            <th class="py-2 px-4 border-b">ID</th>
            <th class="py-2 px-4 border-b">To</th>
            <th class="py-2 px-4 border-b">Action</th>
            <th class="py-2 px-4 border-b">Direction</th>
            <th class="py-2 px-4 border-b">From</th>
            <th class="py-2 px-4 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rule in filteredRules" :key="rule.id">
            <td class="py-2 px-4 border-b">{{ rule.id }}</td>
            <td class="py-2 px-4 border-b">{{ rule.to }}</td>
            <td class="py-2 px-4 border-b">{{ rule.action }}</td>
            <td class="py-2 px-4 border-b">{{ rule.direction }}</td>
            <td class="py-2 px-4 border-b">{{ rule.from }}</td>
            <td class="py-2 px-4 border-b">
              <button @click="deleteRule(rule.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-sm">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative" role="alert">
      <p>No UFW rules found matching your criteria.</p>
    </div>

    <AddRuleModal :isOpen="isModalOpen" @close="isModalOpen = false" @ruleAdded="fetchUfwRules" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from '../api/axios';
import AddRuleModal from '../components/AddRuleModal.vue';

const rules = ref([]);
const isModalOpen = ref(false);
const filterAction = ref('');
const filterDirection = ref('');
const searchQuery = ref('');

const fetchUfwRules = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/rules');
    rules.value = response.data.rules;
  } catch (error) {
    console.error('Error fetching UFW rules:', error);
  }
};

const deleteRule = async (ruleId) => {
  if (confirm(`Are you sure you want to delete rule ID ${ruleId}?`)) {
    try {
      const response = await axios.delete(`http://localhost:8000/api/rules/${ruleId}`);
      if (response.data.status === 'success') {
        alert('Rule deleted successfully!');
        fetchUfwRules(); // Refresh the list of rules
      } else {
        alert('Error deleting rule: ' + response.data.message);
      }
    } catch (error) {
      console.error('Error deleting rule:', error);
      alert('Failed to delete rule. Check console for details.');
    }
  }
};

const filteredRules = computed(() => {
  let filtered = rules.value;

  // Filter by action
  if (filterAction.value) {
    filtered = filtered.filter(rule => rule.action === filterAction.value);
  }

  // Filter by direction
  if (filterDirection.value) {
    filtered = filtered.filter(rule => rule.direction === filterDirection.value);
  }

  // Search across all fields
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(rule =>
      Object.values(rule).some(value =>
        String(value).toLowerCase().includes(query)
      )
    );
  }

  return filtered;
});

onMounted(fetchUfwRules);
</script>

<style scoped>
/* Styles for Rules View */
</style>
