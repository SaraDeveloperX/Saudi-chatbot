<template>
  <AppShell>
    <!-- Header Content -->
    <template #header-content>
      <TopBar />
    </template>

    <div class="flex-1 flex flex-col items-center pt-8 pb-4 h-full relative">
      <!-- Bot Icon -->
      <!-- Bot Icon -->
      <div class="w-[140px] h-[140px] mb-8 bg-[#6CAD85]/10 rounded-full flex items-center justify-center overflow-hidden">
        <img src="@/assets/bot.jpg" alt="Bot" class="w-full h-full object-cover" />
      </div>

      <!-- Text Content -->
      <h1 class="text-[28px] font-bold text-[#6CAD85] mb-2 font-sans tracking-tight">حياك الله</h1>
      <p class="text-[#6CAD85] text-base mb-8 font-normal opacity-90">وش ودّك تعرف عن السعودية؟</p>

      <!-- Spacer -->
      <div class="flex-1 min-h-[40px]"></div>
      
      <!-- Input Area -->
      <div class="w-full mt-auto flex flex-col items-center">
        <ChatInput placeholder="اكتب سؤالك هنا..." @send="onSend" />
        
        <!-- About Link -->
        <button 
          @click="emit('open-about')" 
          class="mt-6 text-[#6CAD85] text-sm font-medium opacity-80 hover:opacity-100 transition-opacity"
        >
          عن المشروع
        </button>
      </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import AppShell from '@/components/AppShell.vue'
import TopBar from '@/components/TopBar.vue'
import ChatInput from '@/components/ChatInput.vue'

const emit = defineEmits<{
  (e: 'start-chat', message: string): void
  (e: 'open-about'): void
}>()

const onSend = (msg: string) => {
  emit('start-chat', msg)
}
</script>
