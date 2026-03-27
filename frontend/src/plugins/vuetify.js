import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

const mumbraTheme = {
  dark: false,
  colors: {
    // Primary teal — trust, healthcare, calm
    primary: '#00695C',
    'primary-darken-1': '#004D40',
    secondary: '#0288D1',
    'secondary-darken-1': '#0277BD',
    // Status colours
    available: '#43A047',
    low: '#FB8C00',
    full: '#E53935',
    whatsapp: '#25D366',
    background: '#F8FAFA',
    surface: '#FFFFFF',
    error: '#E53935',
    warning: '#FB8C00',
    info: '#0288D1',
    success: '#43A047',
  },
}

const mumbraDarkTheme = {
  dark: true,
  colors: {
    primary: '#4DB6AC',
    'primary-darken-1': '#00897B',
    secondary: '#4FC3F7',
    available: '#66BB6A',
    low: '#FFA726',
    full: '#EF5350',
    whatsapp: '#25D366',
    background: '#121212',
    surface: '#1E1E1E',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'mumbra',
    themes: {
      mumbra: mumbraTheme,
      mumbraDark: mumbraDarkTheme,
    },
  },
  defaults: {
    VBtn: { rounded: 'lg', elevation: 0 },
    VCard: { rounded: 'xl', elevation: 2 },
    VChip: { rounded: 'lg' },
    VTextField: { variant: 'outlined', density: 'comfortable', rounded: 'lg' },
    VSelect: { variant: 'outlined', density: 'comfortable', rounded: 'lg' },
  },
})
