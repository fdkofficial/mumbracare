<template>
  <div class="portal-page">
    <v-app-bar flat color="primary" elevation="0">
      <v-app-bar-title>
        <div class="text-subtitle-1 font-weight-bold text-white">Staff Portal</div>
        <div class="text-caption text-white" style="opacity:0.8">{{ me?.profile_name || me?.username }}</div>
      </v-app-bar-title>
      <template #append>
        <v-chip :color="roleColor" variant="flat" size="small" class="me-2 role-chip">{{ me?.user_type }}</v-chip>
        <v-btn icon variant="text" color="white" @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <div class="portal-shell mx-auto px-4 py-4 py-sm-6">
        <div v-if="loadingMe">
          <v-skeleton-loader type="article, actions" rounded="xl" />
        </div>

        <div v-else-if="me">
          <v-card rounded="xl" elevation="0" class="hero-card mb-4">
            <v-card-text class="pa-5 pa-sm-6">
              <div class="d-flex flex-column flex-sm-row align-sm-center justify-space-between ga-4">
                <div>
                  <div class="text-overline text-white" style="opacity:0.72">{{ roleLabel }}</div>
                  <div class="text-h6 text-sm-h5 font-weight-bold text-white mb-1">{{ roleHeading }}</div>
                  <div class="text-body-2 text-white" style="opacity:0.82">{{ roleDescription }}</div>
                </div>
                <div v-if="roleMeta" class="hero-meta text-white text-sm-right">
                  <div class="text-caption" style="opacity:0.72">Current context</div>
                  <div class="text-body-2 font-weight-medium">{{ roleMeta }}</div>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <div class="content-shell mx-auto">
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
            <v-window-item value="beds">
              <div class="pa-4 pa-sm-5">
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

            <v-window-item value="info">
              <div class="pa-4 pa-sm-5">
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

        <template v-else-if="me.user_type === 'DOCTOR'">
          <div class="pa-4 pa-sm-5">
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

        <template v-else-if="me.user_type === 'PHARMACY'">
          <div class="pa-4 pa-sm-5">
            <v-alert v-if="pharmacyError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ pharmacyError }}</v-alert>
            <v-alert v-if="pharmacySaved" type="success" variant="tonal" rounded="lg" density="compact" class="mb-3">Pharmacy info updated!</v-alert>

            <v-card rounded="xl" elevation="1" class="pa-4 mb-4">
              <div class="text-subtitle-2 font-weight-bold mb-3">Pharmacy Info</div>
              <v-text-field v-model="pharmacyForm.name" label="Pharmacy Name" variant="outlined"
                density="comfortable" rounded="lg" class="mb-3" hide-details />
              <v-text-field v-model="pharmacyForm.contact_number" label="Contact Number" variant="outlined"
                density="comfortable" rounded="lg" class="mb-3" hide-details prepend-inner-icon="mdi-phone" />
              <v-textarea v-model="pharmacyForm.address" label="Address" variant="outlined"
                density="comfortable" rounded="lg" class="mb-3" rows="2" hide-details />
              <v-switch v-model="pharmacyForm.is_24_7" label="Open 24/7" color="primary" hide-details class="mb-3" />
              <v-row v-if="!pharmacyForm.is_24_7" dense>
                <v-col cols="6">
                  <v-text-field v-model="pharmacyForm.opening_time" label="Opening Time" type="time"
                    variant="outlined" density="comfortable" rounded="lg" hide-details />
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model="pharmacyForm.closing_time" label="Closing Time" type="time"
                    variant="outlined" density="comfortable" rounded="lg" hide-details />
                </v-col>
              </v-row>
            </v-card>

            <v-btn color="primary" block rounded="lg" size="large" :loading="savingPharmacy" @click="savePharmacy">
              <v-icon start>mdi-content-save</v-icon> Save Pharmacy Info
            </v-btn>
          </div>
        </template>

        <template v-else-if="me.user_type === 'ADMIN'">
          <div class="pa-4 pa-sm-5">
            <v-row class="mb-1" dense>
              <v-col cols="6" md="3">
                <v-card rounded="xl" elevation="1" class="stat-card pa-3">
                  <div class="text-caption text-medium-emphasis">Total Users</div>
                  <div class="text-h6 font-weight-bold">{{ users.length }}</div>
                </v-card>
              </v-col>
              <v-col cols="6" md="3">
                <v-card rounded="xl" elevation="1" class="stat-card pa-3">
                  <div class="text-caption text-medium-emphasis">Active</div>
                  <div class="text-h6 font-weight-bold">{{ activeUsersCount }}</div>
                </v-card>
              </v-col>
              <v-col cols="6" md="3">
                <v-card rounded="xl" elevation="1" class="stat-card pa-3">
                  <div class="text-caption text-medium-emphasis">Linked</div>
                  <div class="text-h6 font-weight-bold">{{ linkedUsersCount }}</div>
                </v-card>
              </v-col>
              <v-col cols="6" md="3">
                <v-card rounded="xl" elevation="1" class="stat-card pa-3">
                  <div class="text-caption text-medium-emphasis">Needs Setup</div>
                  <div class="text-h6 font-weight-bold">{{ unlinkedUsersCount }}</div>
                </v-card>
              </v-col>
            </v-row>

            <div class="d-flex align-center justify-space-between mb-3">
              <div class="text-subtitle-1 font-weight-bold">Portal Users</div>
              <v-btn color="primary" size="small" rounded="lg" prepend-icon="mdi-plus" @click="openCreateUser">
                Add User
              </v-btn>
            </div>

            <v-text-field
              v-model="userSearch"
              label="Search users"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="comfortable"
              rounded="lg"
              hide-details
              class="mb-3"
            />

            <v-alert v-if="adminError" type="error" variant="tonal" rounded="lg" density="compact" class="mb-3">{{ adminError }}</v-alert>

            <div v-if="loadingUsers">
              <v-skeleton-loader v-for="i in 4" :key="i" type="list-item-avatar" class="mb-2" rounded="xl" />
            </div>

            <v-card v-for="user in filteredUsers" :key="user.id" rounded="xl" elevation="1" class="mb-3">
              <v-card-text class="pa-3">
                <div class="d-flex align-center gap-3">
                  <v-avatar :color="userTypeColor(user.user_type)" size="40">
                    <v-icon color="white" size="20">{{ userTypeIcon(user.user_type) }}</v-icon>
                  </v-avatar>
                  <div class="flex-grow-1 min-w-0">
                    <div class="text-subtitle-2 font-weight-bold text-truncate">{{ user.username }}</div>
                    <div class="text-caption text-medium-emphasis text-truncate">
                      {{ user.profile_name || user.email || 'Unlinked account' }}
                    </div>
                    <div class="d-flex gap-1 mt-1">
                      <v-chip size="x-small" :color="userTypeColor(user.user_type)" variant="tonal">{{ user.user_type }}</v-chip>
                      <v-chip size="x-small" :color="user.is_active ? 'available' : 'error'" variant="tonal">
                        {{ user.is_active ? 'Active' : 'Inactive' }}
                      </v-chip>
                      <v-chip v-if="user.user_type === 'STAFF'" size="x-small" color="warning" variant="tonal">
                        Needs linking
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

        <template v-else>
          <div class="pa-4 pa-sm-5">
            <v-alert type="warning" variant="tonal" rounded="xl" class="mb-4">
              This account is active, but it is not linked to a facility, doctor, pharmacy, or admin role yet.
            </v-alert>
            <v-card rounded="xl" elevation="1" class="pa-4">
              <div class="text-subtitle-1 font-weight-bold mb-2">Account setup required</div>
              <div class="text-body-2 text-medium-emphasis mb-4">
                Ask an administrator to link this user before using the staff portal.
              </div>
              <v-btn variant="outlined" rounded="lg" @click="logout">Sign Out</v-btn>
            </v-card>
          </div>
        </template>
          </div>
      </div>
      </div>
    </v-main>

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
            <v-switch v-model="userForm.is_staff" label="Admin access" color="primary" hide-details density="compact" />
            <v-radio-group v-if="!userForm.is_staff" v-model="linkType" inline density="compact" class="mt-2 mb-1">
              <v-radio label="Facility" value="FACILITY" />
              <v-radio label="Doctor" value="DOCTOR" />
              <v-radio label="Pharmacy" value="PHARMACY" />
            </v-radio-group>
            <v-autocomplete
              v-if="!userForm.is_staff"
              v-model="selectedLinkId"
              :items="linkOptions"
              item-title="label"
              item-value="value"
              :label="linkLabel"
              variant="outlined"
              density="comfortable"
              rounded="lg"
              class="mb-2"
              hide-details
              clearable
            />
          </template>

          <template v-else>
            <v-text-field v-model="userForm.email" label="Email" type="email" variant="outlined"
              density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-text-field v-model="userForm.password" label="New Password (leave blank to keep)" type="password"
              variant="outlined" density="comfortable" rounded="lg" class="mb-2" hide-details />
            <v-switch v-model="userForm.is_staff" label="Admin access" color="primary" hide-details density="compact" />
            <v-radio-group v-if="!userForm.is_staff" v-model="linkType" inline density="compact" class="mt-2 mb-1">
              <v-radio label="Facility" value="FACILITY" />
              <v-radio label="Doctor" value="DOCTOR" />
              <v-radio label="Pharmacy" value="PHARMACY" />
            </v-radio-group>
            <v-autocomplete
              v-if="!userForm.is_staff"
              v-model="selectedLinkId"
              :items="linkOptions"
              item-title="label"
              item-value="value"
              :label="linkLabel"
              variant="outlined"
              density="comfortable"
              rounded="lg"
              class="mb-2"
              hide-details
              clearable
            />
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
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  getMe,
  fetchFacilities, fetchDoctors, fetchPharmacies,
  portalGetFacility, portalUpdateFacility,
  portalGetBeds, portalUpdateBeds,
  portalGetDoctor, portalUpdateDoctor, portalToggleDoctorStatus,
  portalGetPharmacy, portalUpdatePharmacy,
  adminGetUsers, adminCreateUser, adminUpdateUser, adminDeleteUser,
} from '@/api/index.js'

