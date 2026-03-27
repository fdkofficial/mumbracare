<template>
  <div class="login-page">
    <div class="login-hero">
      <v-icon size="48" color="white" class="mb-3">mdi-hospital-building</v-icon>
      <h1 class="text-h5 font-weight-black text-white mb-1">Mumbra Care</h1>
      <p class="text-body-2 text-white" style="opacity:0.8">Staff & Facility Portal</p>
    </div>

    <div class="login-card-wrapper px-4">
      <v-card rounded="xl" elevation="4" class="login-card pa-6">
        <div class="text-h6 font-weight-bold mb-1">Sign In</div>
        <div class="text-caption text-medium-emphasis mb-5">
          Use your portal credentials to log in
        </div>

        <v-alert v-if="error" type="error" variant="tonal" rounded="lg" density="compact" class="mb-4">
          {{ error }}
        </v-alert>

        <v-text-field
          v-model="form.username"
          label="Username"
          prepend-inner-icon="mdi-account-outline"
          variant="outlined"
          density="comfortable"
          rounded="lg"
          class="mb-3"
          hide-details="auto"
          :error-messages="fieldErrors.username"
          @keyup.enter="submit"
        />

        <v-text-field
          v-model="form.password"
          label="Password"
          prepend-inner-icon="mdi-lock-outline"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
          variant="outlined"
          density="comfortable"
          rounded="lg"
          class="mb-5"
          hide-details="auto"
          :error-messages="fieldErrors.password"
          @click:append-inner="showPassword = !showPassword"
          @keyup.enter="submit"
        />

        <v-btn
          color="primary"
          size="large"
          rounded="lg"
          block
          :loading="loading"
          @click="submit"
        >
          Sign In
        </v-btn>

        <div class="text-center mt-4">
          <v-btn variant="text" color="primary" size="small" :to="{ name: 'home' }">
            <v-icon start size="16">mdi-arrow-left</v-icon>
            Back to Mumbra Care
          </v-btn>
        </div>
      </v-card>

      <div class="text-center mt-4 text-caption text-medium-emphasis">
        Need a portal account? Contact your administrator.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login, getMe } from '@/api/index.js'

const router = useRouter()

const form = reactive({ username: '', password: '' })
const error = ref('')
const fieldErrors = reactive({ username: [], password: [] })
const loading = ref(false)
const showPassword = ref(false)

async function submit() {
  error.value = ''
  fieldErrors.username = []
  fieldErrors.password = []

  if (!form.username.trim()) { fieldErrors.username = ['Username is required']; return }
  if (!form.password) { fieldErrors.password = ['Password is required']; return }

  loading.value = true
  try {
    const tokens = await login(form.username.trim(), form.password)
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    // Fetch user info to confirm login
    await getMe()
    router.push({ name: 'portal' })
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Invalid username or password.'
    } else {
      error.value = 'Unable to connect. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
}

.login-hero {
  background: linear-gradient(135deg, #00695C 0%, #0288D1 100%);
  padding: 48px 24px 64px;
  text-align: center;
}

.login-card-wrapper {
  margin-top: -32px;
}

.login-card {
  max-width: 480px;
  margin: 0 auto;
}
</style>
