import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Home' },
  },
  {
    path: '/beds',
    name: 'beds',
    component: () => import('@/views/BedTrackerView.vue'),
    meta: { title: 'Bed Tracker' },
  },
  {
    path: '/doctors',
    name: 'doctors',
    component: () => import('@/views/DoctorsView.vue'),
    meta: { title: 'Doctors' },
  },
  {
    path: '/pharmacies',
    name: 'pharmacies',
    component: () => import('@/views/PharmaciesView.vue'),
    meta: { title: 'Pharmacies' },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: 'Portal Login', public: true },
  },
  {
    path: '/portal',
    name: 'portal',
    component: () => import('@/views/PortalView.vue'),
    meta: { title: 'Portal', requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// Auth guard — redirect to login if token missing
router.beforeEach((to) => {
  const hasToken = !!localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !hasToken) {
    return { name: 'login' }
  }

  if (to.name === 'login' && hasToken) {
    return { name: 'portal' }
  }
})

export default router
