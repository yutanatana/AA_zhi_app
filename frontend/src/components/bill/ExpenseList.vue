
<template>
  <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">立替リスト</h3>
    <div v-if="expenses?.length > 0" class="space-y-3">
      <div v-for="expense in expenses" :key="expense.id" class="flex justify-between items-start bg-slate-50 dark:bg-slate-700/50 p-4 rounded-lg">
        <div class="text-sm">
          <p class="font-bold text-base">{{ expense.description }} - {{ formatCurrency(expense.amount) }}</p>
          <p class="text-slate-600 dark:text-slate-400">
            <span class="font-medium">{{ expense.payer.name }}</span> が支払い
          </p>
          <p class="text-slate-600 dark:text-slate-400 text-xs">
            対象: {{ expense.beneficiaries.map(b => b.name).join(', ') }}
          </p>
        </div>
        <button @click="$emit('delete-expense', expense.id)" class="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-100 dark:hover:bg-red-900/50 transition flex-shrink-0 ml-2" title="削除">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    <p v-else class="text-slate-500 dark:text-slate-400">まだ立替がありません。</p>
  </section>
</template>

<script setup>
defineProps({
  expenses: {
    type: Array,
    default: () => []
  }
});
defineEmits(['delete-expense']);

const formatCurrency = (value) => {
  if (typeof value !== 'number') return '';
  return new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(value);
};
</script>