const router = useRouter()

const me = ref(null)
const loadingMe = ref(true)
const userSearch = ref('')
const linkType = ref('FACILITY')
const facilityOptions = ref([])
const doctorOptions = ref([])
const pharmacyOptions = ref([])

const roleColor = computed(() => ({
  FACILITY: 'secondary', DOCTOR: 'info', PHARMACY: 'success', ADMIN: 'error',
}[me.value?.user_type] ?? 'grey'))

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push({ name: 'login' })
}

const roleLabel = computed(() => ({
  FACILITY: 'Facility Portal',
  DOCTOR: 'Doctor Portal',
  PHARMACY: 'Pharmacy Portal',
  ADMIN: 'Admin Portal',
  UNKNOWN: 'Account Setup',
}[me.value?.user_type] ?? 'Portal'))

const roleHeading = computed(() => ({
  FACILITY: 'Update facility details and bed availability',
  DOCTOR: 'Manage your profile and live availability',
  PHARMACY: 'Keep pharmacy hours and contact details current',
  ADMIN: 'Manage staff access and profile linking',
  UNKNOWN: 'This account still needs profile linkage',
}[me.value?.user_type] ?? 'Portal access'))

const roleDescription = computed(() => ({
  FACILITY: 'Use this area to keep live capacity data and hospital information accurate for patients and volunteers.',
  DOCTOR: 'Use this panel to control whether you are in clinic and publish accurate timing/contact details.',
  PHARMACY: 'Use this panel to maintain hours, address, and contact details for the pharmacy listing.',
  ADMIN: 'Create accounts, repair unlinked logins, and assign users to the correct operational profile.',
  UNKNOWN: 'An administrator must connect this account to a hospital, doctor, pharmacy, or admin role before it can be used.',
}[me.value?.user_type] ?? ''))

