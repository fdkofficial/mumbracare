<template>
  <!-- Bed status card with traffic-light colour system -->
  <v-card :color="cardBackground" rounded="xl" elevation="3" class="bed-card" @click="$emit('click')">
    <!-- Status banner -->
    <div :class="['status-banner', statusClass]">
      <v-icon size="16" class="me-1">{{ statusIcon }}</v-icon>
      <span class="text-caption font-weight-bold text-uppercase">{{ statusLabel }}</span>
    </div>

    <v-card-text class="pa-4 pb-3">
      <!-- Header row -->
      <div class="d-flex align-start justify-space-between mb-3">
        <div class="flex-grow-1 me-2">
          <div class="text-subtitle-1 font-weight-bold text-high-emphasis line-clamp-2">
            {{ facility.name }}
          </div>
          <div class="d-flex align-center gap-1 mt-1">
            <v-chip size="x-small" :color="typeColor" variant="tonal">
              <v-icon start size="12">{{ typeIcon }}</v-icon>
              {{ $t(`common.${facility.facility_type?.toLowerCase()}`) }}
            </v-chip>
            <v-chip size="x-small" variant="tonal" color="secondary">
              {{ facility.area_display }}
            </v-chip>
            <v-chip v-if="facility.is_verified" size="x-small" color="success" variant="tonal">
              <v-icon start size="12">mdi-check-decagram</v-icon>
              {{ $t('common.verified') }}
            </v-chip>
          </div>
          <!-- Facility address -->
          <div v-if="facility.address" class="text-caption text-medium-emphasis mt-1 d-flex align-center">
            <v-icon size="12" class="me-1">mdi-map-marker-outline</v-icon>
            <span class="line-clamp-1">{{ facility.address }}</span>
          </div>
        </div>

        <!-- Big bed count bubble -->
        <div :class="['bed-bubble', `bubble--${statusClass}`]">
          <span class="bubble-count">{{ bedStatus?.available_beds ?? '?' }}</span>
          <span class="bubble-label">{{ $t('beds.available') }}</span>
        </div>
      </div>

      <!-- Bed progress bar -->
      <div v-if="bedStatus" class="mb-3">
        <div class="d-flex justify-space-between text-caption text-medium-emphasis mb-1">
          <span>{{ $t('beds.general') }}</span>
          <span>{{ bedStatus.available_beds }} / {{ bedStatus.total_beds }}</span>
        </div>
        <v-progress-linear
          :model-value="generalPct"
          :color="statusClass === 'status--available' ? 'available' : statusClass === 'status--low' ? 'warning' : 'full'"
          height="8"
          rounded
          bg-color="grey-lighten-3"
        />
      </div>

      <!-- ICU row (if applicable) -->
      <div v-if="bedStatus && bedStatus.icu_total > 0" class="mb-3">
        <div class="d-flex justify-space-between text-caption text-medium-emphasis mb-1">
          <span>
            <v-icon size="14" class="me-1">mdi-heart-pulse</v-icon>{{ $t('beds.icu') }}
          </span>
          <span>{{ bedStatus.icu_available }} / {{ bedStatus.icu_total }}</span>
        </div>
        <v-progress-linear
          :model-value="icuPct"
          :color="bedStatus.icu_available > 0 ? 'available' : 'full'"
          height="8"
          rounded
          bg-color="grey-lighten-3"
        />
      </div>

      <!-- Footer: updated time + call button -->
      <div class="d-flex align-center justify-space-between">
        <div class="text-caption text-medium-emphasis">
          <v-icon size="13" class="me-1">mdi-clock-outline</v-icon>
          <span v-if="bedStatus">{{ $t('beds.last_updated') }}: {{ timeAgo }}</span>
          <span v-else>{{ $t('beds.no_data') }}</span>
        </div>
        <v-btn
          v-if="facility.contact_number"
          :href="`tel:${facility.contact_number}`"
          color="primary"
          variant="tonal"
          size="small"
          rounded="lg"
          prepend-icon="mdi-phone"
          @click.stop
        >
          Call
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  facility: { type: Object, required: true },
})
defineEmits(['click'])

const bedStatus = computed(() => props.facility.bed_status)

const generalPct = computed(() => {
  if (!bedStatus.value || !bedStatus.value.total_beds) return 0
  return (bedStatus.value.available_beds / bedStatus.value.total_beds) * 100
})

const icuPct = computed(() => {
  if (!bedStatus.value || !bedStatus.value.icu_total) return 0
  return (bedStatus.value.icu_available / bedStatus.value.icu_total) * 100
})

const statusClass = computed(() => {
  if (!bedStatus.value) return 'status--unknown'
  const { available_beds, total_beds } = bedStatus.value
  if (available_beds === 0) return 'status--full'
  if (available_beds / total_beds <= 0.2) return 'status--low'
  return 'status--available'
})

const statusIcon = computed(() => ({
  'status--available': 'mdi-check-circle',
  'status--low': 'mdi-alert-circle',
  'status--full': 'mdi-close-circle',
  'status--unknown': 'mdi-help-circle',
}[statusClass.value]))

const statusLabel = computed(() => ({
  'status--available': t('beds.available'),
  'status--low': t('beds.low'),
  'status--full': t('beds.full'),
  'status--unknown': '—',
}[statusClass.value]))

const cardBackground = computed(() => ({
  'status--available': 'rgba(67,160,71,0.05)',
  'status--low': 'rgba(251,140,0,0.05)',
  'status--full': 'rgba(229,57,53,0.05)',
  'status--unknown': undefined,
}[statusClass.value]))

const typeIcon = computed(() =>
  props.facility.facility_type === 'HOSPITAL' ? 'mdi-hospital-building' : 'mdi-medical-bag',
)
const typeColor = computed(() =>
  props.facility.facility_type === 'HOSPITAL' ? 'primary' : 'secondary',
)

const timeAgo = computed(() => {
  if (!bedStatus.value?.last_updated) return ''
  const diff = Math.floor((Date.now() - new Date(bedStatus.value.last_updated)) / 60000)
  if (diff < 1) return 'Just now'
  if (diff < 60) return `${diff}m ago`
  return `${Math.floor(diff / 60)}h ago`
})
</script>

<style scoped>
.bed-card {
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  overflow: hidden;
}
.bed-card:active {
  transform: scale(0.98);
}

.status-banner {
  display: flex;
  align-items: center;
  padding: 5px 16px;
  font-size: 0.7rem;
  letter-spacing: 0.3px;
}
.status--available { background: rgba(67, 160, 71, 0.15); color: #2E7D32; }
.status--low       { background: rgba(251, 140, 0, 0.15);  color: #E65100; }
.status--full      { background: rgba(229, 57, 53, 0.15);  color: #B71C1C; }
.status--unknown   { background: rgba(0,0,0,0.06);          color: #666;   }

.bed-bubble {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  flex-shrink: 0;
}
.bubble--status--available { background: rgba(67, 160, 71, 0.15); }
.bubble--status--low       { background: rgba(251, 140, 0, 0.15); }
.bubble--status--full      { background: rgba(229, 57, 53, 0.15); }
.bubble--status--unknown   { background: rgba(0,0,0,0.06); }

.bubble-count {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}
.bubble-label {
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.7;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
