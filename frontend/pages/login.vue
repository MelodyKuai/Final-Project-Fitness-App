<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userService } from '../services/userService'

const router = useRouter()
const loading = ref(false)
const error = ref(null)

const loginForm = ref({
  email: '',
  password: ''
})

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = null
    
    await userService.login(loginForm.value)

    // Reset form
    loginForm.value = {
      email: '',
      password: ''
    }

    // Redirect to home page
    router.push('/home')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="glass-card login-card">
      <h2 class="text-2xl font-bold mb-6">Login</h2>
      
      <div v-if="error" class="error-message mb-4">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="loginForm.email" 
            type="email" 
            placeholder="Enter your email"
            class="form-input"
            :disabled="loading"
            required
          >
        </div>
        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="Enter your password"
            class="form-input"
            :disabled="loading"
            required
          >
        </div>
        <button 
          type="submit" 
          class="btn-primary w-full"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <div class="mt-4 text-center">
        Don't have an account? 
        <NuxtLink to="/register" class="text-primary-color hover:underline">
          Register now
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-color);
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 8px;
  background: rgba(255,255,255,0.9);
}

.form-input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background-color: #dc3545;
  color: white;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 