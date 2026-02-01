
<template>
  <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">立替の追加</h3>
    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium mb-1">内容</label>
        <input v-model="form.description" type="text" required placeholder="例: 夕食代" class="w-full input"/>
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">金額</label>
        <input v-model.number="form.amount" type="number" required placeholder="例: 8000" class="w-full input"/>
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">支払った人</label>
        <select v-model="form.payer_id" required class="w-full input">
          <option disabled value="">選択してください</option>
          <option v-for="member in members" :key="member.id" :value="member.id">{{ member.name }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">対象者 (複数選択可)</label>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
           <div>
              <input type="checkbox" id="select-all" v-model="allBeneficiariesSelected" class="mr-2"/>
              <label for="select-all">全員</label>
          </div>
          <div v-for="member in members" :key="member.id">
            <input type="checkbox" :id="'mem-'+member.id" :value="member.id" v-model="form.beneficiary_ids" class="mr-2"/>
            <label :for="'mem-'+member.id">{{ member.name }}</label>
          </div>
        </div>
      </div>
      <button type="submit" :disabled="submitting" class="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg transition-colors">
        {{ submitting ? '追加中...' : '立替を追加' }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  members: {
    type: Array,
    default: () => []
  },
  submitting: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['add-expense']);

const createInitialFormState = () => ({
  description: '',
  amount: null,
  payer_id: '',
  beneficiary_ids: props.members.map(m => m.id)
});

const form = ref(createInitialFormState());

const allBeneficiariesSelected = computed({
  get() {
    return props.members.length > 0 && form.value.beneficiary_ids.length === props.members.length;
  },
  set(value) {
    if (value) {
      form.value.beneficiary_ids = props.members.map(m => m.id);
    } else {
      form.value.beneficiary_ids = [];
    }
  }
});

watch(() => props.members, (newMembers) => {
  if (newMembers) {
    form.value.beneficiary_ids = newMembers.map(m => m.id);
  }
}, { deep: true, immediate: true });

const resetForm = () => {
  form.value = createInitialFormState();
};

const submit = async () => {
  // The useBill composable will handle the validation logic
  const success = await emit('add-expense', { ...form.value });
  if (success) {
    resetForm();
  }
};

// Expose resetForm to be called from parent if needed
defineExpose({ resetForm });
</script>

<style scoped>
/* Using a shared class for inputs from style.css */
.input {
  @apply w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition;
}
</style>
