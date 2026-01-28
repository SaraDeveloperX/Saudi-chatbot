<template>
  <AppShell>
    <!-- Header Content -->
    <template #header-content>
      <TopBar :showBot="true" :showInfo="true" @open-about="emit('open-about')" />
    </template>

    <div class="flex-1 flex flex-col h-full pt-[32px] relative overflow-hidden">
      
      <!-- New Chat Button (Top Left in RTL) -->
      <div class="flex justify-end px-4 mb-1">
        <button 
          v-if="messages.length > 0"
          @click="onNewChatClick"
          class="flex items-center gap-2 text-[#6CAD85] hover:bg-[#6CAD85]/10 px-3 py-1.5 rounded-full transition-colors text-sm font-medium"
        >
          <span class="text-lg leading-none">↺</span>
          <span>بدء محادثة جديدة</span>
        </button>
      </div>

      <!-- Messages List -->
      <div 
        ref="messagesContainer"
        class="flex-1 overflow-y-auto flex flex-col gap-4 px-1 no-scrollbar pt-2 scroll-smooth max-w-3xl mx-auto w-full" 
        :style="containerStyle"
        dir="rtl"
      >
        <template v-for="(msg, idx) in messages" :key="idx">
          <div class="flex w-full" dir="ltr" :class="msg.isUser ? 'justify-end' : 'justify-start'">
            <ChatBubble 
              :isUser="msg.isUser"
              :hasSources="shouldShowSources(msg.sources)"
              :text="msg.text"
              :isError="msg.isError"
              @open-sources="openSources(msg.sources)"
              @retry="emit('retry')"
            >
              {{ msg.text }}
            </ChatBubble>
          </div>
        </template>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="self-start mr-auto animate-pulse">
           <div class="bg-[#EEF0F2] px-5 py-4 rounded-[28px] rounded-bl-[4px]">
             <div class="flex gap-1.5 h-6 items-center">
               <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
               <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
               <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
             </div>
           </div>
        </div>
      </div>

      <!-- Fixed Bottom Input (Flex item, safe area handled) -->
      <div class="flex-shrink-0 bg-white pt-2 w-full border-t border-transparent">
        <div class="max-w-3xl mx-auto w-full pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)] pr-[env(safe-area-inset-right)]">
          <ChatInput 
            placeholder="اكتب سؤالك هنا..." 
            :isLoading="isLoading"
            @send="onSend" 
          />
        </div>
      </div>

      <!-- Sources Bottom Sheet -->
      <SourcesSheet 
        :isOpen="showSources"
        :sources="activeSources"
        @close="showSources = false"
      />
      
      <ConfirmSheet 
        :isOpen="showResetDialog"
        title="بدء محادثة جديدة؟"
        subtitle="سيتم مسح المحادثة الحالية والبدء من جديد."
        confirmText="بدء جديد"
        cancelText="إلغاء"
        @confirm="confirmReset"
        @cancel="showResetDialog = false"
      />

    </div>
  </AppShell>
</template>

<script setup lang="ts">
import { ref, nextTick, watchEffect, onMounted, onUnmounted, computed } from 'vue'
import AppShell from '@/components/AppShell.vue'
import TopBar from '@/components/TopBar.vue'

import ChatInput from '@/components/ChatInput.vue'
import ChatBubble from '@/components/ChatBubble.vue'
import SourcesSheet from '@/components/SourcesSheet.vue'
import ConfirmSheet from '@/components/ConfirmSheet.vue'


interface SourceItem {
  section: string
  question: string
  source: string
  score: number
  snippet: string
}

interface Message {
  text: string
  isUser: boolean
  sources?: SourceItem[]
  isError?: boolean
}

const props = defineProps<{
  messages: Message[]
  isLoading: boolean
}>()

const emit = defineEmits<{
  (e: 'send-message', message: string): void
  (e: 'reset-chat'): void
  (e: 'retry'): void
  (e: 'open-about'): void
}>()

const messagesContainer = ref<HTMLElement | null>(null)
const showSources = ref(false)
const activeSources = ref<SourceItem[]>([])
const showResetDialog = ref(false)

// Keyboard & Viewport Logic
const keyboardHeight = ref(0)
const isKeyboardOpen = ref(false)
const viewportHeight = ref(0)

