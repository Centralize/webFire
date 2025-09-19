<template>
  <div v-if="authStore.isAuthenticated">
    <Layout>
      <template #header>
        <Navbar />
      </template>
      <router-view />
      <template #footer>
        <Footer />
      </template>
    </Layout>
  </div>
  <div v-else class="min-vh-100 d-flex align-items-center bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body p-4">
              <div class="text-center mb-4">
                <h1 class="h3 fw-bold text-primary">
                  <i class="bi bi-shield-check me-2"></i>webFire
                </h1>
                <p class="text-muted">UFW Management Interface</p>
              </div>
              <form @submit.prevent="handleLogin">
                <div class="form-floating mb-3">
                  <input 
                    v-model="username" 
                    type="text" 
                    id="username" 
                    class="form-control" 
                    placeholder="admin"
                    required
                  >
                  <label for="username">Username</label>
                </div>
                <div class="form-floating mb-4">
                  <input 
                    v-model="password" 
                    type="password" 
                    id="password" 
                    class="form-control" 
                    placeholder="Password"
                    required
                  >
                  <label for="password">Password</label>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-2">
                  <i class="bi bi-box-arrow-in-right me-2"></i>
                  Sign In
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from './stores/auth';
import Layout from './components/Layout.vue';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

const authStore = useAuthStore();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value);
  if (!success) {
    alert('Login failed. Please check your credentials.');
  }
};
</script>

<style>
/* Global styles if any */
</style>