const roleMeta = computed(() => {
  if (!me.value) return ''
  if (me.value.user_type === 'ADMIN') return `${activeUsersCount.value} active accounts`
  return me.value.profile_name || me.value.username
})

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

const pharmacyForm = reactive({
  name: '',
  contact_number: '',
  address: '',
  is_24_7: false,
  opening_time: '',
  closing_time: '',
})
const savingPharmacy = ref(false)
const pharmacyError = ref(''); const pharmacySaved = ref(false)

async function loadPharmacyData() {
  const pharmacy = await portalGetPharmacy()
  Object.assign(pharmacyForm, {
    name: pharmacy.name,
    contact_number: pharmacy.contact_number || '',
    address: pharmacy.address || '',
    is_24_7: pharmacy.is_24_7,
    opening_time: pharmacy.opening_time || '',
    closing_time: pharmacy.closing_time || '',
  })
}

async function savePharmacy() {
  pharmacyError.value = ''; pharmacySaved.value = false; savingPharmacy.value = true
  try {
    await portalUpdatePharmacy({
      ...pharmacyForm,
      opening_time: pharmacyForm.is_24_7 ? null : (pharmacyForm.opening_time || null),
      closing_time: pharmacyForm.is_24_7 ? null : (pharmacyForm.closing_time || null),
    })
    pharmacySaved.value = true
    setTimeout(() => { pharmacySaved.value = false }, 3000)
  } catch {
    pharmacyError.value = 'Failed to save.'
  } finally { savingPharmacy.value = false }
}

