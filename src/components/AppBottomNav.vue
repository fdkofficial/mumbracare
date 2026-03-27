<template>
  <v-bottom-navigation
    v-model="activeTab"
    color="primary"
    grow
    elevation="8"
    height="60"
  >
    <v-btn value="home" :to="{ name: 'home' }" aria-label="Home" class="nav-btn">
      <v-icon size="22">mdi-home-heart</v-icon>
      <span class="nav-label">{{ $t('nav.home') }}</span>
    </v-btn>

    <v-btn value="beds" :to="{ name: 'beds' }" aria-label="Beds" class="nav-btn">
      <v-icon size="22">mdi-bed-king-outline</v-icon>
      <span class="nav-label">{{ $t('nav.beds') }}</span>
    </v-btn>

    <v-btn value="doctors" :to="{ name: 'doctors' }" aria-label="Doctors" class="nav-btn">
      <v-icon size="22">mdi-doctor</v-icon>
      <span class="nav-label">{{ $t('nav.doctors') }}</span>
    </v-btn>

    <v-btn value="pharmacies" :to="{ name: 'pharmacies' }" aria-label="Pharmacy" class="nav-btn">
      <v-icon size="22">mdi-plus</v-icon>
      <span class="nav-label">{{ $t('nav.pharmacies') }}</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const appStore = useAppStore()
const activeTab = ref(route.name)

watch(() => route.name, (name) => { activeTab.value = name })
</script>

<style scoped>
.nav-btn {
  min-width: 0 !important;
  flex-direction: column;
  gap: 2px;
}
.nav-label {
  font-size: 0.65rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  letter-spacing: 0.1px;
}
</style>
