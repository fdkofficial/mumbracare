<template>
  <div class="portal-page">
    <!-- App bar -->
    <v-app-bar flat color="primary" elevation="0">
      <v-app-bar-title>
        <div class="text-subtitle-1 font-weight-bold text-white">Staff Portal</div>
        <div class="text-caption text-white" style="opacity:0.8">{{ me?.profile_name || me?.username }}</div>
      </v-app-bar-title>
      <template #append>
        <v-chip :color="roleColor" variant="flat" size="small" class="me-2">{{ me?.user_type }}</v-chip>
        <v-btn icon variant="text" color="white" @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <div v-if="loadingMe" class="pa-6">
        <v-skeleton-loader type="card" rounded="xl" />
      </div>

      <div v-else-if="me">
        <!-- ── FACILITY portal ─────────────────────────────────── -->
        <template v-if="me.user_type === 'FACILITY'">
          <v-tabs v-model="facilityTab" color="primary" class="border-b">
            <v-tab value="beds">
              <v-icon start>mdi-bed-king</v-icon> Bed Counts
            </v-tab>
            <v-tab value="info">
              <v-icon start>mdi-hospital-building</v-icon> Facility Info
            </v-tab>
          </v-tabs>

          <v-window v-model="facilityTab">
            <!-- Bed update tab -->
            <v-window-item value="beds">
              <div class="pa-4">
                <div class="text-body-2 text-medium-emphasis mb-4">
                  Update your live bed availability. Changes are visible to the community instantly.
                </div>

                <v-alert v-if="bedsError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ bedsError }}</v-alert>
                <v-alert v-if="bedsSaved" type="success" variant="tonal" rounded="lg" density="compact" class="mb-3">Bed counts updated!</v-alert>

                <v-card rounded="xl" elevation="1" class="pa-4 mb-3">
                  <div class="text-subtitle-2 font-weight-bold mb-3">
                    <v-icon size="18" color="primary" class="me-1">mdi-bed-king-outline</v-icon>
                    General Beds
                  </div>
                  <v-row dense>
                    <v-col cols="6">
                      <v-text-field v-model.number="bedsForm.total_beds" label="Total Beds"
                        type="number" min="0" variant="outlined" density="compact" rounded="lg" hide-details />
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model.number="bedsForm.available_beds" label="Available"
                        type="number" min="0" variant="outlined" density="compact" rounded="lg" hide-details />
                    </v-col>
                  </v-row>
                </v-card>

                <v-card rounded="xl" elevation="1" class="pa-4 mb-4">
                  <div class="text-subtitle-2 font-weight-bold mb-3">
                    <v-icon size="18" color="error" class="me-1">mdi-heart-pulse</v-icon>
                    ICU Beds
                  </div>
                  <v-row dense>
                    <v-col cols="6">
                      <v-text-field v-model.number="bedsForm.icu_total" label="ICU Total"
                        type="number" min="0" variant="outlined" density="compact" rounded="lg" hide-details />
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model.number="bedsForm.icu_available" label="ICU Available"
                        type="number" min="0" variant="outlined" density="compact" rounded="lg" hide-details />
                    </v-col>
                  </v-row>
                </v-card>

                <v-btn color="primary" block rounded="lg" size="large" :loading="savingBeds" @click="saveBeds">
                  <v-icon start>mdi-content-save</v-icon> Save Bed Counts
                </v-btn>
              </div>
            </v-window-item>

            <!-- Facility info tab -->
            <v-window-item value="info">
              <div class="pa-4">
                <v-alert v-if="facilityError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ facilityError }}</v-alert>
                <v-alert v-if="facilitySaved" type="success" variant="tonal" rounded="lg" density="compact" class="mb-3">Facility info updated!</v-alert>

                <v-text-field v-model="facilityForm.name" label="Facility Name" variant="outlined"
                  density="comfortable" rounded="lg" class="mb-3" hide-details />
                <v-text-field v-model="facilityForm.contact_number" label="Contact Number" variant="outlined"
                  density="comfortable" rounded="lg" class="mb-3" hide-details prepend-inner-icon="mdi-phone" />
                <v-text-field v-model="facilityForm.whatsapp_number" label="WhatsApp Number" variant="outlined"
                  density="comfortable" rounded="lg" class="mb-3" hide-details prepend-inner-icon="mdi-whatsapp" />
                <v-textarea v-model="facilityForm.address" label="Address" variant="outlined"
                  density="comfortable" rounded="lg" class="mb-4" rows="2" hide-details />

                <v-btn color="primary" block rounded="lg" size="large" :loading="savingFacility" @click="saveFacility">
                  <v-icon start>mdi-content-save</v-icon> Save Info
                </v-btn>
              </div>
            </v-window-item>
          </v-window>
        </template>

        <!-- ── DOCTOR portal ──────────────────────────────────── -->
        <template v-else-if="me.user_type === 'DOCTOR'">
          <div class="pa-4">
            <!-- Availability toggle -->
            <v-card rounded="xl" elevation="2" class="mb-4">
              <v-card-text class="pa-4">
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <div class="text-subtitle-1 font-weight-bold">In Clinic Today?</div>
                    <div class="text-caption text-medium-emphasis">Toggle your live availability status</div>
                  </div>
                  <v-switch
                    v-model="doctorAvailable"
                    :color="doctorAvailable ? 'available' : 'error'"
                    hide-details
                    inset
                    :loading="toggling"
                    @update:model-value="toggleAvailability"
                  />
                </div>
                <v-chip :color="doctorAvailable ? 'available' : 'error'" variant="tonal" size="small" class="mt-2">
                  <v-icon start size="14">{{ doctorAvailable ? 'mdi-circle' : 'mdi-circle-outline' }}</v-icon>
                  {{ doctorAvailable ? 'In Clinic' : 'Away' }}
                </v-chip>
              </v-card-text>
            </v-card>

            <!-- Contact + timing update -->
            <v-alert v-if="doctorError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ doctorError }}</v-alert>
            <v-alert v-if="doctorSaved" type="success" variant="tonal" rounded="lg" density="compact" class="mb-3">Profile updated!</v-alert>

            <v-card rounded="xl" elevation="1" class="pa-4 mb-4">
              <div class="text-subtitle-2 font-weight-bold mb-3">Contact &amp; Timings</div>
              <v-text-field v-model="doctorForm.contact_number" label="Contact Number" variant="outlined"
                density="comfortable" rounded="lg" class="mb-3" hide-details prepend-inner-icon="mdi-phone" />
              <div class="text-caption text-medium-emphasis mb-2">Timing slots (JSON)</div>
              <v-textarea v-model="doctorTimingJson" label='e.g. {"Mon-Sat": "10:00–13:00"}'
                variant="outlined" density="comfortable" rounded="lg" rows="3"
                :error-messages="timingJsonError" hide-details="auto" />
            </v-card>

            <v-btn color="primary" block rounded="lg" size="large" :loading="savingDoctor" @click="saveDoctor">
              <v-icon start>mdi-content-save</v-icon> Save Profile
            </v-btn>
          </div>
        </template>

        <!-- ── ADMIN portal ───────────────────────────────────── -->
        <template v-else-if="me.user_type === 'ADMIN'">
          <div class="pa-4">
            <div class="d-flex align-center justify-space-between mb-3">
              <div class="text-subtitle-1 font-weight-bold">Portal Users</div>
              <v-btn color="primary" size="small" rounded="lg" prepend-icon="mdi-plus" @click="openCreateUser">
                Add User
              </v-btn>
            </div>

            <v-alert v-if="adminError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ adminError }}</v-alert>

            <div v-if="loadingUsers">
              <v-skeleton-loader v-for="i in 4" :key="i" type="list-item-avatar" class="mb-2" rounded="xl" />
            </div>

            <v-card v-for="user in users" :key="user.id" rounded="xl" elevation="1" class="mb-3">
              <v-card-text class="pa-3">
                <div class="d-flex align-center gap-3">
                  <v-avatar :color="userTypeColor(user.user_type)" size="40">
                    <v-icon color="white" size="20">{{ userTypeIcon(user.user_type) }}</v-icon>
                  </v-avatar>
                  <div class="flex-grow-1 min-w-0">
                    <div class="text-subtitle-2 font-weight-bold text-truncate">{{ user.username }}</div>
                    <div class="text-caption text-medium-emphasis text-truncate">
                      {{ user.profile_name || user.email }}
                    </div>
                    <div class="d-flex gap-1 mt-1">
                      <v-chip size="x-small" :color="userTypeColor(user.user_type)" variant="tonal">{{ user.user_type }}</v-chip>
                      <v-chip size="x-small" :color="user.is_active ? 'available' : 'error'" variant="tonal">
                        {{ user.is_active ? 'Active' : 'Inactive' }}
                      </v-chip>
                    </div>
                  </div>
                  <div class="d-flex gap-1 flex-shrink-0">
                    <v-btn icon size="small" variant="text" color="primary" @click="openEditUser(user)">
                      <v-icon size="18">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="small" variant="text" :color="user.is_active ? 'error' : 'available'"
                      @click="toggleUserActive(user)">
                      <v-icon size="18">{{ user.is_active ? 'mdi-account-off' : 'mdi-account-check' }}</v-icon>
                    </v-btn>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </template>
      </div>
    </v-main>

    <!-- Create / Edit user dialog (admin) -->
    <v-dialog v-model="userDialog" max-width="480">
      <v-card rounded="xl" class="pa-2">
        <v-card-title class="text-subtitle-1 font-weight-bold pa-4 pb-2">
          {{ editingUser ? 'Edit User' : 'Add Portal User' }}
        </v-card-title>
        <v-card-text class="pa-4 pt-0">
          <v-alert v-if="dialogError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ dialogError }}</v-alert>

          <template v-if="!editingUser">
            <v-text-field v-model="userForm.username" label="Username" variant="outlined"
              density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model="userForm.email" label="Email" type="email" variant="outlined"
              density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model="userForm.password" label="Password (min 8 chars)" type="password"
              variant="outlined" density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model.number="userForm.link_to_facility" label="Link to Facility ID (optional)"
              type="number" variant="outlined" density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model.number="userForm.link_to_doctor" label="Link to Doctor ID (optional)"
              type="number" variant="outlined" density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-switch v-model="userForm.is_staff" label="Admin access" color="primary" hide-details density="compact" />
          </template>

          <template v-else>
            <v-text-field v-model="userForm.email" label="Email" type="email" variant="outlined"
              density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model="userForm.password" label="New Password (leave blank to keep)" type="password"
              variant="outlined" density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-switch v-model="userForm.is_staff" label="Admin access" color="primary" hide-details density="compact" />
          </template>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0 gap-2">
          <v-btn variant="outlined" rounded="lg" @click="userDialog = false">Cancel</v-btn>
          <v-spacer />
          <v-btn color="primary" rounded="lg" :loading="savingUser" @click="saveUser">
            {{ editingUser ? 'Save Changes' : 'Create User' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  getMe,
  portalGetFacility, portalUpdateFacility,
  portalGetBeds, portalUpdateBeds,
  portalGetDoctor, portalUpdateDoctor, portalToggleDoctorStatus,
  adminGetUsers, adminCreateUser, adminUpdateUser, adminDeleteUser,
} from '@/api/index.js'

const router = useRouter()

// ── Auth ─────────────────────────────────────────────────────────────────────
const me = ref(null)
const loadingMe = ref(true)

const roleColor = computed(() => ({
  FACILITY: 'secondary', DOCTOR: 'info', ADMIN: 'error',
}[me.value?.user_type] ?? 'grey'))

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push({ name: 'login' })
}

