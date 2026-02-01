
<template>
  <header class="bg-white dark:bg-slate-800 shadow-md">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <h1 @click="goHome" class="text-2xl font-bold text-slate-900 dark:text-white cursor-pointer">割り勘.com</h1>
      <div class="flex items-center gap-4">
        <p v-if="billDescription" class="text-sm text-slate-600 dark:text-slate-400 hidden sm:block">
          <strong>名目:</strong> {{ billDescription }}
        </p>
        <button v-if="billId" @click="copyUrl" title="URLをコピー" class="p-2 rounded-full bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" /></svg>
        </button>
      </div>
    </div>
  </header>

  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="transform translate-y-full opacity-0"
    enter-to-class="transform translate-y-0 opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="transform translate-y-0 opacity-100"
    leave-to-class="transform translate-y-full opacity-0"
  >
    <div v-if="showToast" class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-slate-800 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <span>コピーしました</span>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

defineProps({
  billId: {
    type: String,
    default: null
  },
  billDescription: {
    type: String,
    default: ''
  }
});

const router = useRouter();
const showToast = ref(false);
const toastTimeout = ref(null);

const currentUrl = computed(() => window.location.href);

const goHome = () => {
  router.push('/');
};

const copyUrl = () => {
  navigator.clipboard.writeText(currentUrl.value).then(() => {
    if (toastTimeout.value) {
      clearTimeout(toastTimeout.value);
    }
    showToast.value = true;
    toastTimeout.value = setTimeout(() => {
      showToast.value = false;
      toastTimeout.value = null;
    }, 3000);
  });
};
</script>
