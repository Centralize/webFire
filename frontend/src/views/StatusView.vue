<!-- (C) 2025 by OPNLAB Development. All rights reserved. -->
<template>
  <div class="container py-4">
    <div class="row">
      <div class="col-12">
        <h1 class="h2 mb-4">
          <i class="bi bi-shield-check me-2"></i>UFW Status
        </h1>
        
        <!-- Loading State -->
        <div v-if="status.status === 'loading'" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3 text-muted">Checking UFW status...</p>
        </div>
        
        <!-- Status Alerts -->
        <div 
          v-else-if="status.status === 'active'" 
          class="alert alert-success d-flex align-items-center mb-4"
          role="alert"
        >
          <i class="bi bi-check-circle-fill me-2"></i>
          <div>
            <strong>UFW is Active!</strong>
            <span class="d-block d-sm-inline">Your firewall is currently enabled and protecting your system.</span>
          </div>
        </div>
        
        <div 
          v-else-if="status.status === 'inactive'" 
          class="alert alert-danger d-flex align-items-center mb-4"
          role="alert"
        >
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          <div>
            <strong>UFW is Inactive!</strong>
            <span class="d-block d-sm-inline">Your firewall is currently disabled.</span>
          </div>
        </div>
        
        <div 
          v-else 
          class="alert alert-warning d-flex align-items-center mb-4"
          role="alert"
        >
          <i class="bi bi-question-circle-fill me-2"></i>
          <div>
            <strong>UFW Status Unknown!</strong>
            <span class="d-block d-sm-inline">{{ status.message }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mt-4">
      <div class="col-12">
        <RuleSummary :rules="rules" />
      </div>
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
    const response = await axios.get('/status');
    status.value = response.data;
  } catch (error) {
    console.error('Error fetching UFW status:', error);
    status.value = { status: 'error', message: error.message || 'Failed to fetch status.' };
  }
};

const fetchUfwRules = async () => {
  try {
    const response = await axios.get('/rules');
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
