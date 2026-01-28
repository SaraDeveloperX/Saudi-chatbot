<template>
  <div class="min-h-screen bg-page-bg flex flex-col items-center">
    <!-- Green Header -->
    <div class="w-full h-36 bg-primary"></div>
    
    <!-- White Card -->
    <div class="w-full max-w-md -mt-12 bg-white rounded-t-[40px] shadow-lg flex-1 flex flex-col relative">
      <!-- Bot Icon (overlapping) -->
      <div v-if="showBotIcon" class="absolute -top-8 left-1/2 -translate-x-1/2">
        <div class="w-16 h-16 rounded-full bg-white shadow-md flex items-center justify-center p-2">
          <img :src="botIcon" alt="Bot" class="w-full h-full" />
        </div>
      </div>
      
      <!-- Content Slot -->
      <div class="flex-1 flex flex-col p-6" :class="showBotIcon ? 'pt-12' : ''">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import botIcon from '@/assets/bot.svg'

defineProps<{
  showBotIcon?: boolean
}>()
</script>