const handleViewportResize = () => {
  if (!window.visualViewport) return
  
  const currentHeight = window.visualViewport.height
  const windowHeight = window.innerHeight
  const diff = windowHeight - currentHeight
  
  viewportHeight.value = currentHeight
  
  // Threshold to consider keyboard open (e.g. > 150px)
  if (diff > 150) {
    keyboardHeight.value = diff
    isKeyboardOpen.value = true
    // Force scroll to bottom if keyboard just opened and we were at bottom?
    // Requirement: "keyboard open/close -> auto-scroll"
    // We'll let the watcher handle the scroll if needed or call it here
    checkAndScrollToBottom(true) 
  } else {
    keyboardHeight.value = 0
    isKeyboardOpen.value = false
  }
}

const handleViewportScroll = () => {
    // Optional: could track scroll offset if needed for fixing input
}

onMounted(() => {
  if (window.visualViewport) {
    viewportHeight.value = window.visualViewport.height
    window.visualViewport.addEventListener('resize', handleViewportResize)
    window.visualViewport.addEventListener('scroll', handleViewportScroll)
  }
})

onUnmounted(() => {
  if (window.visualViewport) {
    window.visualViewport.removeEventListener('resize', handleViewportResize)
    window.visualViewport.removeEventListener('scroll', handleViewportScroll)
  }
})

// Dynamic padding style for messages container
const containerStyle = computed(() => {
  if (!isKeyboardOpen.value) return {}
  return {
    paddingBottom: `${keyboardHeight.value}px`
  }
})


// Scroll Logic
const isAtBottom = () => {
  if (!messagesContainer.value) return true // Default to true if not mounted
  const { scrollHeight, scrollTop, clientHeight } = messagesContainer.value
  const distanceToBottom = scrollHeight - scrollTop - clientHeight
  return distanceToBottom < 80 // 80px threshold
}

const scrollToBottom = (instant = false) => {
  nextTick(() => {
    if (messagesContainer.value) {
      if (instant) {
          messagesContainer.value.style.scrollBehavior = 'auto'
      }
      
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      
      if (instant) {
           // Restore smooth after a tick
           requestAnimationFrame(() => {
               if(messagesContainer.value) messagesContainer.value.style.scrollBehavior = 'smooth'
           })
      }
    }
  })
}

const checkAndScrollToBottom = (force = false) => {
    // Use requestAnimationFrame for smoothness and to ensure layout updated
    requestAnimationFrame(() => {
        if (force || isAtBottom()) {
            scrollToBottom()
        }
    })
}


// Watch messages to auto-scroll
// Requirement: "user send, bot response"
// We track length changes.
watchEffect(() => {
  if (props.messages.length) {
      // Check if the last message is from user to set 'justSent' equivalent
      const lastMsg = props.messages[props.messages.length - 1]
      const justSent = lastMsg.isUser
      
      checkAndScrollToBottom(justSent)
  }
})

// Also scroll when loading starts (bot thinking)
// watching props.isLoading
import { watch } from 'vue'
watch(() => props.isLoading, (newVal) => {
    if (newVal) {
        checkAndScrollToBottom(true) // Scroll to show loading indicator
    }
})


const onSend = (msg: string) => {
  emit('send-message', msg)
  // Force scroll immediately - relying on watchEffect might be slightly delayed or 'justSent' logic handles it
  // But explicitly calling it here ensures UI responsiveness
  scrollToBottom() 
}

// Helper to determine if we should show sources
const shouldShowSources = (sources?: SourceItem[]) => {
  if (!sources || sources.length === 0) return false
  
  // Use same logic as backend: score is similarity (0..1)
  // Backend returns "score" field.
  // We check the BEST score in the list
  const maxScore = Math.max(...sources.map(s => s.score))
  
  // Threshold from requirements
  const THRESHOLD = 0.7
  
  // Also check if valid link exists
  const hasValidLink = sources.some(s => s.source && s.source.trim().length > 0)
  
  return maxScore >= THRESHOLD && hasValidLink
}

const openSources = (sources?: SourceItem[]) => {
  if (shouldShowSources(sources)) {
    activeSources.value = sources || []
    showSources.value = true
  }
}

const onNewChatClick = () => {
  if (props.messages.length > 0) {
    showResetDialog.value = true
  }
}

const confirmReset = () => {
  showResetDialog.value = false
  // Close sources if open
  showSources.value = false
  emit('reset-chat')
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
