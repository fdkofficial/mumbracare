import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchPharmacies } from '@/api'

export const usePharmaciesStore = defineStore('pharmacies', () => {
  const pharmacies = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedArea = ref('ALL')
  const onlyNight = ref(false)

  const filtered = computed(() => {
    let result = pharmacies.value
    if (selectedArea.value !== 'ALL')
      result = result.filter(p => p.area === selectedArea.value)
    if (onlyNight.value)
      result = result.filter(p => p.is_24_7)
    return result
  })

  async function load(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await fetchPharmacies(params)
      pharmacies.value = Array.isArray(data) ? data : (data.results ?? [])
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { pharmacies, loading, error, selectedArea, onlyNight, filtered, load }
})
