<template>
  <div class="bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 min-h-screen font-sans">
    <header class="bg-white dark:bg-slate-800 shadow-md">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 @click="goHome" class="text-2xl font-bold text-slate-900 dark:text-white cursor-pointer">割り勘.com</h1>
        <div class="flex items-center gap-4">
           <p v-if="billData" class="text-sm text-slate-600 dark:text-slate-400 hidden sm:block">
            <strong>名目:</strong> {{ billData.description }}
          </p>
          <button v-if="billId" @click="copyUrl" title="Share URL" class="p-2 rounded-full bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" /></svg>
          </button>
        </div>
      </div>
    </header>

    <main class="container mx-auto p-4 md:p-8">
      <!-- Loading State -->
      <div v-if="loading" class="text-center p-8">
        <svg class="animate-spin h-8 w-8 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <p class="mt-2 text-slate-600 dark:text-slate-400">Loading...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-6" role="alert">
        <strong class="font-bold">エラー:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <!-- Create Bill Form (Home) -->
      <div v-if="!billId && !loading" class="max-w-md mx-auto bg-white dark:bg-slate-800 shadow-lg rounded-xl p-8">
        <h2 class="text-2xl font-semibold mb-6 text-center">新しい割り勘を作成</h2>
        <form @submit.prevent="createBill" class="space-y-6">
          <div>
            <label for="description" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">名目 (例: 旅行、飲み会)</label>
            <input id="description" v-model="newBill.description" type="text" required placeholder="名目を入力" class="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" />
          </div>
          <button type="submit" :disabled="submitting || loading" class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-slate-800 transition-colors">
            {{ (submitting || loading) ? '作成中...' : '作成する' }}
          </button>
        </form>
      </div>

      <!-- Bill Details View -->
      <div v-if="billId && billData && !loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Left Column: Members & Expenses -->
        <div class="space-y-8">
          <!-- Members -->
          <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
            <h3 class="text-xl font-semibold mb-4">メンバー</h3>
            <ul v-if="billData.members?.length > 0" class="space-y-2 mb-4">
              <li v-for="member in billData.members" :key="member.id" class="flex justify-between items-center bg-slate-50 dark:bg-slate-700/50 p-3 rounded-lg">
                <span class="font-medium">{{ member.name }}</span>
              </li>
            </ul>
             <p v-else class="text-slate-500 dark:text-slate-400 text-sm mb-4">まだメンバーがいません。</p>
            <form @submit.prevent="addMember" class="flex gap-2">
              <input v-model="newMemberName" type="text" placeholder="新しいメンバー名" required class="flex-grow px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 outline-none"/>
              <button type="submit" :disabled="submitting" class="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-bold py-2 px-4 rounded-lg transition-colors">
                {{ submitting ? '追加中' : '追加' }}
              </button>
            </form>
          </section>

          <!-- Add Expense -->
          <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
            <h3 class="text-xl font-semibold mb-4">立替の追加</h3>
            <form @submit.prevent="addExpense" class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-1">内容</label>
                <input v-model="newExpense.description" type="text" required placeholder="例: 夕食代" class="w-full input"/>
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">金額</label>
                <input v-model.number="newExpense.amount" type="number" required placeholder="例: 8000" class="w-full input"/>
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">支払った人</label>
                <select v-model="newExpense.payer_id" required class="w-full input">
                  <option disabled value="">選択してください</option>
                  <option v-for="member in billData.members" :key="member.id" :value="member.id">{{ member.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">対象者 (複数選択可)</label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
                   <div>
                      <input type="checkbox" id="select-all" @change="toggleSelectAllBeneficiaries" class="mr-2"/>
                      <label for="select-all">全員</label>
                  </div>
                  <div v-for="member in billData.members" :key="member.id">
                    <input type="checkbox" :id="'mem-'+member.id" :value="member.id" v-model="newExpense.beneficiary_ids" class="mr-2"/>
                    <label :for="'mem-'+member.id">{{ member.name }}</label>
                  </div>
                </div>
              </div>
              <button type="submit" :disabled="submitting" class="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg transition-colors">
                {{ submitting ? '追加中...' : '立替を追加' }}
              </button>
            </form>
          </section>
        </div>

        <!-- Right Column: Expense List & Settle -->
        <div class="space-y-8">
           <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
              <h3 class="text-xl font-semibold mb-4">立替リスト</h3>
              <div v-if="billData.expenses?.length > 0" class="space-y-3">
                <div v-for="expense in billData.expenses" :key="expense.id" class="bg-slate-50 dark:bg-slate-700/50 p-4 rounded-lg text-sm">
                  <p class="font-bold text-base">{{ expense.description }} - {{ formatCurrency(expense.amount) }}</p>
                  <p class="text-slate-600 dark:text-slate-400">
                    <span class="font-medium">{{ expense.payer.name }}</span> が支払い
                  </p>
                   <p class="text-slate-600 dark:text-slate-400 text-xs">
                    対象: {{ expense.beneficiaries.map(b => b.name).join(', ') }}
                  </p>
                </div>
              </div>
              <p v-else class="text-slate-500 dark:text-slate-400">まだ立替がありません。</p>
           </section>
           <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
              <h3 class="text-xl font-semibold mb-4">精算</h3>
              <p class="text-slate-600 dark:text-slate-400 mb-4">全てのメンバーと立替を登録したら、下のボタンを押して精算を開始してください。</p>
              <button @click="settleBill" class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg transition-colors">精算する</button>
           </section>
        </div>
      </div>
    </main>
    
    <!-- Settlement Modal -->
    <div v-if="showSettlement" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
        <div class="bg-white dark:bg-slate-800 rounded-xl shadow-2xl p-8 max-w-lg w-full">
            <h2 class="text-2xl font-bold text-center mb-6">精算結果</h2>
            <div v-if="settlement.length > 0" class="space-y-4">
                <div v-for="(trans, index) in settlement" :key="index" class="flex items-center justify-between bg-slate-100 dark:bg-slate-700 p-4 rounded-lg">
                    <span class="font-medium text-slate-800 dark:text-slate-200">{{ trans.from_member_name }}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                    <span class="font-medium text-slate-800 dark:text-slate-200">{{ trans.to_member_name }}</span>
                    <span class="font-bold text-lg text-blue-600 dark:text-blue-400">{{ formatCurrency(trans.amount) }}</span>
                </div>
            </div>
            <p v-else class="text-center text-slate-600 dark:text-slate-400">精算は不要です。全員の貸し借りは0です。</p>
            <button @click="showSettlement = false" class="w-full mt-8 bg-slate-500 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg">閉じる</button>
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
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const billId = ref(route.params.id || null);
const billData = ref(null);
const loading = ref(false);
const submitting = ref(false);
const error = ref(null);

const newBill = ref({ description: '' });
const newMemberName = ref('');
const newExpense = ref({
  description: '',
  amount: null,
  payer_id: '',
  beneficiary_ids: []
});
const settlement = ref([]);
const showSettlement = ref(false);

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
    handleApiError(err, "割り勘情報の取得に失敗しました。");
  } finally {
    loading.value = false;
  }
};