const users = ref([])
const loadingUsers = ref(false)
const adminError = ref('')
const userDialog = ref(false)
const editingUser = ref(null)
const savingUser = ref(false)
const dialogError = ref('')
const userForm = reactive({
  username: '', email: '', password: '', is_staff: false,
  link_to_facility: null, link_to_doctor: null, link_to_pharmacy: null,
})

const userTypeColor = (t) => ({ FACILITY: 'primary', DOCTOR: 'secondary', PHARMACY: 'success', ADMIN: 'error' }[t] ?? 'grey')
const userTypeIcon = (t) => ({ FACILITY: 'mdi-hospital-building', DOCTOR: 'mdi-doctor', PHARMACY: 'mdi-pill', ADMIN: 'mdi-shield-crown' }[t] ?? 'mdi-account')
const activeUsersCount = computed(() => users.value.filter(user => user.is_active).length)
const linkedUsersCount = computed(() => users.value.filter(user => user.user_type !== 'STAFF').length)
const unlinkedUsersCount = computed(() => users.value.filter(user => user.user_type === 'STAFF').length)
const filteredUsers = computed(() => {
  const term = userSearch.value.trim().toLowerCase()
  if (!term) return users.value
  return users.value.filter((user) => {
    const haystack = [
      user.username,
      user.email,
      user.profile_name,
      user.user_type,
    ].filter(Boolean).join(' ').toLowerCase()
    return haystack.includes(term)
  })
})

const linkOptions = computed(() => ({
  FACILITY: facilityOptions.value,
  DOCTOR: doctorOptions.value,
  PHARMACY: pharmacyOptions.value,
}[linkType.value] ?? []))

const linkLabel = computed(() => ({
  FACILITY: 'Select facility',
  DOCTOR: 'Select doctor',
  PHARMACY: 'Select pharmacy',
}[linkType.value] ?? 'Select profile'))

const selectedLinkId = computed({
  get() {
    if (linkType.value === 'FACILITY') return userForm.link_to_facility
    if (linkType.value === 'DOCTOR') return userForm.link_to_doctor
    if (linkType.value === 'PHARMACY') return userForm.link_to_pharmacy
    return null
  },
  set(value) {
    userForm.link_to_facility = null
    userForm.link_to_doctor = null
    userForm.link_to_pharmacy = null
    if (linkType.value === 'FACILITY') userForm.link_to_facility = value
    if (linkType.value === 'DOCTOR') userForm.link_to_doctor = value
    if (linkType.value === 'PHARMACY') userForm.link_to_pharmacy = value
  },
})

function normalizeCollection(data) {
  if (Array.isArray(data)) return data
  return data?.results ?? []
}

function formatFacilityOption(item) {
  return { value: item.id, label: `${item.name} • ${item.area_display || item.area}` }
}

function formatDoctorOption(item) {
  return { value: item.id, label: `${item.name} • ${item.specialty_display || item.specialty}` }
}

