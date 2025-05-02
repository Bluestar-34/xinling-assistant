<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>心聆助手</h1>
    </div>
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
        {{ message.content }}
      </div>
    </div>
    <div class="chat-input">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage"
        placeholder="在这里输入你想说的话..."
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading">
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const userMessage = userInput.value
  messages.value.push({ role: 'user', content: userMessage })
  userInput.value = ''
  await scrollToBottom()

  isLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content: userMessage }),
    })
    const data = await response.json()
    messages.value.push({ role: 'assistant', content: data.response })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({ 
      role: 'assistant', 
      content: '抱歉，我遇到了一些问题，请稍后再试。' 
    })
  }
  isLoading.value = false
  await scrollToBottom()
}

onMounted(() => {
  messages.value.push({
    role: 'assistant',
    content: '你好！我是心聆助手，很高兴能和你交流。请告诉我你的想法或困扰，我会认真倾听并尽力帮助你。'
  })
})
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.chat-header {
  background-color: #4a90e2;
  color: white;
  padding: 1rem;
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 70%;
  padding: 0.8rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.user-message {
  align-self: flex-end;
  background-color: #4a90e2;
  color: white;
}

.assistant-message {
  align-self: flex-start;
  background-color: white;
  color: #333;
}

.chat-input {
  padding: 1rem;
  background-color: white;
  display: flex;
  gap: 0.5rem;
}

input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

button {
  padding: 0.8rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #357abd;
}
</style> 