// ── Facility ─────────────────────────────────────────────────────────────────
const facilityTab = ref('beds')
const bedsForm = reactive({ total_beds: 0, available_beds: 0, icu_total: 0, icu_available: 0 })
const facilityForm = reactive({ name: '', contact_number: '', whatsapp_number: '', address: '' })
const savingBeds = ref(false)
const savingFacility = ref(false)
const bedsError = ref(''); const bedsSaved = ref(false)
const facilityError = ref(''); const facilitySaved = ref(false)

async function loadFacilityData() {
  const [fac, beds] = await Promise.all([portalGetFacility(), portalGetBeds()])
  Object.assign(facilityForm, {
    name: fac.name, contact_number: fac.contact_number,
    whatsapp_number: fac.whatsapp_number, address: fac.address,
  })
  Object.assign(bedsForm, {
    total_beds: beds.total_beds, available_beds: beds.available_beds,
    icu_total: beds.icu_total, icu_available: beds.icu_available,
  })
}

async function saveBeds() {
  bedsError.value = ''; bedsSaved.value = false; savingBeds.value = true
  try {
    await portalUpdateBeds({ ...bedsForm })
    bedsSaved.value = true
    setTimeout(() => { bedsSaved.value = false }, 3000)
  } catch (e) {
    bedsError.value = e.response?.data?.available_beds?.[0]
      || e.response?.data?.icu_available?.[0] || 'Failed to save.'
  } finally { savingBeds.value = false }
}

