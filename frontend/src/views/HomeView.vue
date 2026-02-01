
<template>
  <div class="max-w-md mx-auto pt-12">
    <ErrorMessage v-if="error" :message="error" @clear="clearError" />
    <BillCreateForm :submitting="submitting" @create-bill="handleCreateBill" />
  </div>
</template>

<script setup>
import BillCreateForm from '@/components/bill/BillCreateForm.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import { useBill } from '@/composables/useBill';

const { submitting, error, createBill, clearError } = useBill();

const handleCreateBill = (description) => {
  createBill(description);
};
</script>
