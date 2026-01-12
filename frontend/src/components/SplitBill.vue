<template>
  <div class="split-bill-container">
    <h1>割り勘アプリ (MVP)</h1>

    <!-- Loading State -->
    <div v-if="loading">Loading...</div>

    <!-- Error State -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Create Bill Form (Home) -->
    <div v-if="!billId && !loading" class="create-bill">
      <h2>新しい割り勘を作成</h2>
      <form @submit.prevent="createBill">
        <div class="form-group">
          <label for="description">名目 (例: 飲み会)</label>
          <input
            id="description"
            v-model="newBill.description"
            type="text"
            required
            placeholder="名目を入力"
          />
        </div>
        <div class="form-group">
          <label for="amount">合計金額 (円)</label>
          <input
            id="amount"
            v-model.number="newBill.total_amount"
            type="number"
            required
            placeholder="金額を入力"
          />
        </div>
        <button type="submit">URLを発行する</button>
      </form>
    </div>

    <!-- Bill Details (Shared View) -->
    <div v-if="billId && billData" class="bill-details">
      <h2>割り勘詳細</h2>
      <div class="card">
        <p><strong>名目:</strong> {{ billData.description }}</p>
        <p><strong>合計金額:</strong> {{ formatCurrency(billData.total_amount) }}</p>
      </div>

      <div class="share-section">
        <p>このページを共有してください:</p>
        <div class="url-box">
          <input type="text" readonly :value="currentUrl" />
          <button @click="copyUrl">コピー</button>
        </div>
      </div>
      
      <button @click="goHome" class="secondary-btn">新しく作成する</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

// API Base URL - adjust port if backend runs elsewhere
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
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.post(`${API_URL}/bills`, newBill.value);
    const createdId = response.data.id;
    // Navigate to the view page for the created bill
    router.push(`/${createdId}`);
  } catch (err) {
    console.error(err);
    error.value = "作成に失敗しました。";
  } finally {
    loading.value = false;
  }
};

const copyUrl = () => {
  navigator.clipboard.writeText(currentUrl.value).then(() => {
    alert('URLをコピーしました！');
  });
};

const goHome = () => {
  router.push('/');
  billData.value = null;
  newBill.value = { description: '', total_amount: null };
};

// Watch for route changes to handle navigation between IDs or back to home
watch(() => route.params.id, (newId) => {
  billId.value = newId;
  if (newId) {
    fetchBill(newId);
  } else {
    billData.value = null;
  }
});

onMounted(() => {
  if (billId.value) {
    fetchBill(billId.value);
  }
});
</script>

<style scoped>
.split-bill-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  font-family: sans-serif;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  box-sizing: border-box;
}

button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #3aa876;
}

.secondary-btn {
  background-color: #666;
  margin-top: 1rem;
}

.error {
  color: red;
  margin-bottom: 1rem;
}

.card {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
  background-color: #f9f9f9;
  text-align: left;
}

.share-section {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #eef;
  border-radius: 8px;
}

.url-box {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.url-box input {
  flex: 1;
}
</style>
