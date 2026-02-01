
<template>
  <div>
    <!-- Loading State -->
    <LoadingSpinner v-if="loading && !billData" />

    <!-- Error State -->
    <ErrorMessage v-if="error" :message="error" @clear="clearError" />
    
    <!-- Bill Details View -->
    <div v-if="billData && !error" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Left Column: Members & Expenses -->
      <div class="space-y-8">
        <h2 class="text-2xl font-bold mb-4 text-center lg:text-left">{{ billData.description }}</h2>
        <MemberList 
          :members="billData.members" 
          :submitting="submitting"
          @add-member="handleAddMember"
          @delete-member="handleDeleteMember"
        />
        <ExpenseForm 
          :members="billData.members"
          :submitting="submitting"
          @add-expense="handleAddExpense"
        />
      </div>

      <!-- Right Column: Expense List & Settle -->
      <div class="space-y-8">
         <ExpenseList 
           :expenses="billData.expenses"
           @delete-expense="handleDeleteExpense"
         />
         <SettlementList 
           :settlement="settlement"
           :has-expenses="billData.expenses?.length > 0"
         />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useBill } from '@/composables/useBill';

import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import MemberList from '@/components/bill/MemberList.vue';
import ExpenseForm from '@/components/bill/ExpenseForm.vue';
import ExpenseList from '@/components/bill/ExpenseList.vue';
import SettlementList from '@/components/bill/SettlementList.vue';

const route = useRoute();
const { 
  billData, 
  settlement, 
  loading, 
  submitting, 
  error, 
  fetchBill,
  addMember,
  deleteMember,
  addExpense,
  deleteExpense,
  clearError
} = useBill();

const handleAddMember = (name) => {
  addMember(route.params.id, name);
};

const handleDeleteMember = (memberId) => {
  deleteMember(route.params.id, memberId);
};

const handleAddExpense = (expenseData) => {
  return addExpense(route.params.id, expenseData);
};

const handleDeleteExpense = (expenseId) => {
  deleteExpense(route.params.id, expenseId);
};

watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchBill(newId);
  }
}, { immediate: true });

</script>