function formatPharmacyOption(item) {
  return { value: item.id, label: `${item.name} • ${item.area_display || item.area}` }
}

async function loadLinkOptions() {
  const [facilities, doctors, pharmacies] = await Promise.all([
    fetchFacilities(),
    fetchDoctors(),
    fetchPharmacies(),
  ])
  facilityOptions.value = normalizeCollection(facilities).map(formatFacilityOption)
  doctorOptions.value = normalizeCollection(doctors).map(formatDoctorOption)
  pharmacyOptions.value = normalizeCollection(pharmacies).map(formatPharmacyOption)
}

async function loadUsers() {
  loadingUsers.value = true
  try { users.value = await adminGetUsers() }
  catch { adminError.value = 'Failed to load users.' }
  finally { loadingUsers.value = false }
}

function openCreateUser() {
  editingUser.value = null
  linkType.value = 'FACILITY'
  Object.assign(userForm, {
    username: '', email: '', password: '', is_staff: false,
    link_to_facility: null, link_to_doctor: null, link_to_pharmacy: null,
  })
  dialogError.value = ''
  userDialog.value = true
}

function openEditUser(user) {
  editingUser.value = user
  linkType.value = user.user_type === 'DOCTOR' || user.user_type === 'PHARMACY' ? user.user_type : 'FACILITY'
  Object.assign(userForm, {
    email: user.email,
    password: '',
    is_staff: user.is_staff,
    link_to_facility: user.user_type === 'FACILITY' ? user.profile_id : null,
    link_to_doctor: user.user_type === 'DOCTOR' ? user.profile_id : null,
    link_to_pharmacy: user.user_type === 'PHARMACY' ? user.profile_id : null,
  })
  dialogError.value = ''
  userDialog.value = true
}

watch(() => userForm.is_staff, (isStaff) => {
  if (isStaff) {
    userForm.link_to_facility = null
    userForm.link_to_doctor = null
    userForm.link_to_pharmacy = null
  }
})

watch(linkType, () => {
  if (userForm.is_staff) return
  selectedLinkId.value = null
})

async function saveUser() {
  dialogError.value = ''; savingUser.value = true
  try {
    if (editingUser.value) {
      const payload = {
        email: userForm.email,
        is_staff: userForm.is_staff,
        link_to_facility: userForm.link_to_facility || null,
        link_to_doctor: userForm.link_to_doctor || null,
        link_to_pharmacy: userForm.link_to_pharmacy || null,
      }
      if (userForm.password) payload.password = userForm.password
      const updated = await adminUpdateUser(editingUser.value.id, payload)
      const idx = users.value.findIndex(u => u.id === editingUser.value.id)
      if (idx !== -1) users.value[idx] = updated
    } else {
      const payload = { ...userForm }
      if (!payload.link_to_facility) delete payload.link_to_facility
      if (!payload.link_to_doctor) delete payload.link_to_doctor
      if (!payload.link_to_pharmacy) delete payload.link_to_pharmacy
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

onMounted(async () => {
  try {
    me.value = await getMe()
    if (me.value.user_type === 'FACILITY') await loadFacilityData()
    else if (me.value.user_type === 'DOCTOR') await loadDoctorData()
    else if (me.value.user_type === 'PHARMACY') await loadPharmacyData()
    else if (me.value.user_type === 'ADMIN') {
      await Promise.all([loadUsers(), loadLinkOptions()])
    }
  } catch {
    logout()
  } finally {
    loadingMe.value = false
  }
})
</script>

<style scoped>
.portal-page { min-height: 100vh; background: rgb(var(--v-theme-background)); }
.portal-shell { max-width: 1180px; }
.content-shell { max-width: 760px; }
.hero-card {
  background:
    radial-gradient(circle at top right, rgba(255,255,255,0.18), transparent 34%),
    linear-gradient(135deg, #00695c 0%, #0288d1 100%);
}
.hero-meta { min-width: 160px; }
.stat-card { height: 100%; }
.border-b { border-bottom: 1px solid rgba(0,0,0,0.08); }
.min-w-0 { min-width: 0; }
@media (max-width: 600px) {
  .role-chip { display: none; }
}
</style>
