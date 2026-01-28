<template>
  <component 
    :is="currentView" 
    v-bind="currentProps"
    @start-chat="handleStartChat"
    @send-message="handleSendMessage"
    @reset-chat="handleResetChat"
    @retry="handleRetry"
    @open-about="handleOpenAbout"
    @close="handleCloseAbout"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import WelcomePage from '@/pages/Welcome.vue'
import ChatPage from '@/pages/Chat.vue'
import AboutPage from '@/pages/About.vue'

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

const isChatStarted = ref(false)
const isAboutOpen = ref(false)
const messages = ref<Message[]>([])
const isLoading = ref(false)
const lastUserMessage = ref('')

const currentView = computed(() => {
  if (isAboutOpen.value) return AboutPage
  if (isChatStarted.value) return ChatPage
  return WelcomePage
})

// Props to pass dynamically to the current page
const currentProps = computed(() => {
  if (isChatStarted.value) {
    return {
      messages: messages.value,
      isLoading: isLoading.value
    }
  }
  return {}
})

const handleStartChat = (msg: string) => {
  isChatStarted.value = true
  handleSendMessage(msg)
}

const handleOpenAbout = () => {
  isAboutOpen.value = true
}

const handleCloseAbout = () => {
  isAboutOpen.value = false
}

const handleSendMessage = async (msg: string) => {
  // Store for retry
  lastUserMessage.value = msg
  
  // Add user message
  messages.value.push({ text: msg, isUser: true })
  
  // Call backend
  isLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    })
    
    if (response.ok) {
      const data = await response.json()
      // Correctly map backend response to message with sources
      messages.value.push({ 
        text: data.answer, 
        isUser: false,
        sources: data.sources 
      })
    } else {
      messages.value.push({ 
        text: 'تعذر الاتصال بالخادم. تأكد أنه يعمل ثم جرّب مرة ثانية.', 
        isUser: false, 
        isError: true 
      })
    }
  } catch (error) {
    messages.value.push({ 
      text: 'تعذر الاتصال بالخادم. تأكد أنه يعمل ثم جرّب مرة ثانية.', 
      isUser: false, 
      isError: true 
    })
  } finally {
    isLoading.value = false
  }
}

const handleRetry = () => {
  // Remove the last message if it was an error
  if (messages.value.length > 0 && messages.value[messages.value.length - 1].isError) {
    messages.value.pop()
  }
  
  // Remove the user message too so we don't duplicate it? 
  // Requirements say: "re-sends the last user message". 
  // Usually this means we just call the API again. 
  // But handleSendMessage adds the user message to the list. 
  // So we should probably NOT call handleSendMessage directly if we want to avoid duplicating the user bubble.
  // OR we modify handleSendMessage to optionally skip adding user message.
  // Let's create a specialized retry flow:
  
  retryLastMessage()
}

const retryLastMessage = async () => {
  // Don't add user message again, just call API
  isLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: lastUserMessage.value })
    })
    
    if (response.ok) {
      const data = await response.json()
      messages.value.push({ 
        text: data.answer, 
        isUser: false,
        sources: data.sources 
      })
    } else {
      messages.value.push({ 
        text: 'تعذر الاتصال بالخادم. تأكد أنه يعمل ثم جرّب مرة ثانية.', 
        isUser: false, 
        isError: true 
      })
    }
  } catch (error) {
    messages.value.push({ 
      text: 'تعذر الاتصال بالخادم. تأكد أنه يعمل ثم جرّب مرة ثانية.', 
      isUser: false, 
      isError: true 
    })
  } finally {
    isLoading.value = false
  }
}

const handleResetChat = () => {
  messages.value = []
  isLoading.value = false
  isChatStarted.value = false
}
</script>
