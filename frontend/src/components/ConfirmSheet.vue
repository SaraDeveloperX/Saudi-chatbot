<template>
  <Transition name="slide-up">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end justify-center pointer-events-none" dir="rtl">
      <!-- Backdrop -->
      <div 
        class="absolute inset-0 bg-black/20 backdrop-blur-[1px] pointer-events-auto transition-opacity duration-300"
        @click="$emit('cancel')"
      ></div>

      <!-- Sheet Container -->
      <div class="bg-white w-full max-w-3xl rounded-t-[32px] shadow-[0_-8px_30px_rgba(0,0,0,0.12)] z-10 pointer-events-auto pb-[env(safe-area-inset-bottom)] flex flex-col max-h-[85vh] transition-transform duration-300 transform">
        
        <!-- Header / Drag Handle -->
        <div class="flex flex-col items-center pt-3 pb-2 flex-shrink-0 cursor-pointer" @click="$emit('cancel')">
          <div class="w-12 h-1.5 bg-gray-300 rounded-full mb-4"></div>
          <h3 class="text-lg font-bold text-gray-900">{{ title }}</h3>
        </div>

        <!-- Content -->
        <div class="px-6 pb-8 pt-2 text-center">
            <p class="text-gray-600 mb-8 text-base leading-relaxed">{{ subtitle }}</p>
            
            <div class="flex items-center gap-3 justify-center">
                <button 
                @click="$emit('cancel')"
                class="flex-1 py-3 text-gray-600 font-bold bg-gray-100 hover:bg-gray-200 rounded-2xl transition-colors text-base"
                >
                {{ cancelText }}
                </button>
                <button 
                @click="$emit('confirm')"
                class="flex-1 py-3 bg-[#6CAD85] text-white font-bold hover:bg-[#5b9671] rounded-2xl shadow-sm transition-all text-base"
                >
                {{ confirmText }}
                </button>
            </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

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
.slide-up-enter-active,
.slide-up-leave-active {
  transition: opacity 0.3s ease;
}

.slide-up-enter-active > div:last-child,
.slide-up-leave-active > div:last-child {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from > div:first-child,
.slide-up-leave-to > div:first-child {
  opacity: 0;
}

.slide-up-enter-from > div:last-child,
.slide-up-leave-to > div:last-child {
  transform: translateY(100%);
}
</style>
