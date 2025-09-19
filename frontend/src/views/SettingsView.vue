<!-- (C) 2025 by OPNLAB Development. All rights reserved. -->
<template>
  <div class="container py-4">
    <div class="row">
      <div class="col-12">
        <h1 class="h2 mb-4">
          <i class="bi bi-gear me-2"></i>Settings
        </h1>
        
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="bi bi-shield me-2"></i>UFW Control
            </h5>
          </div>
          <div class="card-body">
            <p class="text-muted mb-4">
              Control the UFW firewall service. Use with caution as incorrect configuration may disconnect your session.
            </p>
            <div class="d-flex gap-3">
              <button @click="enableUfw" class="btn btn-success">
                <i class="bi bi-shield-check me-1"></i>
                Enable UFW
              </button>
              <button @click="disableUfw" class="btn btn-danger">
                <i class="bi bi-shield-x me-1"></i>
                Disable UFW
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from '../api/axios';

const enableUfw = async () => {
  if (confirm('Are you sure you want to ENABLE UFW? This might disconnect you if not configured correctly.')) {
    try {
      const response = await axios.post('/enable');
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
      const response = await axios.post('/disable');
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
