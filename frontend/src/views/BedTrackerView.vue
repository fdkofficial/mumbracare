<template>
  <div>
    <!-- App Bar -->
    <v-app-bar flat color="primary" elevation="0">
      <v-app-bar-title>
        <div>
          <div class="text-subtitle-1 font-weight-bold text-white">{{ $t('beds.title') }}</div>
          <div class="text-caption text-white opacity-80">{{ $t('beds.subtitle') }}</div>
        </div>
      </v-app-bar-title>
      <template #append>
        <v-btn icon variant="text" color="white" @click="refresh">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <!-- Area Filter -->
      <div class="filter-strip px-4 py-3">
        <div class="d-flex gap-2 overflow-x-auto hide-scrollbar">
          <v-chip
            v-for="area in areas"
            :key="area.key"
            :color="store.selectedArea === area.key ? 'primary' : undefined"
            :variant="store.selectedArea === area.key ? 'flat' : 'outlined'"
            rounded="lg"
            @click="selectArea(area.key)"
          >
            {{ $t(`area.${area.key}`) }}
          </v-chip>
        </div>
      </div>

      <!-- Summary row -->
      <div v-if="!store.loading && store.filtered.length" class="px-4 mb-2">
        <div class="d-flex align-center gap-3">
          <v-chip color="available" variant="tonal" size="small">
            <v-icon start size="14">mdi-check-circle</v-icon>
            {{ store.summary.available }} {{ $t('beds.available') }}
          </v-chip>
          <v-chip color="error" variant="tonal" size="small">
            <v-icon start size="14">mdi-close-circle</v-icon>
            {{ store.summary.full }} {{ $t('beds.full') }}
          </v-chip>
          <v-spacer />
          <span v-if="store.lastRefreshed" class="text-caption text-medium-emphasis">
            {{ refreshedText }}
          </span>
        </div>
      </div>

      <!-- Loading skeletons -->
      <div v-if="store.loading" class="px-4">
        <v-skeleton-loader
          v-for="i in 3"
          :key="i"
          type="card"
          class="mb-3"
          rounded="xl"
        />
      </div>

      <!-- Error state -->
      <div v-else-if="store.error" class="px-4">
        <v-alert type="error" rounded="xl" variant="tonal">
          <div>{{ store.error }}</div>
          <v-btn class="mt-2" variant="tonal" size="small" @click="refresh">
            {{ $t('common.retry') }}
          </v-btn>
        </v-alert>
      </div>

      <!-- Empty state -->
      <div v-else-if="!store.filtered.length" class="px-4 py-12 text-center">
        <v-icon size="72" color="medium-emphasis" class="mb-4">mdi-hospital-off</v-icon>
        <div class="text-body-1 text-medium-emphasis">{{ $t('beds.no_data') }}</div>
      </div>

      <!-- Facility cards -->
      <div v-else class="px-4">
        <BedStatusCard
          v-for="facility in store.filtered"
          :key="facility.id"
          :facility="facility"
          class="mb-3"
        />
      </div>

      <div style="height: 80px;" />
    </v-main>

    <EmergencyFab />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBedsStore } from '@/stores/beds'
import BedStatusCard from '@/components/BedStatusCard.vue'
import EmergencyFab from '@/components/EmergencyFab.vue'

const { t } = useI18n()
const store = useBedsStore()

const areas = [
  { key: 'ALL' },
  { key: 'KAUSA' },
  { key: 'AMRUT_NAGAR' },
  { key: 'STATION_ROAD' },
]

const refreshedText = computed(() => {
  if (!store.lastRefreshed) return ''
  const diff = Math.floor((Date.now() - store.lastRefreshed) / 60000)
  return diff < 1 ? 'Just refreshed' : `${diff}m ago`
})

function selectArea(area) {
  store.setArea(area)
  store.load(area === 'ALL' ? null : area)
}

function refresh() {
  store.load(store.selectedArea === 'ALL' ? null : store.selectedArea)
}

onMounted(() => {
  if (!store.facilities.length) store.load()
})
</script>

<style scoped>
.filter-strip { background: rgb(var(--v-theme-surface)); border-bottom: 1px solid rgba(0,0,0,0.06); }
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
