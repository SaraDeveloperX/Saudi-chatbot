<template>
  <Transition name="toast">
    <div 
      v-if="show"
      class="fixed left-1/2 -translate-x-1/2 z-50 flex items-center justify-center gap-2 px-3 py-2 rounded-xl backdrop-blur-sm shadow-sm"
      :class="[
        'bottom-[calc(16px+env(safe-area-inset-bottom))]',
        isError ? 'bg-red-500/90 text-white' : 'bg-[#1F2937]/85 text-white'
      ]"
    >
      <span class="text-sm font-medium font-tajawal leading-none pt-0.5">{{ message }}</span>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
  message: string
  isError?: boolean
}>()
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.12s ease-out;
}
.toast-leave-active {
  transition: all 0.18s ease-in;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 8px);
}
</style>
