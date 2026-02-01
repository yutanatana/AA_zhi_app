
import { ref, computed, readonly } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function useBill() {
  const router = useRouter();

  const billData = ref(null);
  const settlement = ref([]);
  const loading = ref(false);
  const submitting = ref(false);
  const error = ref(null);

  const handleApiError = (err, defaultMessage) => {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail;
    } else {
      error.value = defaultMessage;
    }
    console.error(err);
  };

  const fetchBill = async (id) => {
    loading.value = true;
    error.value = null;
    billData.value = null;
    settlement.value = [];
    try {
      const response = await axios.get(`${API_URL}/bills/${id}`);
      billData.value = response.data;
      if (billData.value.members.length > 0 && billData.value.expenses.length > 0) {
        await fetchSettlement(id);
      }
    } catch (err) {
      handleApiError(err, "割り勘情報の取得に失敗しました。");
      billData.value = null; // Ensure data is cleared on error
    } finally {
      loading.value = false;
    }
  };

  const fetchSettlement = async (billId) => {
    try {
      const response = await axios.get(`${API_URL}/bills/${billId}/settle`);
      settlement.value = response.data;
    } catch (err) {
      console.error("Failed to fetch settlement:", err);
      // Not showing a user-facing error for this, as it's a secondary call.
    }
  };

  const createBill = async (description) => {
    if (submitting.value) return;
    submitting.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${API_URL}/bills`, { description });
      router.push(`/${response.data.id}`);
    } catch (err) {
      handleApiError(err, "作成に失敗しました。");
    } finally {
      submitting.value = false;
    }
  };

  const addMember = async (billId, name) => {
    if (!name.trim() || submitting.value) return;
    submitting.value = true;
    error.value = null;
    try {
      await axios.post(`${API_URL}/bills/${billId}/members`, { name });
      await fetchBill(billId); // Refresh data
    } catch (err) {
      handleApiError(err, "メンバーの追加に失敗しました。");
    } finally {
      submitting.value = false;
    }
  };

  const deleteMember = async (billId, memberId) => {
    if (!confirm('本当にこのメンバーを削除しますか？')) return;
    loading.value = true; // Use loading state for a global indicator
    error.value = null;
    try {
      await axios.delete(`${API_URL}/bills/${billId}/members/${memberId}`);
      await fetchBill(billId);
    } catch (err) {
      handleApiError(err, "メンバーの削除に失敗しました。支払履歴がある場合は削除できません。");
    } finally {
      loading.value = false;
    }
  };

  const addExpense = async (billId, expenseData) => {
     if (expenseData.beneficiary_ids.length === 0) {
      error.value = "対象者を1人以上選択してください。";
      return;
    }
    if (submitting.value) return;
    submitting.value = true;
    error.value = null;
    try {
      await axios.post(`${API_URL}/bills/${billId}/expenses`, expenseData);
      await fetchBill(billId); // Refresh data
      return true; // Indicate success for form reset
    } catch (err) {
      handleApiError(err, "立替の追加に失敗しました。");
      return false;
    } finally {
      submitting.value = false;
    }
  };

  const deleteExpense = async (billId, expenseId) => {
    if (!confirm('本当にこの立替を削除しますか？')) return;
    loading.value = true;
    error.value = null;
    try {
      await axios.delete(`${API_URL}/bills/${billId}/expenses/${expenseId}`);
      await fetchBill(billId);
    } catch (err) {
      handleApiError(err, "立替の削除に失敗しました。");
    } finally {
      loading.value = false;
    }
  };
  
  const clearError = () => {
    error.value = null;
  }

  return {
    billData: readonly(billData),
    settlement: readonly(settlement),
    loading: readonly(loading),
    submitting: readonly(submitting),
    error: readonly(error),
    fetchBill,
    createBill,
    addMember,
    deleteMember,
    addExpense,
    deleteExpense,
    clearError,
  };
}
