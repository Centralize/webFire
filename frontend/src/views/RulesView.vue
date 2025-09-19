<template>
  <div class="container py-4">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h1 class="h2 mb-0">
            <i class="bi bi-list-ul me-2"></i>UFW Rules
          </h1>
          <button 
            @click="isModalOpen = true" 
            class="btn btn-primary"
          >
            <i class="bi bi-plus-lg me-1"></i>Add New Rule
          </button>
        </div>

        <!-- Filter Card -->
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-funnel me-2"></i>Filter and Search Rules
            </h5>
          </div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-4">
                <label for="filterAction" class="form-label">Action</label>
                <select v-model="filterAction" id="filterAction" class="form-select">
                  <option value="">All Actions</option>
                  <option value="ALLOW">ALLOW</option>
                  <option value="DENY">DENY</option>
                  <option value="REJECT">REJECT</option>
                  <option value="LIMIT">LIMIT</option>
                </select>
              </div>
              <div class="col-md-4">
                <label for="filterDirection" class="form-label">Direction</label>
                <select v-model="filterDirection" id="filterDirection" class="form-select">
                  <option value="">All Directions</option>
                  <option value="IN">IN</option>
                  <option value="OUT">OUT</option>
                </select>
              </div>
              <div class="col-md-4">
                <label for="searchQuery" class="form-label">Search</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-search"></i>
                  </span>
                  <input 
                    v-model="searchQuery" 
                    type="text" 
                    id="searchQuery" 
                    class="form-control" 
                    placeholder="Search all fields"
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Rules Table -->
        <div v-if="filteredRules.length > 0" class="card">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">To</th>
                  <th scope="col">Action</th>
                  <th scope="col">Direction</th>
                  <th scope="col">From</th>
                  <th scope="col" class="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="rule in filteredRules" :key="rule.id">
                  <td class="fw-mono">{{ rule.id }}</td>
                  <td>{{ rule.to }}</td>
                  <td>
                    <span 
                      class="badge" 
                      :class="getActionBadgeClass(rule.action)"
                    >
                      {{ rule.action }}
                    </span>
                  </td>
                  <td>{{ rule.direction }}</td>
                  <td>{{ rule.from }}</td>
                  <td class="text-center">
                    <button 
                      @click="deleteRule(rule.id)" 
                      class="btn btn-sm btn-outline-danger"
                      :title="`Delete rule ${rule.id}`"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- No Results -->
        <div v-else class="alert alert-info text-center">
          <i class="bi bi-info-circle me-2"></i>
          No UFW rules found matching your criteria.
        </div>
      </div>
    </div>

    
    <AddRuleModal 
      :isOpen="isModalOpen" 
      @close="isModalOpen = false" 
      @ruleAdded="fetchUfwRules" 
    />
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
    const response = await axios.get('/rules');
    rules.value = response.data.rules;
  } catch (error) {
    console.error('Error fetching UFW rules:', error);
  }
};

const deleteRule = async (ruleId) => {
  if (confirm(`Are you sure you want to delete rule ID ${ruleId}?`)) {
    try {
      const response = await axios.delete(`/rules/${ruleId}`);
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

const getActionBadgeClass = (action) => {
  switch (action) {
    case 'ALLOW': return 'bg-success'
    case 'DENY': return 'bg-danger' 
    case 'REJECT': return 'bg-warning'
    case 'LIMIT': return 'bg-info'
    default: return 'bg-secondary'
  }
}

onMounted(fetchUfwRules);
</script>

<style scoped>
/* Styles for Rules View */
</style>
