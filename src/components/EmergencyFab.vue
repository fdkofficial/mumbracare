<template>
  <!-- Floating WhatsApp button — always visible for emergencies -->
  <v-fab
    :style="fabStyle"
    color="whatsapp"
    size="large"
    icon
    :aria-label="$t('whatsapp.fab_label')"
    class="emergency-fab"
    @click="openWhatsApp"
  >
    <v-icon size="32">mdi-whatsapp</v-icon>
    <v-tooltip activator="parent" location="start">
      {{ $t('whatsapp.fab_label') }}
    </v-tooltip>
  </v-fab>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const appStore = useAppStore()

// Community WhatsApp number — replace with real number
const COMMUNITY_WHATSAPP = '919XXXXXXXXX'

const fabStyle = computed(() => ({
  position: 'fixed',
  bottom: '80px',
  right: '16px',
  zIndex: 1000,
}))

function openWhatsApp() {
  const msg = encodeURIComponent(t('whatsapp.default_message'))
  window.open(`https://wa.me/${COMMUNITY_WHATSAPP}?text=${msg}`, '_blank', 'noopener,noreferrer')
}
</script>

<style scoped>
.emergency-fab {
  box-shadow: 0 4px 20px rgba(37, 211, 102, 0.5) !important;
}
</style>
