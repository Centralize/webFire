<template>
  <div 
    v-if="isOpen" 
    class="modal fade show d-block" 
    tabindex="-1" 
    role="dialog"
    style="background-color: rgba(0,0,0,0.5)"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-plus-circle me-2"></i>Add New UFW Rule
          </h5>
          <button 
            type="button" 
            class="btn-close" 
            @click="closeModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="action" class="form-label">Action</label>
              <select v-model="rule.action" id="action" class="form-select">
                <option value="allow">ALLOW</option>
                <option value="deny">DENY</option>
                <option value="reject">REJECT</option>
                <option value="limit">LIMIT</option>
              </select>
            </div>
            
            <div class="mb-3">
              <label for="port" class="form-label">Port</label>
              <input 
                v-model="rule.port" 
                type="text" 
                id="port" 
                class="form-control" 
                placeholder="e.g., 80, 443, 22"
                required
              >
              <div class="form-text">Enter a single port or port range</div>
            </div>
            
            <div class="mb-3">
              <label for="protocol" class="form-label">Protocol (optional)</label>
              <input 
                v-model="rule.protocol" 
                type="text" 
                id="protocol" 
                class="form-control" 
                placeholder="e.g., tcp, udp"
              >
            </div>
            
            <div class="mb-3">
              <label for="direction" class="form-label">Direction</label>
              <select v-model="rule.direction" id="direction" class="form-select">
                <option value="in">IN</option>
                <option value="out">OUT</option>
              </select>
            </div>
            
            <div class="mb-3">
              <label for="from_ip" class="form-label">From IP (optional)</label>
              <input 
                v-model="rule.from_ip" 
                type="text" 
                id="from_ip" 
                class="form-control" 
                placeholder="e.g., 192.168.1.1"
              >
              <div class="form-text">Leave empty for 'any'</div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-secondary" 
            @click="closeModal"
          >
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="submitForm"
          >
            <i class="bi bi-check-lg me-1"></i>Add Rule
          </button>
        </div>
      </div>
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
    const response = await axios.post('/rules', rule.value);
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
