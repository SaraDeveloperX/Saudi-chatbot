<template>
  <div class="flex flex-col gap-2 relative group max-w-[78%] md:max-w-[70%]" 
    dir="rtl"
  >
    <!-- Bubble Container -->
    <div class="relative w-full">
      <!-- Bubble -->
      <div
        :class="[
          'px-5 py-3.5 text-[15px] leading-relaxed break-words font-normal whitespace-pre-wrap select-text w-full text-right',
          isUser
            ? 'bg-[#6CAD85] text-white rounded-[24px] rounded-br-[4px] shadow-sm'
            : isError 
              ? 'bg-red-50 text-red-700 border border-red-100 rounded-[24px] rounded-bl-[4px]'
              : 'bg-[#EEF0F2] text-[#1F2937] rounded-[24px] rounded-bl-[4px]',
           'prose-rtl'
        ]"
      >
        <slot />
        
        <!-- Retry Button -->
        <div v-if="isError" class="mt-3 flex justify-end">
          <button 
            @click="emit('retry')"
            class="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-red-200 hover:bg-red-50 text-red-600 rounded-full text-xs font-bold transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 2v6h-6"></path>
              <path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path>
              <path d="M3 22v-6h6"></path>
              <path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path>
            </svg>
            <span>إعادة المحاولة</span>
          </button>
        </div>
      </div>

      <!-- Copy Button (Bot Only) -->
      <div v-if="!isUser" class="absolute -left-8 bottom-0 flex flex-col items-center">
         <!-- Tooltip -->
        <Transition name="fade">
          <div 
            v-if="copyStatus !== 'idle'"
            class="absolute bottom-full mb-1 px-2 py-1 bg-black/65 text-white text-xs rounded-lg whitespace-nowrap pointer-events-none z-10 font-tajawal"
          >
            {{ copyStatus === 'success' ? 'تم النسخ' : 'تعذر النسخ' }}
          </div>
        </Transition>

        <button
          @click="copyText"
          class="p-1.5 text-gray-400 hover:text-[#6CAD85] opacity-100 md:opacity-0 group-hover:opacity-100 transition-all"
          aria-label="نسخ الإجابة"
          title="نسخ"
        >
          <svg v-if="copyStatus === 'success'" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-[#6CAD85]">
             <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Sources Button (Only for bot if has sources) -->
    <template v-if="!isUser && hasSources">
      <button 
        @click="emit('open-sources')"
        class="flex items-center gap-1.5 px-3 py-1.5 mt-1 mr-1 text-xs font-bold text-[#6CAD85] bg-[#6CAD85]/10 hover:bg-[#6CAD85]/20 rounded-full transition-colors w-fit"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <line x1="10" y1="9" x2="8" y2="9"></line>
        </svg>
        <span>المصادر</span>
      </button>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  isUser?: boolean
  hasSources?: boolean
  text?: string
  isError?: boolean
}>()

const emit = defineEmits<{
  (e: 'open-sources'): void
  (e: 'retry'): void
}>()

const copyStatus = ref<'idle' | 'success' | 'error'>('idle')
let timeoutId: ReturnType<typeof setTimeout>

const copyText = async () => {
  if (!props.text) return
  
  // Clear any existing timeout
  if (timeoutId) clearTimeout(timeoutId)
  
  try {
    await navigator.clipboard.writeText(props.text)
    copyStatus.value = 'success'
  } catch (err) {
    copyStatus.value = 'error'
  }
  
  // Reset after delay
  timeoutId = setTimeout(() => {
    copyStatus.value = 'idle'
  }, 1200)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Fix Markdown Lists in RTL */
.prose-rtl :deep(ul), .prose-rtl :deep(ol) {
  margin-right: 1.5em; /* Space for bullets on right */
  margin-left: 0;
  list-style-position: outside;
}

.prose-rtl :deep(li) {
  margin-bottom: 0.25em;
}

.prose-rtl :deep(ul) {
  list-style-type: disc;
}

.prose-rtl :deep(ol) {
  list-style-type: decimal;
}
</style>
