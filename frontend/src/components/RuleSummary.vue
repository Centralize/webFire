<template>
  <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h2 class="text-xl font-bold mb-4">Rule Summary</h2>
    <p>Total Rules: {{ rules.length }}</p>
    <p>Allow Rules: {{ allowRulesCount }}</p>
    <p>Deny Rules: {{ denyRulesCount }}</p>
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
  return props.rules.filter(rule => rule.Action && rule.Action.includes('ALLOW')).length;
});

const denyRulesCount = computed(() => {
  return props.rules.filter(rule => rule.Action && rule.Action.includes('DENY')).length;
});
</script>

<style scoped>
/* Add any specific styles for the rule summary here */
</style>
