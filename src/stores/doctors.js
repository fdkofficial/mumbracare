import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchDoctors, updateDoctorStatus } from '@/api'

export const useDoctorsStore = defineStore('doctors', () => {
  const doctors = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedSpecialty = ref('ALL')
  const selectedArea = ref('ALL')
  const searchQuery = ref('')

  const filtered = computed(() => {
    let result = doctors.value
    if (selectedSpecialty.value !== 'ALL')
      result = result.filter(d => d.specialty === selectedSpecialty.value)
    if (selectedArea.value !== 'ALL')
      result = result.filter(d => d.facility_area === selectedArea.value)
    if (searchQuery.value)
      result = result.filter(d =>
        d.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
      )
    return result
  })

  const available = computed(() => filtered.value.filter(d => d.is_available))
  const away = computed(() => filtered.value.filter(d => !d.is_available))

  async function load(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await fetchDoctors(params)
      doctors.value = Array.isArray(data) ? data : (data.results ?? [])
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function toggleStatus(doctor) {
    const prev = doctor.is_available
    doctor.is_available = !prev
    try {
      await updateDoctorStatus(doctor.id, doctor.is_available)
    } catch {
      doctor.is_available = prev // rollback on failure
    }
  }

  return {
    doctors, loading, error, selectedSpecialty, selectedArea, searchQuery,
    filtered, available, away, load, toggleStatus,
  }
})
