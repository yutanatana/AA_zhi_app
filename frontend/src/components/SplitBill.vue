<template>
  <div class="bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 min-h-screen font-sans flex flex-col items-center justify-center p-4">
    <div class="w-full max-w-md">
      <h1 class="text-4xl font-bold text-center mb-2 text-slate-900 dark:text-white">割り勘アプリ</h1>
      <p class="text-center text-slate-600 dark:text-slate-400 mb-8">(MVP)</p>

      <!-- Loading State -->
      <div v-if="loading" class="text-center p-8">
        <svg class="animate-spin h-8 w-8 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="mt-2">Loading...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-6" role="alert">
        <strong class="font-bold">エラー:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <!-- Create Bill Form (Home) -->
      <div v-if="!billId && !loading" class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-semibold mb-6 text-center">新しい割り勘を作成</h2>
        <form @submit.prevent="createBill" class="space-y-6">
          <div>
            <label for="description" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">名目 (例: 飲み会)</label>
            <input id="description" v-model="newBill.description" type="text" required placeholder="名目を入力"
                   class="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" />
          </div>
          <div>
            <label for="amount" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">合計金額 (円)</label>
            <input id="amount" v-model.number="newBill.total_amount" type="number" required placeholder="金額を入力"
                   class="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" />
          </div>
          <button type="submit"
                  class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-slate-800 transition-colors">
            URLを発行する
          </button>
        </form>
      </div>

      <!-- Bill Details (Shared View) -->
      <div v-if="billId && billData" class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-8 space-y-6">
        <h2 class="text-2xl font-semibold mb-4 text-center">割り勘詳細</h2>
        <div class="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-6 text-left space-y-3">
          <p><strong>名目:</strong> <span class="text-lg">{{ billData.description }}</span></p>
          <p><strong>合計金額:</strong> <span class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ formatCurrency(billData.total_amount) }}</span></p>
        </div>

        <div class="share-section space-y-2">
          <p class="font-medium text-center">このページを共有してください:</p>
          <div class="flex gap-2">
            <input type="text" readonly :value="currentUrl" class="flex-grow px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-50 dark:bg-slate-700 outline-none"/>
            <button @click="copyUrl" class="bg-slate-200 hover:bg-slate-300 dark:bg-slate-600 dark:hover:bg-slate-500 text-slate-800 dark:text-slate-200 font-bold py-2 px-4 rounded-lg transition-colors">
              コピー
            </button>
          </div>
        </div>

        <button @click="goHome" class="w-full bg-slate-500 hover:bg-slate-600 text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 dark:focus:ring-offset-slate-800 transition-colors">
          新しく作成する
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

// API Base URL
const API_URL = 'http://localhost:8000';

const billId = ref(route.params.id || null);
const billData = ref(null);
const loading = ref(false);
const error = ref(null);

const newBill = ref({
  description: '',
  total_amount: null
});

const currentUrl = computed(() => window.location.href);

const formatCurrency = (value) => {
  if (typeof value !== 'number') return '';
  return new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(value);
};

const fetchBill = async (id) => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`${API_URL}/bills/${id}`);
    billData.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "割り勘情報の取得に失敗しました。URLが正しいか確認してください。";
  } finally {
    loading.value = false;
  }
};

const createBill = async () => {
  if (!newBill.value.description || !newBill.value.total_amount) {
    error.value = "名目と合計金額を入力してください。";
    return;
  }
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.post(`${API_URL}/bills`, newBill.value);
    const createdId = response.data.id;
    router.push(`/${createdId}`);
  } catch (err) {
    console.error(err);
    error.value = "作成に失敗しました。サーバーが起動しているか確認してください。";
  } finally {
    loading.value = false;
  }
};

const copyUrl = () => {
  navigator.clipboard.writeText(currentUrl.value).then(() => {
    alert('URLをコピーしました！');
  }).catch(err => {
    console.error('Copy failed', err);
    alert('コピーに失敗しました。');
  });
};

const goHome = () => {
  router.push('/');
};

// Watch for route changes to handle navigation
watch(() => route.params.id, (newId) => {
  billId.value = newId;
  error.value = null; // Clear errors on navigation
  if (newId) {
    fetchBill(newId);
  } else {
    // Reset state for the creation form
    billData.value = null;
    newBill.value = { description: '', total_amount: null };
  }
});

onMounted(() => {
  if (billId.value) {
    fetchBill(billId.value);
  }
});
</script>

<style scoped>
/* Scoped styles are no longer needed as we are using Tailwind utilities */
</style>