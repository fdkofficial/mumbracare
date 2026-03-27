<template>
  <div>
    <v-app-bar flat color="primary" elevation="0">
      <v-app-bar-title>
        <div>
          <div class="text-subtitle-1 font-weight-bold text-white">{{ $t('pharmacies.title') }}</div>
          <div class="text-caption text-white opacity-80">{{ $t('pharmacies.subtitle') }}</div>
        </div>
      </v-app-bar-title>
      <template #append>
        <v-btn icon variant="text" color="white" @click="store.load()">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <!-- Filters -->
      <div class="filter-section px-4 pt-4 pb-2">
        <!-- 24/7 toggle -->
        <v-switch
          v-model="store.onlyNight"
          color="primary"
          hide-details
          density="compact"
          class="mb-2"
        >
          <template #label>
            <span class="text-body-2 font-weight-medium">
              <v-icon size="16" class="me-1" color="primary">mdi-moon-waxing-crescent</v-icon>
              {{ $t('pharmacies.night_only') }}
            </span>
          </template>
        </v-switch>

        <!-- Area chips -->
        <div class="d-flex gap-2 overflow-x-auto hide-scrollbar pb-1">
          <v-chip
            v-for="area in areas"
            :key="area.key"
            :color="store.selectedArea === area.key ? 'primary' : undefined"
            :variant="store.selectedArea === area.key ? 'flat' : 'outlined'"
            size="small"
            rounded="lg"
            @click="store.selectedArea = area.key"
          >
            {{ $t(`area.${area.key}`) }}
          </v-chip>
        </div>
      </div>

      <!-- Count -->
      <div v-if="!store.loading" class="px-4 py-2">
        <span class="text-caption text-medium-emphasis">
          {{ store.filtered.length }} store{{ store.filtered.length === 1 ? '' : 's' }} found
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
      <div v-else-if="!store.filtered.length" class="px-4 py-12 text-center">
        <v-icon size="72" color="medium-emphasis" class="mb-4">mdi-pill-off</v-icon>
        <div class="text-body-1 text-medium-emphasis">{{ $t('pharmacies.no_data') }}</div>
      </div>

      <!-- Pharmacy cards -->
      <div v-else class="px-4">
        <!-- 24/7 section at top -->
        <div v-if="twentyFourSeven.length && !store.onlyNight" class="mb-2">
          <div class="text-overline text-medium-emphasis ps-1 mb-1">
            <v-icon size="14" color="available" class="me-1">mdi-clock-check-outline</v-icon>
            Open 24 / 7
          </div>
          <PharmacyCard
            v-for="pharmacy in twentyFourSeven"
            :key="pharmacy.id"
            :pharmacy="pharmacy"
            class="mb-3"
          />
        </div>

        <!-- Other stores -->
        <div v-if="regular.length && !store.onlyNight">
          <div class="text-overline text-medium-emphasis ps-1 mb-1">
            <v-icon size="14" color="primary" class="me-1">mdi-store-outline</v-icon>
            Day Stores
          </div>
          <PharmacyCard
            v-for="pharmacy in regular"
            :key="pharmacy.id"
            :pharmacy="pharmacy"
            class="mb-3"
          />
        </div>

        <!-- When night filter is on -->
        <div v-if="store.onlyNight">
          <PharmacyCard
            v-for="pharmacy in store.filtered"
            :key="pharmacy.id"
            :pharmacy="pharmacy"
            class="mb-3"
          />
        </div>
      </div>

      <div style="height: 80px;" />
    </v-main>

    <EmergencyFab />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { usePharmaciesStore } from '@/stores/pharmacies'
import PharmacyCard from '@/components/PharmacyCard.vue'
import EmergencyFab from '@/components/EmergencyFab.vue'

const { t } = useI18n()
const store = usePharmaciesStore()

const areas = [
  { key: 'ALL' }, { key: 'KAUSA' }, { key: 'AMRUT_NAGAR' }, { key: 'STATION_ROAD' },
]

const twentyFourSeven = computed(() => store.filtered.filter(p => p.is_24_7))
const regular = computed(() => store.filtered.filter(p => !p.is_24_7))

onMounted(() => { if (!store.pharmacies.length) store.load() })
</script>

<style scoped>
.filter-section { background: rgb(var(--v-theme-surface)); border-bottom: 1px solid rgba(0,0,0,0.06); }
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