const createBill = async () => {
  if (submitting.value) return;
  submitting.value = true;
  error.value = null;
  try {
    const response = await axios.post(`${API_URL}/bills`, newBill.value);
    router.push(`/${response.data.id}`);
  } catch (err) {
    handleApiError(err, "作成に失敗しました。");
  } finally {
    submitting.value = false;
  }
};

const addMember = async () => {
  if (!newMemberName.value.trim() || submitting.value) return;
  submitting.value = true;
  error.value = null;
  try {
    await axios.post(`${API_URL}/bills/${billId.value}/members`, { name: newMemberName.value });
    newMemberName.value = '';
    await fetchBill(billId.value); // Refresh data
  } catch (err) {
    handleApiError(err, "メンバーの追加に失敗しました。");
  } finally {
    submitting.value = false;
  }
};

const addExpense = async () => {
  if (newExpense.value.beneficiary_ids.length === 0 || submitting.value) {
      if (!submitting.value) error.value = "対象者を1人以上選択してください。";
      return;
  }
  submitting.value = true;
  error.value = null;
  try {
    await axios.post(`${API_URL}/bills/${billId.value}/expenses`, newExpense.value);
    newExpense.value = { description: '', amount: null, payer_id: '', beneficiary_ids: [] };
    await fetchBill(billId.value); // Refresh data
  } catch (err) {
    handleApiError(err, "立替の追加に失敗しました。");
  } finally {
    submitting.value = false;
  }
};

const settleBill = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`${API_URL}/bills/${billId.value}/settle`);
    settlement.value = response.data;
    showSettlement.value = true;
  } catch (err) {
    handleApiError(err, "精算に失敗しました。");
  } finally {
    loading.value = false;
  }
};

const toggleSelectAllBeneficiaries = (event) => {
    if (event.target.checked) {
        newExpense.value.beneficiary_ids = billData.value.members.map(m => m.id);
    } else {
        newExpense.value.beneficiary_ids = [];
    }
}

const handleApiError = (err, defaultMessage) => {
  if (err.response && err.response.data && err.response.data.detail) {
    error.value = err.response.data.detail;
  } else {
    error.value = defaultMessage;
  }
  console.error(err);
};

const copyUrl = () => {
  navigator.clipboard.writeText(currentUrl.value).then(() => alert('URLをコピーしました！'));
};

const goHome = () => {
  router.push('/');
};

watch(() => route.params.id, (newId) => {
  billId.value = newId;
  error.value = null;
  billData.value = null; // Reset data to prevent showing old state
  if (newId) {
    fetchBill(newId);
  }
}, { immediate: true });

</script>

