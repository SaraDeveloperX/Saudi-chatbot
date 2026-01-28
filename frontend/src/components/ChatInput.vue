<template>
  <div class="w-full relative h-[56px]">
    <input
      v-model="inputValue"
      type="text"
      dir="rtl"
      :placeholder="placeholder"
      :disabled="isLoading"
      class="w-full h-full pl-4 pr-[60px] rounded-[9999px] bg-[#F0F2F4] text-[#2F6B4E] text-right placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-[#6CAD85] transition-all text-base font-medium disabled:opacity-70 disabled:cursor-wait"
      @keydown.enter="handleEnter"
    />
    
    <button
      @click="handleSend"
      :disabled="!inputValue.trim() || isLoading"
      class="absolute top-1/2 -translate-y-1/2 flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
      style="
        right: 6px; 
        width: 44px; 
        height: 44px; 
        border-radius: 50%;
        background-color: #6CAD85;
      "
    >
      <!-- Change icon to match reference (mic/send) or kept as send 
           User request says "small mic/send icon on right (can be send icon)"
           Keeping send icon.
      -->
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white -mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
         <line x1="5" y1="12" x2="19" y2="12"></line>
         <polyline points="12 5 5 12 12 19"></polyline>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'

defineProps<{
  placeholder?: string
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'send', message: string): void
}>()

const inputValue = ref('')

const handleSend = () => {
  if (inputValue.value.trim()) {
    emit('send', inputValue.value.trim())
    inputValue.value = ''
  }
}

const handleEnter = (e: KeyboardEvent) => {
  if (e.shiftKey) return // Allow multiline
  e.preventDefault()
  handleSend()
}
</script>
