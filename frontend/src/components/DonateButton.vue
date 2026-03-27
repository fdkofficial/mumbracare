<template>
  <!-- Floating heart button -->
  <v-btn
    icon
    size="40"
    class="donate-fab"
    color="error"
    elevation="4"
    @click="open = true"
    aria-label="Support Us"
  >
    <v-icon size="20">mdi-heart</v-icon>
  </v-btn>

  <!-- Donation dialog -->
  <v-dialog v-model="open" max-width="340" :scrim-opacity="0.55">
    <v-card rounded="xl" class="donate-card pa-1">
      <!-- Close button -->
      <v-btn
        icon size="small" variant="text" color="medium-emphasis"
        class="donate-close"
        @click="open = false"
      >
        <v-icon size="18">mdi-close</v-icon>
      </v-btn>

      <v-card-text class="text-center pa-4">
        <!-- Heart animation -->
        <div class="heart-pulse mb-2">
          <v-icon size="40" color="error">mdi-heart</v-icon>
        </div>

        <div class="text-h6 font-weight-bold mb-1">Thank You! 🙏</div>
        <div class="text-body-2 text-medium-emphasis mb-4">
          Your support keeps Mumbra Care free for the community.
        </div>

        <!-- QR Code -->
        <div v-if="loading" class="py-6">
          <v-progress-circular indeterminate color="primary" />
        </div>

        <template v-else-if="settings?.paytm_qr_image">
          <v-card rounded="xl" elevation="0" color="grey-lighten-4" class="qr-wrap mx-auto mb-3 pa-3">
            <img :src="settings.paytm_qr_image" class="qr-img" alt="Paytm QR Code" />
          </v-card>
          <div class="text-subtitle-2 font-weight-bold">{{ settings.donate_name }}</div>
          <div v-if="settings.donate_upi_id" class="text-caption text-medium-emphasis mt-1">
            <v-icon size="13">mdi-contactless-payment</v-icon>
            {{ settings.donate_upi_id }}
          </div>
          <div class="text-caption text-medium-emphasis mt-2">Scan with any UPI app · Paytm · GPay · PhonePe</div>
        </template>

        <template v-else-if="!loading">
          <v-icon size="60" color="grey-lighten-1" class="mb-3">mdi-qrcode</v-icon>
          <div class="text-body-2 text-medium-emphasis">
            QR code coming soon. Thank you for your love! ❤️
          </div>
        </template>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSiteSettings } from '@/api/index.js'

const open = ref(false)
const settings = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    settings.value = await getSiteSettings()
  } catch {
    // Non-critical — dialog still opens, shows fallback message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.donate-fab {
  position: fixed;
  /* Above ad banner (36px) which sits above nav (60px) = 104px + 8px gap */
  bottom: 104px;
  right: 14px;
  z-index: 101;
}

.donate-card {
  position: relative;
}

.donate-close {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 1;
}

.heart-pulse {
  animation: pulse 1.6s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.15); }
}

.qr-wrap {
  max-width: 200px;
}

.qr-img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  display: block;
}
</style>
