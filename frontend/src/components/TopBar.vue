<template>
  <div class="flex items-center justify-between px-6 pt-6 pb-2 w-full absolute top-0 left-0 z-30 text-white" dir="rtl">
    
    <!-- Empty div for spacing/centering balance if needed, or absolute positioning -->
    <div class="w-8"></div> 

    <!-- Centered Bot Info -->
    <div v-if="showBot" class="flex flex-col items-center gap-2 absolute left-1/2 top-6 -translate-x-1/2">
      <div class="w-12 h-12 rounded-full overflow-hidden border-2 border-white/20 shadow-sm">
        <img src="@/assets/bot.jpg" alt="Bot" class="w-full h-full object-cover" />
      </div>
    </div>

    <!-- Info Button (conditionally shown) -->
    <button 
      v-if="showInfo"
      @click="emit('open-about')"
      class="w-8 h-8 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 text-white/90 hover:text-white transition-colors"
      aria-label="About"
    >
       <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
       </svg>
    </button>
    <div v-else class="w-8"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  showBot?: boolean
  showInfo?: boolean
}>()

const emit = defineEmits<{
  (e: 'open-about'): void
}>()
</script>
