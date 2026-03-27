<template>
  <v-card rounded="xl" elevation="2" class="doctor-card">
    <v-card-text class="pa-4">
      <div class="d-flex align-start gap-3">
        <!-- Specialty avatar -->
        <v-avatar :color="specialtyColor" size="52" class="flex-shrink-0 mt-1">
          <v-icon :icon="specialtyIcon" size="26" color="white" />
        </v-avatar>

        <!-- Content -->
        <div class="flex-grow-1 min-w-0">
          <div class="d-flex align-center justify-space-between gap-2">
            <div class="text-subtitle-1 font-weight-bold text-truncate">
              Dr. {{ doctor.name }}
            </div>
            <!-- Availability badge -->
            <v-chip
              :color="doctor.is_available ? 'available' : 'error'"
              variant="flat"
              size="small"
              class="flex-shrink-0"
            >
              <v-icon start size="14">
                {{ doctor.is_available ? 'mdi-circle' : 'mdi-circle-outline' }}
              </v-icon>
              {{ doctor.is_available ? $t('doctors.in_clinic') : $t('doctors.away') }}
            </v-chip>
          </div>

          <!-- Specialty & location -->
          <div class="d-flex flex-wrap gap-1 mt-1">
            <v-chip size="x-small" :color="specialtyColor" variant="tonal">
              {{ $t(`specialty.${doctor.specialty}`) }}
            </v-chip>
            <v-chip size="x-small" variant="tonal" color="secondary">
              <v-icon start size="12">mdi-map-marker-outline</v-icon>
              {{ doctor.facility_area }}
            </v-chip>
          </div>

          <!-- Facility name -->
          <div class="text-caption text-medium-emphasis mt-1 d-flex align-center">
            <v-icon size="13" class="me-1">mdi-hospital-building</v-icon>
            {{ doctor.facility_name }}
          </div>

          <!-- Facility address -->
          <div v-if="doctor.facility_address" class="text-caption text-medium-emphasis mt-1 d-flex align-center">
            <v-icon size="13" class="me-1">mdi-map-marker-outline</v-icon>
            {{ doctor.facility_address }}
          </div>

          <!-- Timing -->
          <div v-if="timingText" class="text-caption text-medium-emphasis mt-1 d-flex align-center">
            <v-icon size="13" class="me-1">mdi-clock-time-four-outline</v-icon>
            {{ timingText }}
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="d-flex gap-2 mt-3 pt-1">
        <v-btn
          v-if="doctor.contact_number"
          :href="`tel:${doctor.contact_number}`"
          color="primary"
          variant="tonal"
          size="small"
          rounded="lg"
          prepend-icon="mdi-phone"
          class="flex-grow-1"
        >
          {{ $t('doctors.call') }}
        </v-btn>
        <v-btn
          v-if="doctor.contact_number"
          :href="whatsAppLink"
          target="_blank"
          rel="noopener noreferrer"
          color="whatsapp"
          variant="tonal"
          size="small"
          rounded="lg"
          icon="mdi-whatsapp"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  doctor: { type: Object, required: true },
})

const SPECIALTY_META = {
  CARDIAC:   { color: '#E53935', icon: 'mdi-heart-pulse' },
  PEDIATRIC: { color: '#7B1FA2', icon: 'mdi-baby-face-outline' },
  GENERAL:   { color: '#0288D1', icon: 'mdi-stethoscope' },
  GYNAE:     { color: '#D81B60', icon: 'mdi-human-female' },
  ORTHO:     { color: '#F57C00', icon: 'mdi-bone' },
  DERM:      { color: '#388E3C', icon: 'mdi-weather-sunny' },
  ENT:       { color: '#00838F', icon: 'mdi-ear-hearing' },
}

const specialtyColor = computed(() => SPECIALTY_META[props.doctor.specialty]?.color ?? '#546E7A')
const specialtyIcon = computed(() => SPECIALTY_META[props.doctor.specialty]?.icon ?? 'mdi-doctor')

const timingText = computed(() => {
  const slots = props.doctor.timing_slots
  if (!slots || !Object.keys(slots).length) return ''
  return Object.entries(slots)
    .map(([k, v]) => `${k}: ${v}`)
    .join(' | ')
})

const whatsAppLink = computed(() => {
  if (!props.doctor.contact_number) return '#'
  const msg = encodeURIComponent(`Hello Dr. ${props.doctor.name}, I would like to enquire about an appointment.`)
  return `https://wa.me/${props.doctor.contact_number.replace(/\D/g, '')}?text=${msg}`
})
</script>

<style scoped>
.doctor-card {
  transition: transform 0.15s ease;
}
.doctor-card:active {
  transform: scale(0.98);
}
.min-w-0 { min-width: 0; }
</style>
