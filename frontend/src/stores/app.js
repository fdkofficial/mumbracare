import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const locale = ref(localStorage.getItem('mc_locale') || 'en')
  const darkMode = ref(localStorage.getItem('mc_dark') === 'true')
  const selectedArea = ref('ALL')

  const isRTL = computed(() => locale.value === 'ur')

  function setLocale(lang) {
    locale.value = lang
    localStorage.setItem('mc_locale', lang)
  }

  function toggleDark() {
    darkMode.value = !darkMode.value
    localStorage.setItem('mc_dark', darkMode.value)
  }

  function setArea(area) {
    selectedArea.value = area
  }

  return { locale, darkMode, isRTL, selectedArea, setLocale, toggleDark, setArea }
})
