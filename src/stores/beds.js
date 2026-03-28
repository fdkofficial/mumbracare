import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchBeds } from '@/api'

export const useBedsStore = defineStore('beds', () => {
  const facilities = ref([])
  const loading = ref(false)
  const error = ref(null)
  const lastRefreshed = ref(null)
  const selectedArea = ref('ALL')

  const filtered = computed(() => {
    if (selectedArea.value === 'ALL') return facilities.value
    return facilities.value.filter(f => f.area === selectedArea.value)
  })

  const summary = computed(() => ({
    total: filtered.value.length,
    available: filtered.value.filter(f => f.bed_status?.is_available).length,
    full: filtered.value.filter(f => f.bed_status && !f.bed_status.is_available).length,
  }))

  async function load(area = null) {
    loading.value = true
    error.value = null
    try {
      const data = await fetchBeds(area === 'ALL' ? null : area)
      facilities.value = Array.isArray(data) ? data : (data.results ?? [])
      lastRefreshed.value = new Date()
    } catch (e) {
      error.value = `${e.message}` // print error and url
    } finally {
      loading.value = false
    }
  }

  function setArea(area) {
    selectedArea.value = area
  }

  return { facilities, loading, error, lastRefreshed, selectedArea, filtered, summary, load, setArea }
})
