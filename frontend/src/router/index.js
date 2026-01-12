import { createRouter, createWebHistory } from 'vue-router'
import SplitBill from '../components/SplitBill.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SplitBill
    },
    {
      path: '/:id',
      name: 'bill',
      component: SplitBill
    }
  ]
})

export default router
