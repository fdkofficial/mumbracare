<template>
  <div>
    <v-app-bar flat color="secondary" elevation="0">
      <v-app-bar-title>
        <div>
          <div class="text-subtitle-1 font-weight-bold text-white">{{ $t('doctors.title') }}</div>
          <div class="text-caption text-white opacity-80">{{ $t('doctors.subtitle') }}</div>
        </div>
      </v-app-bar-title>
      <template #append>
        <v-btn icon variant="text" color="white" @click="store.load()">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <!-- Search + Filters -->
      <div class="filter-section px-4 pt-3 pb-1">
        <!-- Search bar -->
        <v-text-field
          v-model="store.searchQuery"
          :placeholder="$t('doctors.search')"
          prepend-inner-icon="mdi-magnify"
          clearable
          hide-details
          density="compact"
          variant="outlined"
          rounded="lg"
          class="mb-3"
        />

        <!-- Availability toggle -->
        <v-chip-group v-model="availabilityFilter" color="primary" mandatory class="mb-2" selected-class="availability-active">
          <v-chip value="all" variant="outlined" size="small" rounded="pill">All</v-chip>
          <v-chip value="available" color="available" variant="outlined" size="small" rounded="pill">
            <v-icon start size="12">mdi-circle</v-icon>
            {{ $t('doctors.in_clinic') }}
          </v-chip>
          <v-chip value="away" color="error" variant="outlined" size="small" rounded="pill">
            <v-icon start size="12">mdi-circle-outline</v-icon>
            {{ $t('doctors.away') }}
          </v-chip>
        </v-chip-group>

        <!-- Specialty filter -->
        <div class="filter-label mb-1">{{ $t('doctors.all_specialties') }}</div>
        <v-chip-group
          v-model="store.selectedSpecialty"
          color="secondary"
          mandatory
          selected-class="v-chip--selected"
          class="mb-2"
        >
          <v-chip
            v-for="spec in specialties"
            :key="spec.key"
            :value="spec.key"
            variant="outlined"
            size="small"
            rounded="pill"
          >
            {{ specialtyLabel(spec.key) }}
          </v-chip>
        </v-chip-group>

        <!-- Area filter -->
        <div class="filter-label mb-1">Area</div>
        <v-chip-group
          v-model="store.selectedArea"
          color="primary"
          mandatory
          selected-class="v-chip--selected"
          class="mb-1"
        >
          <v-chip
            v-for="area in areas"
            :key="area.key"
            :value="area.key"
            variant="outlined"
            size="small"
            rounded="pill"
          >
            {{ $t(`area.${area.key}`) }}
          </v-chip>
        </v-chip-group>
      </div>

      <!-- Count -->
      <div v-if="!store.loading" class="px-4 py-2">
        <span class="text-caption text-medium-emphasis">
          {{ displayedDoctors.length }} doctor{{ displayedDoctors.length === 1 ? '' : 's' }} found
        </span>
      </div>

      <!-- Skeleton loaders -->
      <div v-if="store.loading" class="px-4">
        <v-skeleton-loader v-for="i in 4" :key="i" type="list-item-avatar-three-line" class="mb-3" rounded="xl" />
      </div>

      <!-- Error -->
      <div v-else-if="store.error" class="px-4">
        <v-alert type="error" rounded="xl" variant="tonal">
          {{ store.error }}
          <v-btn class="mt-2" variant="tonal" size="small" @click="store.load()">{{ $t('common.retry') }}</v-btn>
        </v-alert>
      </div>

      <!-- Empty -->
      <div v-else-if="!displayedDoctors.length" class="px-4 py-12 text-center">
        <v-icon size="72" color="medium-emphasis" class="mb-4">mdi-doctor</v-icon>
        <div class="text-body-1 text-medium-emphasis">{{ $t('doctors.no_data') }}</div>
      </div>

      <!-- Doctor cards -->
      <div v-else class="px-4">
        <DoctorCard
          v-for="doctor in displayedDoctors"
          :key="doctor.id"
          :doctor="doctor"
          class="mb-3"
        />
      </div>

      <div style="height: 80px;" />
    </v-main>

    <EmergencyFab />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDoctorsStore } from '@/stores/doctors'
import DoctorCard from '@/components/DoctorCard.vue'
import EmergencyFab from '@/components/EmergencyFab.vue'

const { t } = useI18n()
const store = useDoctorsStore()

const availabilityFilter = ref('all')

const specialties = [
  { key: 'ALL' }, { key: 'GENERAL' }, { key: 'CARDIAC' }, { key: 'PEDIATRIC' },
  { key: 'GYNAE' }, { key: 'ORTHO' }, { key: 'DERM' }, { key: 'ENT' },
]

// Short labels for specialty chips to prevent truncation
const SPECIALTY_SHORT = {
  ALL: 'All', GENERAL: 'GP', CARDIAC: 'Cardiac', PEDIATRIC: 'Paediatric',
  GYNAE: 'Gynae', ORTHO: 'Ortho', DERM: 'Derm', ENT: 'ENT',
}
function specialtyLabel(key) {
  return SPECIALTY_SHORT[key] ?? key
}
const areas = [
  { key: 'ALL' }, { key: 'KAUSA' }, { key: 'AMRUT_NAGAR' }, { key: 'STATION_ROAD' },
]

const displayedDoctors = computed(() => {
  let result = store.filtered
  if (availabilityFilter.value === 'available') result = result.filter(d => d.is_available)
  if (availabilityFilter.value === 'away') result = result.filter(d => !d.is_available)
  return result
})

onMounted(() => { if (!store.doctors.length) store.load() })
</script>

<style scoped>
.filter-section { background: rgb(var(--v-theme-surface)); border-bottom: 1px solid rgba(0,0,0,0.06); }
.filter-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; color: rgba(var(--v-theme-on-surface), 0.5); }
</style>
