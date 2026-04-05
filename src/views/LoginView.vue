<template>
  <div class="login-page">
    <div class="login-shell mx-auto px-4 py-6 py-sm-10">
      <div class="login-grid">
        <div class="login-hero pa-6 pa-sm-8">
          <v-icon size="48" color="white" class="mb-4">mdi-hospital-building</v-icon>
          <h1 class="text-h5 text-sm-h4 font-weight-black text-white mb-2">Mumbra Care Portal</h1>
          <p class="text-body-2 text-white mb-5 hero-copy">
            One place for hospitals, doctors, pharmacies, and administrators to keep live community data accurate.
          </p>

          <div class="d-flex flex-wrap ga-2 mb-5">
            <v-chip color="white" variant="flat" size="small">Facilities</v-chip>
            <v-chip color="white" variant="flat" size="small">Doctors</v-chip>
            <v-chip color="white" variant="flat" size="small">Pharmacies</v-chip>
            <v-chip color="white" variant="flat" size="small">Admins</v-chip>
          </div>

          <v-card rounded="xl" elevation="0" class="hero-note pa-4">
            <div class="text-subtitle-2 font-weight-bold mb-2">Before you sign in</div>
            <div class="text-body-2 text-medium-emphasis">
              If your login works but access looks incomplete, your account probably still needs to be linked to the correct profile by an administrator.
            </div>
          </v-card>
        </div>

        <v-card rounded="xl" elevation="4" class="login-card pa-6 pa-sm-7">
          <div class="text-h6 font-weight-bold mb-1">Sign In</div>
          <div class="text-caption text-medium-emphasis mb-5">
            Use your portal credentials to access your assigned dashboard.
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

          <div class="text-center mt-4 text-caption text-medium-emphasis">
            Need a portal account? Contact your administrator.
          </div>
        </v-card>
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
  background:
    radial-gradient(circle at top left, rgba(2, 136, 209, 0.08), transparent 28%),
    linear-gradient(180deg, rgba(0, 105, 92, 0.05), transparent 40%),
    rgb(var(--v-theme-background));
}

.login-shell {
  max-width: 1120px;
}

.login-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 24px;
  align-items: center;
}

.login-hero {
  background: linear-gradient(135deg, #00695C 0%, #0288D1 100%);
  border-radius: 28px;
  min-height: 100%;
}

.hero-copy {
  opacity: 0.84;
  max-width: 44ch;
}

.login-card {
  max-width: 480px;
  width: 100%;
  margin-left: auto;
}

.hero-note {
  background: rgba(255, 255, 255, 0.92);
}

@media (max-width: 900px) {
  .login-grid {
    grid-template-columns: 1fr;
  }

  .login-card {
    max-width: none;
    margin-left: 0;
  }
}
</style>
