<template>
  <div class="card">
    <div class="card-header">
      <h5 class="card-title mb-0">
        <i class="bi bi-bar-chart me-2"></i>Rule Summary
      </h5>
    </div>
    <div class="card-body">
      <div class="row text-center">
        <div class="col-md-4">
          <div class="border-end">
            <h3 class="text-primary mb-1">{{ rules.length }}</h3>
            <p class="text-muted mb-0">Total Rules</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="border-end">
            <h3 class="text-success mb-1">{{ allowRulesCount }}</h3>
            <p class="text-muted mb-0">Allow Rules</p>
          </div>
        </div>
        <div class="col-md-4">
          <h3 class="text-danger mb-1">{{ denyRulesCount }}</h3>
          <p class="text-muted mb-0">Deny Rules</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  rules: {
    type: Array,
    default: () => [],
  },
});

const allowRulesCount = computed(() => {
  return props.rules.filter(rule => rule.action && String(rule.action).toUpperCase().includes('ALLOW')).length;
});

const denyRulesCount = computed(() => {
  return props.rules.filter(rule => rule.action && String(rule.action).toUpperCase().includes('DENY')).length;
});
</script>

<style scoped>
/* Add any specific styles for the rule summary here */
</style>
<!-- (C) 2025 by OPNLAB Development. All rights reserved. -->
