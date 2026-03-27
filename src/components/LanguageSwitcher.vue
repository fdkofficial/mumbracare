<template>
  <v-menu location="bottom end">
    <template #activator="{ props }">
      <v-btn v-bind="props" variant="text" :icon="false" rounded="lg" size="small">
        <span class="text-body-2 font-weight-medium me-1">{{ currentFlag }}</span>
        <v-icon size="18">mdi-translate</v-icon>
      </v-btn>
    </template>

    <v-list density="compact" rounded="xl" min-width="160" elevation="8">
      <v-list-item
        v-for="lang in languages"
        :key="lang.code"
        :value="lang.code"
        :active="appStore.locale === lang.code"
        active-color="primary"
        rounded="lg"
        @click="selectLanguage(lang.code)"
      >
        <template #prepend>
          <!-- <span class="me-2 text-body-1">{{ lang.flag }}</span> -->
        </template>
        <v-list-item-title class="text-body-2">{{ lang.label }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'

const { locale } = useI18n()
const appStore = useAppStore()

const languages = [
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'hi', label: 'हिंदी', flag: '🇮🇳' },
  { code: 'ur', label: 'اردو', flag: 'UR' },
]

const currentFlag = computed(() => languages.find(l => l.code === appStore.locale)?.flag ?? '🌐')

function selectLanguage(code) {
  appStore.setLocale(code)
  locale.value = code
}
</script>
