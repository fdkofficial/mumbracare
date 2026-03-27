import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getMe } from '@/api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => !!user.value)
  const userType = computed(() => user.value?.user_type ?? null)

  async function fetchMe() {
    if (!localStorage.getItem('access_token')) return
    try {
      loading.value = true
      user.value = await getMe()
    } catch {
      logout()
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, loading, isLoggedIn, userType, fetchMe, logout }
})
