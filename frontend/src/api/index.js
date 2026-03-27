import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://51.20.91.145:8080/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const { data } = await axios.post(`${import.meta.env.VITE_API_BASE_URL || 'http://51.20.91.145:8080/api'}/auth/refresh/`, { refresh })
          localStorage.setItem('access_token', data.access)
          original.headers.Authorization = `Bearer ${data.access}`
          return api(original)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      }
    }
    return Promise.reject(error)
  },
)

export const fetchBeds = (area = null) =>
  api.get('/beds/', { params: area ? { area } : {} }).then(r => r.data)

export const fetchFacilities = (params = {}) =>
  api.get('/facilities/', { params }).then(r => r.data)

export const fetchDoctors = (params = {}) =>
  api.get('/doctors/', { params }).then(r => r.data)

export const fetchPharmacies = (params = {}) =>
  api.get('/pharmacies/', { params }).then(r => r.data)

export const updateDoctorStatus = (id, isAvailable) =>
  api.patch(`/doctors/${id}/status/`, { is_available: isAvailable }).then(r => r.data)

// ─── Auth API ────────────────────────────────────────────────────────────────
export const login = (username, password) =>
  api.post('/auth/login/', { username, password }).then(r => r.data)

export const getMe = () => api.get('/auth/me/').then(r => r.data)

// ─── Portal API ──────────────────────────────────────────────────────────────
export const portalGetFacility = () => api.get('/portal/facility/').then(r => r.data)
export const portalUpdateFacility = (data) => api.patch('/portal/facility/', data).then(r => r.data)
export const portalGetBeds = () => api.get('/portal/facility/beds/').then(r => r.data)
export const portalUpdateBeds = (data) => api.patch('/portal/facility/beds/', data).then(r => r.data)

export const portalGetDoctor = () => api.get('/portal/doctor/').then(r => r.data)
export const portalUpdateDoctor = (data) => api.patch('/portal/doctor/', data).then(r => r.data)
export const portalToggleDoctorStatus = (is_available) =>
  api.patch('/portal/doctor/status/', { is_available }).then(r => r.data)

export const adminGetUsers = () => api.get('/portal/admin/users/').then(r => r.data)
export const adminCreateUser = (data) => api.post('/portal/admin/users/', data).then(r => r.data)
export const adminUpdateUser = (id, data) => api.patch(`/portal/admin/users/${id}/`, data).then(r => r.data)
export const adminDeleteUser = (id) => api.delete(`/portal/admin/users/${id}/`).then(r => r.data)

// ─── Public content ───────────────────────────────────────────────────────────
export const getAds = () => api.get('/ads/').then(r => r.data)
export const getSiteSettings = () => api.get('/site-settings/').then(r => r.data)

export default api
