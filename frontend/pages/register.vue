<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userService } from '../services/userService'

const router = useRouter()
const loading = ref(false)
const error = ref(null)

const registerForm = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  try {
    // Validate passwords match
    if (registerForm.value.password !== registerForm.value.confirmPassword) {
      error.value = 'Passwords do not match'
      return
    }

    loading.value = true
    error.value = null
    
    await userService.register({
      name: registerForm.value.name,
      email: registerForm.value.email,
      password: registerForm.value.password
    })

    // Reset form
    registerForm.value = {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    }

    // Redirect to login page
    router.push('/login')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-container">
    <div class="glass-card register-card">
      <h2 class="text-2xl font-bold mb-6">Register</h2>
      
      <div v-if="error" class="error-message mb-4">
        {{ error }}
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Name</label>
          <input 
            v-model="registerForm.name" 
            type="text" 
            placeholder="Enter your name"
            class="form-input"
            :disabled="loading"
            required
          >
        </div>
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="registerForm.email" 
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
            v-model="registerForm.password" 
            type="password" 
            placeholder="Enter password"
            class="form-input"
            :disabled="loading"
            required
          >
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="Confirm password"
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
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      <div class="mt-4 text-center">
        Already have an account? 
        <NuxtLink to="/login" class="text-primary-color hover:underline">
          Login now
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-card {
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