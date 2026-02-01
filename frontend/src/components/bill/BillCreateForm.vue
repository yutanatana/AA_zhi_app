
<template>
  <div class="max-w-md mx-auto bg-white dark:bg-slate-800 shadow-lg rounded-xl p-8">
    <h2 class="text-2xl font-semibold mb-6 text-center">新しい割り勘を作成</h2>
    <form @submit.prevent="submit" class="space-y-6">
      <div>
        <label for="description" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">名目 (例: 旅行、飲み会)</label>
        <input id="description" v-model="description" type="text" required placeholder="名目を入力" class="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" />
      </div>
      <button type="submit" :disabled="submitting" class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-slate-800 transition-colors">
        {{ submitting ? '作成中...' : '作成する' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  submitting: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['create-bill']);

const description = ref('');

const submit = () => {
  if (description.value.trim()) {
    emit('create-bill', description.value);
  }
};
</script>
