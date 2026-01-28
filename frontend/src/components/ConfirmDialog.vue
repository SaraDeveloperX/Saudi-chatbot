<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm" dir="rtl">
      <div class="bg-white rounded-[24px] shadow-xl w-full max-w-sm p-6 transform transition-all" @click.stop>
        <h3 class="text-lg font-bold text-gray-900 mb-2">{{ title }}</h3>
        <p class="text-gray-600 mb-6 text-base">{{ subtitle }}</p>
        
        <div class="flex items-center gap-3 justify-end">
          <button 
            @click="$emit('cancel')"
            class="px-4 py-2 text-gray-600 font-medium hover:bg-gray-100 rounded-xl transition-colors text-sm"
          >
            {{ cancelText }}
          </button>
          <button 
            @click="$emit('confirm')"
            class="px-4 py-2 bg-[#6CAD85] text-white font-medium hover:bg-[#5b9671] rounded-xl shadow-sm transition-all text-sm"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean
  title: string
  subtitle: string
  confirmText: string
  cancelText: string
}>()

defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