async function saveFacility() {
  facilityError.value = ''; facilitySaved.value = false; savingFacility.value = true
  try {
    await portalUpdateFacility({ ...facilityForm })
    facilitySaved.value = true
    setTimeout(() => { facilitySaved.value = false }, 3000)
  } catch { facilityError.value = 'Failed to save.' }
  finally { savingFacility.value = false }
}

// ── Doctor ───────────────────────────────────────────────────────────────────
const doctorAvailable = ref(true)
const doctorForm = reactive({ contact_number: '' })
const doctorTimingJson = ref('{}')
const timingJsonError = ref('')
const toggling = ref(false)
const savingDoctor = ref(false)
const doctorError = ref(''); const doctorSaved = ref(false)

async function loadDoctorData() {
  const doc = await portalGetDoctor()
  doctorAvailable.value = doc.is_available
  doctorForm.contact_number = doc.contact_number || ''
  doctorTimingJson.value = JSON.stringify(doc.timing_slots || {}, null, 2)
}

async function toggleAvailability(val) {
  toggling.value = true
  try { await portalToggleDoctorStatus(val) }
  catch { doctorAvailable.value = !val }
  finally { toggling.value = false }
}

async function saveDoctor() {
  timingJsonError.value = ''
  let timing
  try { timing = JSON.parse(doctorTimingJson.value) } catch {
    timingJsonError.value = 'Invalid JSON format'
    return
  }
  doctorError.value = ''; doctorSaved.value = false; savingDoctor.value = true
  try {
    await portalUpdateDoctor({ contact_number: doctorForm.contact_number, timing_slots: timing })
    doctorSaved.value = true
    setTimeout(() => { doctorSaved.value = false }, 3000)
  } catch { doctorError.value = 'Failed to save.' }
  finally { savingDoctor.value = false }
}

