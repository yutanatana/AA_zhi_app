
<template>
  <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">精算結果</h3>
    <div v-if="settlement.length > 0" class="space-y-4">
      <div v-for="(trans, index) in settlement" :key="index" class="flex items-center justify-between bg-slate-100 dark:bg-slate-700 p-4 rounded-lg">
        <span class="font-medium text-slate-800 dark:text-slate-200">{{ trans.from_member_name }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
        <span class="font-medium text-slate-800 dark:text-slate-200">{{ trans.to_member_name }}</span>
        <span class="font-bold text-lg text-blue-600 dark:text-blue-400">{{ formatCurrency(trans.amount) }}</span>
      </div>
    </div>
    <p v-else-if="!hasExpenses" class="text-slate-500 dark:text-slate-400">立替が追加されると、ここに精算結果が自動で表示されます。</p>
    <p v-else class="text-center text-slate-600 dark:text-slate-400">精算は不要です。全員の貸し借りは0です。</p>
  </section>
</template>

<script setup>
defineProps({
  settlement: {
    type: Array,
    default: () => []
  },
  hasExpenses: {
    type: Boolean,
    default: false
  }
});

const formatCurrency = (value) => {
  if (typeof value !== 'number') return '';
  return new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(value);
};
</script>
