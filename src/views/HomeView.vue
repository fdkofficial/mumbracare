<template>
  <div class="home-view">
    <!-- Hero Banner -->
    <div class="hero-section">
      <!-- Top row: controls only -->
      <div class="d-flex align-center justify-end gap-1 mb-3">
        <LanguageSwitcher />
        <v-btn icon variant="text" size="small" color="white" @click="toggleDark">
          <v-icon size="20">{{ appStore.darkMode ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
        </v-btn>
        <v-btn icon variant="text" size="small" color="white" :to="{ name: 'login' }" aria-label="Staff Portal">
          <v-icon size="20">mdi-account-key-outline</v-icon>
        </v-btn>
      </div>

      <!-- Title block: full width, no competition -->
      <div class="mb-3">
        <h1 class="text-h4 font-weight-black text-white mb-1 hero-title">{{ $t('home.hero_title') }}</h1>
        <p class="text-body-2 text-white hero-subtitle mb-0">{{ $t('home.hero_subtitle') }}</p>
      </div>

      <!-- Emergency tip -->
      <v-alert
        type="warning"
        variant="tonal"
        density="compact"
        rounded="lg"
        icon="mdi-alert-circle-outline"
        class="emergency-alert"
      >
        <span class="text-caption">{{ $t('home.emergency_tip') }}</span>
      </v-alert>
    </div>

    <!-- Live Summary Strip -->
    <div class="summary-strip px-4 py-3">
      <v-row dense class="mt-4">
        <v-col v-for="stat in summaryStats" :key="stat.label" cols="4">
          <v-card :color="stat.color" variant="tonal" rounded="xl" elevation="2" class="stat-card text-center py-3 px-1">
            <div class="text-h5 font-weight-black stat-value">{{ stat.value }}</div>
            <div class="text-caption font-weight-medium stat-label mt-1">{{ stat.label }}</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Quick Action Cards -->
    <div class="cards-section px-4">
      <!-- Bed Tracker -->
      <v-card rounded="xl" elevation="2" class="action-card mb-3" @click="router.push('/beds')">
        <v-card-text class="d-flex align-center pa-4 gap-3">
          <v-avatar size="52" color="available" class="flex-shrink-0">
            <v-icon icon="mdi-bed-king" size="28" color="white" />
          </v-avatar>
          <div class="flex-grow-1 min-w-0 ms-3">
            <div class="text-subtitle-1 font-weight-bold">{{ $t('home.bed_tracker') }}</div>
            <div class="text-caption text-medium-emphasis">{{ $t('home.bed_tracker_desc') }}</div>
          </div>
          <v-icon size="20" color="medium-emphasis" class="flex-shrink-0">mdi-chevron-right</v-icon>
        </v-card-text>
        <div class="live-strip d-flex align-center px-4 pb-3 pt-0">
          <span class="live-dot me-2"></span>
          <span class="text-caption text-medium-emphasis font-weight-medium">LIVE</span>
          <v-spacer />
          <span v-if="bedsStore.summary.available > 0" class="text-caption text-success font-weight-bold">
            {{ bedsStore.summary.available }} {{ $t('beds.available') }}
          </span>
        </div>
      </v-card>

      <!-- Doctors -->
      <v-card rounded="xl" elevation="2" class="action-card mb-3" @click="router.push('/doctors')">
        <v-card-text class="d-flex align-center pa-4 gap-3">
          <v-avatar size="52" color="secondary" class="flex-shrink-0">
            <v-icon icon="mdi-doctor" size="28" color="white" />
          </v-avatar>
          <div class="flex-grow-1 min-w-0  ms-3">
            <div class="text-subtitle-1 font-weight-bold">{{ $t('home.doctors') }}</div>
            <div class="text-caption text-medium-emphasis">{{ $t('home.doctors_desc') }}</div>
          </div>
          <v-icon size="20" color="medium-emphasis" class="flex-shrink-0">mdi-chevron-right</v-icon>
        </v-card-text>  
      </v-card>

      <!-- Pharmacies -->
      <v-card rounded="xl" elevation="2" class="action-card mb-3" @click="router.push('/pharmacies')">
        <v-card-text class="d-flex align-center pa-4 gap-3">
          <v-avatar size="52" color="teal-darken-2" class="flex-shrink-0">
            <v-icon icon="mdi-pill-multiple" size="28" color="white" />
          </v-avatar>
          <div class="flex-grow-1 min-w-0  ms-3">
            <div class="text-subtitle-1 font-weight-bold">{{ $t('home.pharmacies') }}</div>
            <div class="text-caption text-medium-emphasis">{{ $t('home.pharmacies_desc') }}</div>
          </div>
          <v-icon size="20" color="medium-emphasis" class="flex-shrink-0">mdi-chevron-right</v-icon>
        </v-card-text>
      </v-card>

      <!-- WhatsApp Help -->
      <v-card rounded="xl" elevation="2" color="whatsapp" class="action-card mb-1" @click="openWhatsApp">
        <v-card-text class="d-flex align-center pa-4 gap-3">
          <v-avatar size="52" color="white" class="flex-shrink-0">
            <v-icon icon="mdi-whatsapp" size="28" color="whatsapp" />
          </v-avatar>
          <div class="flex-grow-1 min-w-0  ms-3">
            <div class="text-subtitle-1 font-weight-bold text-white">{{ $t('home.whatsapp_help') }}</div>
            <div class="text-caption text-white" style="opacity:0.85">{{ $t('home.whatsapp_desc') }}</div>
          </div>
          <v-icon size="20" color="white" class="flex-shrink-0">mdi-chevron-right</v-icon>
        </v-card-text>
      </v-card>
    </div>

    <!-- Area quick-links -->
    <div class="px-4 pt-4 pb-4">
      <div class="section-label mb-3">Browse by area</div>
      <v-row dense>
        <v-col v-for="area in areas" :key="area.key" cols="4">
          <v-card
            rounded="xl"
            variant="outlined"
            class="area-card text-center pa-3"
            @click="goToBedsByArea(area.key)"
          >
            <v-icon size="26" color="primary">mdi-map-marker</v-icon>
            <div class="text-caption font-weight-semibold mt-1">{{ $t(`area.${area.key}`) }}</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <div style="height: 80px;" />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'
import { useBedsStore } from '@/stores/beds'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

const { t } = useI18n()
const router = useRouter()
const appStore = useAppStore()
const bedsStore = useBedsStore()

const COMMUNITY_WHATSAPP = '919XXXXXXXXX'
const areas = [
  { key: 'KAUSA' },
  { key: 'AMRUT_NAGAR' },
  { key: 'STATION_ROAD' },
]

const summaryStats = computed(() => [
  { label: t('beds.available'), value: bedsStore.summary.available, color: 'available' },
  { label: t('beds.low'),       value: 0,                            color: 'warning' },
  { label: t('beds.full'),      value: bedsStore.summary.full,       color: 'error' },
])

function toggleDark() {
  appStore.toggleDark()
}

function openWhatsApp() {
  const msg = encodeURIComponent(t('whatsapp.default_message'))
  window.open(`https://wa.me/${COMMUNITY_WHATSAPP}?text=${msg}`, '_blank', 'noopener,noreferrer')
}

function goToBedsByArea(area) {
  bedsStore.setArea(area)
  router.push('/beds')
}

onMounted(() => bedsStore.load())
</script>

<style scoped>
.home-view {
  background: rgb(var(--v-theme-background));
  min-height: 100vh;
}

/* ── Hero ── */
.hero-section {
  background: linear-gradient(135deg, #00695C 0%, #0288D1 100%);
  padding: 14px 16px 32px;
}

.hero-title {
  line-height: 1.15;
  letter-spacing: -0.3px;
}

.hero-subtitle {
  opacity: 0.82;
  line-height: 1.4;
}

.emergency-alert {
  background: rgba(255, 255, 255, 0.12) !important;
}

/* ── Summary strip ── */
.summary-strip {
  margin-top: -18px;
  position: relative;
  z-index: 1;
}

.stat-card {
  border: none;
}

.stat-value {
  line-height: 1;
}

.stat-label {
  opacity: 0.75;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* ── Action cards ── */
.cards-section {
  padding-top: 4px;
  padding-bottom: 0;
}

.action-card {
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.action-card:active {
  transform: scale(0.98);
}

.min-w-0 { min-width: 0; }

.live-strip {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.live-dot {
  width: 7px;
  height: 7px;
  background: #43A047;
  border-radius: 50%;
  animation: pulse 2s infinite;
  display: inline-block;
  flex-shrink: 0;
}

@keyframes pulse {
  0%   { box-shadow: 0 0 0 0 rgba(67, 160, 71, 0.6); }
  70%  { box-shadow: 0 0 0 7px rgba(67, 160, 71, 0); }
  100% { box-shadow: 0 0 0 0 rgba(67, 160, 71, 0); }
}

/* ── Area quick links ── */
.section-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: rgba(var(--v-theme-on-surface), 0.45);
  padding-left: 4px;
}

.area-card {
  cursor: pointer;
  transition: background 0.15s;
}

.area-card:active {
  opacity: 0.8;
}
</style>