// ── Admin ────────────────────────────────────────────────────────────────────
const users = ref([])
const loadingUsers = ref(false)
const adminError = ref('')
const userDialog = ref(false)
const editingUser = ref(null)
const savingUser = ref(false)
const dialogError = ref('')
const userForm = reactive({
  username: '', email: '', password: '', is_staff: false,
  link_to_facility: null, link_to_doctor: null,
})

const userTypeColor = (t) => ({ FACILITY: 'primary', DOCTOR: 'secondary', ADMIN: 'error' }[t] ?? 'grey')
const userTypeIcon = (t) => ({ FACILITY: 'mdi-hospital-building', DOCTOR: 'mdi-doctor', ADMIN: 'mdi-shield-crown' }[t] ?? 'mdi-account')

async function loadUsers() {
  loadingUsers.value = true
  try { users.value = await adminGetUsers() }
  catch { adminError.value = 'Failed to load users.' }
  finally { loadingUsers.value = false }
}

function openCreateUser() {
  editingUser.value = null
  Object.assign(userForm, { username: '', email: '', password: '', is_staff: false, link_to_facility: null, link_to_doctor: null })
  dialogError.value = ''
  userDialog.value = true
}

function openEditUser(user) {
  editingUser.value = user
  Object.assign(userForm, { email: user.email, password: '', is_staff: user.is_staff })
  dialogError.value = ''
  userDialog.value = true
}

async function saveUser() {
  dialogError.value = ''; savingUser.value = true
  try {
    if (editingUser.value) {
      const payload = { email: userForm.email, is_staff: userForm.is_staff }
      if (userForm.password) payload.password = userForm.password
      const updated = await adminUpdateUser(editingUser.value.id, payload)
      const idx = users.value.findIndex(u => u.id === editingUser.value.id)
      if (idx !== -1) users.value[idx] = updated
    } else {
      const payload = { ...userForm }
      if (!payload.link_to_facility) delete payload.link_to_facility
      if (!payload.link_to_doctor) delete payload.link_to_doctor
      const created = await adminCreateUser(payload)
      users.value.unshift(created)
    }
    userDialog.value = false
  } catch (e) {
    const errs = e.response?.data
    dialogError.value = errs
      ? Object.values(errs).flat().join(' ')
      : 'Failed to save user.'
  } finally { savingUser.value = false }
}

async function toggleUserActive(user) {
  try {
    if (user.is_active) {
      await adminDeleteUser(user.id)
      user.is_active = false
    } else {
      const updated = await adminUpdateUser(user.id, { is_active: true })
      user.is_active = updated.is_active
    }
  } catch { adminError.value = 'Failed to update user.' }
}

// ── Init ─────────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    me.value = await getMe()
    if (me.value.user_type === 'FACILITY') await loadFacilityData()
    else if (me.value.user_type === 'DOCTOR') await loadDoctorData()
    else if (me.value.user_type === 'ADMIN') await loadUsers()
  } catch {
    logout()
  } finally {
    loadingMe.value = false
  }
})
</script>

<style scoped>
.portal-page { min-height: 100vh; background: rgb(var(--v-theme-background)); }
.border-b { border-bottom: 1px solid rgba(0,0,0,0.08); }
.min-w-0 { min-width: 0; }
</style>
