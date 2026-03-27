<template>
  <v-app :theme="appStore.darkMode ? 'mumbraDark' : 'mumbra'" :dir="appStore.isRTL ? 'rtl' : 'ltr'">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <AppBottomNav v-if="showNav" />
    <AdBanner v-if="showNav" />
    <DonateButton v-if="showNav" />
  </v-app>
</template>

<script setup>
import { watch, computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import AppBottomNav from '@/components/AppBottomNav.vue'
import AdBanner from '@/components/AdBanner.vue'
import DonateButton from '@/components/DonateButton.vue'

const appStore = useAppStore()
const { locale } = useI18n()
const route = useRoute()

const showNav = computed(() => !['login', 'portal'].includes(route.name))

// Sync store locale → i18n locale on startup
locale.value = appStore.locale

watch(() => appStore.locale, (val) => {
  locale.value = val
  // Set HTML lang attribute for accessibility
  document.documentElement.lang = val
  // Set dir for RTL (Urdu)
  document.documentElement.dir = val === 'ur' ? 'rtl' : 'ltr'
})
</script>

<style>
/* Global resets for mobile-first */
*, *::before, *::after { box-sizing: border-box; }
html { overflow-x: hidden; }
body { margin: 0; -webkit-tap-highlight-color: transparent; }

/* Page transition */
.fade-enter-active,
.fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from,
.fade-leave-to   { opacity: 0; }

/* Custom font fallback stack for Devanagari + Arabic */
.v-application {
  font-family: 'Noto Sans', 'Noto Sans Arabic', 'Noto Sans Devanagari', sans-serif !important;
}

/* Urdu RTL adjustments */
[dir="rtl"] .v-app-bar-title { text-align: right; }
[dir="rtl"] .v-icon.mdi-chevron-right { transform: scaleX(-1); }
</style>
