
<template>
  <div class="bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 min-h-screen font-sans">
    <AppHeader :bill-id="billId" :bill-description="billData?.description" />
    <main class="container mx-auto p-4 md:p-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { RouterView } from 'vue-router';
import AppHeader from '@/components/common/AppHeader.vue';
import { useBill } from '@/composables/useBill';

const route = useRoute();
const { billData } = useBill();

const billId = computed(() => route.params.id || null);

</script>
