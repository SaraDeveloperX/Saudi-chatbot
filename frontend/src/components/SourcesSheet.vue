<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end justify-center" dir="rtl">
    <!-- Backdrop -->
    <div 
      class="absolute inset-0 bg-black/40 backdrop-blur-[2px] transition-opacity"
      @click="emit('close')"
    ></div>

    <!-- Sheet -->
    <div class="relative w-full md:max-w-[430px] bg-white rounded-t-[32px] overflow-hidden flex flex-col max-h-[85vh] shadow-[0_-10px_40px_rgba(0,0,0,0.1)] animate-slide-up">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 pt-5 pb-4 border-b border-gray-100">
        <h3 class="text-xl font-bold text-[#1F2937] font-sans">المصادر المستخدمة</h3>
        <button @click="emit('close')" class="p-2 -ml-2 text-gray-400 hover:text-gray-600 bg-gray-50 rounded-full">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Sources List -->
      <div class="overflow-y-auto p-5 pb-8 flex flex-col gap-4">
        <div 
          v-for="(source, idx) in sources" 
          :key="idx" 
          class="border border-gray-100 rounded-2xl p-4 bg-gray-50/50 hover:bg-gray-50 transition-colors"
        >
          <!-- Section / Tag -->
          <div class="flex items-center gap-2 mb-2">
            <span class="text-xs font-bold text-[#6CAD85] bg-[#6CAD85]/10 px-2.5 py-1 rounded-full">
              المصدر [{{ idx + 1 }}]
            </span>
            <span class="text-xs text-gray-500 truncate max-w-[200px]">{{ source.section }}</span>
          </div>

          <!-- Question (Title) -->
          <h4 class="text-sm font-bold text-gray-900 mb-2 leading-relaxed">
            {{ source.question }}
          </h4>

          <!-- Snippet -->
          <p class="text-xs text-gray-500 leading-relaxed line-clamp-3 mb-3">
            {{ source.snippet }}
          </p>

          <!-- Link -->
           <a 
            :href="source.source" 
            target="_blank" 
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1.5 text-xs font-bold text-[#6CAD85] hover:underline"
          >
            <span>فتح المصدر</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface SourceItem {
  section: string
  question: string
  source: string
  score: float
  snippet: string
}

defineProps<{
  isOpen: boolean
  sources: SourceItem[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
