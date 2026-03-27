<template>
  <v-card rounded="xl" elevation="2" class="pharmacy-card">
    <v-card-text class="pa-4">
      <div class="d-flex align-start gap-3">
        <!-- Icon -->
        <v-avatar color="primary" size="52" class="flex-shrink-0 mt-1">
          <v-icon icon="mdi-pill" size="26" color="white" />
        </v-avatar>

        <!-- Content -->
        <div class="flex-grow-1 min-w-0">
          <div class="d-flex align-center justify-space-between gap-2">
            <div class="text-subtitle-1 font-weight-bold text-truncate">
              {{ pharmacy.name }}
            </div>
            <v-chip
              v-if="pharmacy.is_24_7"
              color="available"
              variant="flat"
              size="small"
              class="flex-shrink-0"
            >
              <v-icon start size="14">mdi-clock-check-outline</v-icon>
              {{ $t('pharmacies.open_24') }}
            </v-chip>
          </div>

          <!-- Area -->
          <div class="d-flex flex-wrap gap-1 mt-1">
            <v-chip size="x-small" variant="tonal" color="secondary">
              <v-icon start size="12">mdi-map-marker-outline</v-icon>
              {{ pharmacy.area_display }}
            </v-chip>
            <v-chip v-if="pharmacy.is_verified" size="x-small" color="success" variant="tonal">
              <v-icon start size="12">mdi-check-decagram</v-icon>
              {{ $t('common.verified') }}
            </v-chip>
          </div>

          <!-- Address -->
          <div class="text-caption text-medium-emphasis mt-1">
            <v-icon size="13" class="me-1">mdi-store-marker-outline</v-icon>
            {{ pharmacy.address }}
          </div>

          <!-- Hours (when not 24/7) -->
          <div v-if="!pharmacy.is_24_7 && hoursText" class="text-caption text-medium-emphasis mt-1">
            <v-icon size="13" class="me-1">mdi-clock-outline</v-icon>
            {{ $t('pharmacies.hours') }}: {{ hoursText }}
          </div>
        </div>
      </div>

      <!-- Call button -->
      <div class="d-flex gap-2 mt-3">
        <v-btn
          v-if="pharmacy.contact_number"
          :href="`tel:${pharmacy.contact_number}`"
          color="primary"
          variant="tonal"
          size="small"
          rounded="lg"
          prepend-icon="mdi-phone"
          class="flex-grow-1"
        >
          {{ $t('pharmacies.call') }}
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pharmacy: { type: Object, required: true },
})

const hoursText = computed(() => {
  const { opening_time, closing_time } = props.pharmacy
  if (!opening_time && !closing_time) return ''
  return `${opening_time ?? '?'} – ${closing_time ?? '?'}`
})
</script>

<style scoped>
.pharmacy-card {
  transition: transform 0.15s ease;
}
.pharmacy-card:active {
  transform: scale(0.98);
}
.min-w-0 { min-width: 0; }
</style>
