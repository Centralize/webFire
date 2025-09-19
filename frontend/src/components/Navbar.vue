<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold">
        <i class="bi bi-shield-check me-2"></i>
        webFire
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
        aria-controls="navbarNav" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link to="/status" class="nav-link">
              <i class="bi bi-activity me-1"></i>Status
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/rules" class="nav-link">
              <i class="bi bi-list-ul me-1"></i>Rules
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/settings" class="nav-link">
              <i class="bi bi-gear me-1"></i>Settings
            </router-link>
          </li>
        </ul>
        <button @click="authStore.logout()" class="btn btn-outline-danger">
          <i class="bi bi-box-arrow-right me-1"></i>Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
/* Add any specific styles for the navbar here */
</style>