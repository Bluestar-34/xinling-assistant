<template>
  <div class="app-container">
    <header class="header">
      <div class="logo">
        <h1>心聆助手</h1>
      </div>
    </header>
    <main class="main-content">
      <div class="chat-container">
        <div class="chat-header">
          <div class="therapist-info">
            <h3>小南心</h3>
            <p>专业倾听，温暖陪伴</p>
          </div>
        </div>
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
            <div class="message-content">
              <div class="message-bubble">
                <div class="text">{{ message.content }}</div>
                <span class="time">{{ message.time }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="input-area">
          <div class="input-wrapper">
            <textarea 
              v-model="userInput"
              @keyup.enter="sendMessage"
              placeholder="告诉我你的想法..."
              rows="3"
            ></textarea>
            <button class="send-btn" @click="sendMessage">
              发送 <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      messages: [],
      userInput: '',
      sessionId: null
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return
      const now = new Date()
      const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      this.messages.push({
        role: 'user',
        content: this.userInput,
        time: time
      })
      const message = this.userInput
      this.userInput = ''
      try {
        const response = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: message,
            session_id: this.sessionId
          })
        })
        const data = await response.json()
        if (data.session_id) {
          this.sessionId = data.session_id
        }
        this.messages.push({
          role: 'assistant',
          content: data.response,
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        })
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }
}
</script>

<style>
:root {
  --primary-color: #2C3E50;
  --background-color: #F8F9FA;
  --text-color: #2C3E50;
  --border-radius: 12px;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}
.app-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
.logo h1 {
  font-size: 1.8em;
  font-weight: 500;
  color: var(--primary-color);
}
.chat-container {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  min-height: 500px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-header {
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: var(--primary-color);
  color: white;
}
.therapist-info h3 {
  margin: 0;
  font-size: 1.1em;
  font-weight: 500;
}
.therapist-info p {
  margin: 5px 0 0 0;
  opacity: 0.8;
  font-size: 0.9em;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: #f8f9fa;
}
.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}
.message.user {
  align-self: flex-end;
}
.message-content {
  display: flex;
  gap: 10px;
}
.message-bubble {
  background: white;
  padding: 12px 16px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  position: relative;
}
.message.user .message-bubble {
  background: var(--primary-color);
  color: white;
}
.time {
  font-size: 0.75em;
  opacity: 0.7;
  margin-top: 5px;
  display: block;
}
.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: var(--border-radius);
  resize: none;
  font-family: inherit;
  font-size: 1em;
  transition: var(--transition);
}
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.1);
}
.send-btn {
  padding: 12px 24px;
  border: none;
  border-radius: var(--border-radius);
  background: var(--primary-color);
  color: white;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.95em;
  align-self: flex-end;
}
.send-btn:hover {
  background: #34495E;
  transform: translateY(-2px);
}
</style> 