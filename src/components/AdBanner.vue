<template>
  <!--
    Fixed bottom banner ad — sits above the 60px bottom nav.
    pointer-events:none on wrapper so underlying content is never blocked.

    SETUP: Replace placeholder values with your real AdSense credentials.
    Get them at https://adsense.google.com → Ads → By ad unit → Display ads
    Or set env vars VITE_ADSENSE_CLIENT and VITE_ADSENSE_SLOT in .env.local
  -->
  <div class="ad-positioner" aria-hidden="true">
    <div class="ad-banner">
      <ins
        class="adsbygoogle"
        style="display:block"
        :data-ad-client="adClient"
        :data-ad-slot="adSlot"
        data-ad-format="banner"
        data-full-width-responsive="true"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

// Publisher ID  → AdSense → Account → Account information → Publisher ID
const adClient = import.meta.env.VITE_ADSENSE_CLIENT || 'ca-pub-XXXXXXXXXXXXXXXX'
// Ad Slot ID   → AdSense → Ads → By ad unit → (your Display ad unit) → Slot ID
const adSlot   = import.meta.env.VITE_ADSENSE_SLOT   || '0000000000'

onMounted(() => {
  try {
    ;(window.adsbygoogle = window.adsbygoogle || []).push({})
  } catch {
    // Expected in dev or when blocked by an ad blocker — safe to ignore
  }
})
</script>

<style scoped>
/* Wrapper — pointer-events:none so it NEVER blocks any app touch or click */
.ad-positioner {
  position: fixed;
  bottom: 60px; /* exactly above the 60px bottom nav */
  left: 0;
  right: 0;
  z-index: 100;
  pointer-events: none;
}

/* Banner slot — re-enable pointer events for ad interactions only */
.ad-banner {
  pointer-events: auto;
  height: 50px; /* IAB mobile banner standard */
  overflow: hidden;
  background: transparent;
}

/* Make sure AdSense fills the slot fully */
:deep(.adsbygoogle) {
  display: block !important;
  width: 100% !important;
  height: 50px !important;
}
</style>
