
<template>
  <section class="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6">
    <h3 class="text-xl font-semibold mb-4">メンバー</h3>
    <ul v-if="members?.length > 0" class="space-y-2 mb-4">
      <li v-for="member in members" :key="member.id" class="flex justify-between items-center bg-slate-50 dark:bg-slate-700/50 p-3 rounded-lg">
        <span class="font-medium">{{ member.name }}</span>
        <button @click="$emit('delete-member', member.id)" class="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-100 dark:hover:bg-red-900/50 transition" title="削除">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
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
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  members: {
    type: Array,
    default: () => []
  },
  submitting: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['add-member', 'delete-member']);

const newMemberName = ref('');

const addMember = () => {
  if (newMemberName.value.trim()) {
    emit('add-member', newMemberName.value);
    newMemberName.value = '';
  }
};
</script>
