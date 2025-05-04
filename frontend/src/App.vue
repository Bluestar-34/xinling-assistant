<template>
  <div class="app-container">
    <!-- 仅显示一个箭头，点击后弹出菜单 -->
    <div class="sidebar-arrow-container">
      <button class="sidebar-arrow-btn" @click="sidebarVisible = !sidebarVisible">
        <i :class="sidebarVisible ? 'fas fa-chevron-left' : 'fas fa-chevron-right'"></i>
      </button>
      <transition name="sidebar-fade">
        <div v-if="sidebarVisible" class="sidebar-popup">
          <ul>
            <li :class="{active: currentTab==='station'}" @click="switchTab('station')">
              <i class="fas fa-comments"></i>
              <span>心理驿站</span>
            </li>
            <li :class="{active: currentTab==='assessment'}" @click="switchTab('assessment')">
              <i class="fas fa-heartbeat"></i>
              <span>心理评估</span>
            </li>
            <li :class="{active: currentTab==='science'}" @click="switchTab('science')">
              <i class="fas fa-book-open"></i>
              <span>心理科普</span>
            </li>
          </ul>
        </div>
      </transition>
    </div>
    <div class="main-content-full">
      <header class="header">
        <div class="logo">
          <h1>心聆助手</h1>
          <p class="subtitle">温暖陪伴，守护心灵</p>
        </div>
      </header>
      <main class="main-content">
        <div v-if="currentTab==='station'">
          <!-- 聊天主容器 -->
          <div class="chat-container">
            <div class="particles">
              <div v-for="n in 50" :key="n" class="particle"></div>
            </div>
            <div class="light-beams">
              <div v-for="n in 5" :key="n" class="beam"></div>
            </div>
            <div class="floating-elements">
              <div v-for="n in 12" :key="n" class="floating-element">
                <i :class="['fas', getFloatingIcon(n)]"></i>
              </div>
            </div>
            <div class="chat-header">
              <div class="therapist-info">
                <div class="avatar" @click="handleHeartClick" :class="{ clicked: isHeartClicked }">
                  <i class="fas fa-heart"></i>
                </div>
                <div class="info">
                  <h3>小南心</h3>
                  <p class="subtitle">专业倾听，温暖陪伴</p>
                </div>
              </div>
              <!-- 新增：鸡汤语录及爱心按钮 -->
              <div class="header-quote-box">
                <transition name="fade-float">
                  <span class="header-quote-text" v-if="currentQuote" :key="currentQuote">{{ currentQuote }}</span>
                </transition>
                <button class="header-quote-btn" @click="changeQuote" title="换一句鸡汤">
                  <i class="fas fa-heart"></i>
                </button>
              </div>
            </div>
            <div class="chat-layout">
              <div class="chat-messages" ref="chatMessages">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                  <div class="message-content">
                    <div class="message-bubble" :class="{ typing: message.typing }">
                      <div v-if="message.typing" class="typing-indicator">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                      </div>
                      <div class="text">{{ message.content }}</div>
                      <span class="time">{{ message.time }}</span>
                    </div>
                  </div>
                </div>
                <!-- 添加 AI 正在输入的提示 -->
                <div v-if="isAiTyping" class="message assistant">
                  <div class="message-content">
                    <div class="message-bubble typing">
                      <div class="typing-indicator">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                      </div>
                      <div class="typing-text">正在挖掘心里的小九九...</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="emotion-sidebar">
                <div class="emotion-status" :class="{ animate: isStatusAnimating }">
                  <h4>当前情绪状态</h4>
                  <div class="emotion-icon" :class="{ animate: isIconAnimating }">
                    <i :class="currentEmotion.icon"></i>
                  </div>
                  <p class="emotion-text">{{ currentEmotion.text }}</p>
                </div>
                <div class="emotion-chart" :class="{ animate: isChartAnimating }">
                  <h4>情绪波动</h4>
                  <canvas ref="emotionChart"></canvas>
                </div>
              </div>
            </div>
            <div class="input-area">
              <div class="input-wrapper">
                <textarea 
                  v-model="userInput"
                  @keyup.enter="sendMessage"
                  placeholder="你今天有什么困惑吗..."
                  rows="3"
                ></textarea>
                <button class="send-btn" @click="sendMessage">
                  发送 <i class="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="currentTab==='assessment'">
          <div class="chat-container">
            <div class="particles">
              <div v-for="n in 50" :key="n" class="particle"></div>
            </div>
            <div class="light-beams">
              <div v-for="n in 5" :key="n" class="beam"></div>
            </div>
            <div class="floating-elements">
              <div v-for="n in 12" :key="n" class="floating-element">
                <i :class="['fas', getFloatingIcon(n)]"></i>
              </div>
            </div>
            <div class="chat-header">
              <div class="therapist-info">
                <div class="avatar" @click="handleAssessmentClick" :class="{ clicked: isAssessmentClicked }">
                  <i class="fas fa-clipboard-check"></i>
                </div>
                <div class="info">
                  <h3>心理评估</h3>
                  <p class="subtitle">专业评估，科学指导</p>
                </div>
              </div>
              <transition name="assessment-popup">
                <div v-if="showAssessmentOptions" class="assessment-options">
                  <div class="option-item" @click="selectAssessment('PHQ-9')">
                    <i class="fas fa-file-medical"></i>
                    <span>PHQ-9 抑郁筛查</span>
                  </div>
                  <div class="option-item" @click="selectAssessment('GAD-7')">
                    <i class="fas fa-brain"></i>
                    <span>GAD-7 焦虑筛查</span>
                  </div>
                </div>
              </transition>
            </div>
            <div class="chat-layout">
              <div class="chat-messages" ref="assessmentMessages">
                <div v-for="(message, index) in assessmentMessages" :key="index" :class="['message', message.role]">
                  <div class="message-content">
                    <div class="message-bubble">
                      <div class="text">{{ message.content }}</div>
                      <span class="time">{{ message.time }}</span>
                    </div>
                  </div>
                </div>
                <!-- 添加评估界面的 AI 正在输入提示 -->
                <div v-if="isAssessmentTyping" class="message assistant">
                  <div class="message-content">
                    <div class="message-bubble typing assessment-typing">
                      <div class="typing-indicator">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                      </div>
                      <div class="typing-text">正在挖掘心里的小九九...</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="assessment-sidebar">
                <div class="assessment-progress">
                  <h4>评估进度</h4>
                  <div class="progress-bar">
                    <div class="progress" :style="{ width: assessmentProgress + '%' }"></div>
                  </div>
                  <p class="progress-text">{{ assessmentProgress }}%</p>
                </div>
                <div class="assessment-status">
                  <h4>当前状态</h4>
                  <div class="status-content">
                    <i :class="getStatusIcon()"></i>
                    <p>{{ assessmentStatus }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="input-area">
              <div class="input-wrapper">
                <textarea 
                  v-model="assessmentInput"
                  @keyup.enter="sendAssessmentMessage"
                  placeholder="请输入你的回答..."
                  rows="3"
                ></textarea>
                <button class="send-btn" @click="sendAssessmentMessage">
                  提交 <i class="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="currentTab==='science'">
          <div class="feature-placeholder">心理科普功能开发中...</div>
        </div>
      </main>
    </div>
    <transition name="bubble-float">
      <div v-if="showReportBubble" class="report-bubble">
        <span>你的专属心理报告正在生成，请不要离开哦</span>
      </div>
    </transition>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import { defineComponent, onMounted, ref } from 'vue';
import dailyQuotes from './daily_quotes.json'; // 导入鸡汤语录
import { PHQ9 } from './assessments/phq9';

Chart.register(...registerables);

export default defineComponent({
  name: 'App',
  data() {
    return {
      messages: [],
      userInput: '',
      sessionId: null,
      currentEmotion: {
        icon: 'fas fa-smile',
        text: '平静'
      },
      emotionHistory: [],
      emotionChart: null,
      isHeartClicked: false,
      isStatusAnimating: false,
      isIconAnimating: false,
      isChartAnimating: false,
      currentQuote: '', // 当前显示的鸡汤语录
      currentTab: 'station',
      sidebarVisible: false,
      isAiTyping: false,
      assessmentMessages: [],
      assessmentInput: '',
      isAssessmentTyping: false,
      showAssessmentOptions: false,
      isAssessmentClicked: false,
      assessmentProgress: 0,
      assessmentStatus: '等待开始评估',
      currentAssessment: null,
      currentQuestionIndex: 0,
      assessmentAnswers: [],
      assessmentState: 'welcome', // welcome, questioning, summary, chat
      assessmentContext: [], // 存储评估过程中的对话上下文
      currentQuestion: null,
      assessmentSummary: null,
      showReportBubble: false,
    }
  },
  mounted() {
    this.initEmotionChart();
    this.setRandomQuote();
  },
  methods: {
    initEmotionChart() {
      const ctx = this.$refs.emotionChart.getContext('2d');
      this.emotionChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: '情绪值',
            data: [],
            borderColor: '#2C3E50',
            tension: 0.4,
            fill: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    },
    updateEmotionChart(emotion) {
      const now = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      this.emotionHistory.push({ time: now, value: emotion.value });
      
      if (this.emotionHistory.length > 10) {
        this.emotionHistory.shift();
      }

      this.emotionChart.data.labels = this.emotionHistory.map(h => h.time);
      this.emotionChart.data.datasets[0].data = this.emotionHistory.map(h => h.value);
      this.emotionChart.update();
    },
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
      
      // 显示AI正在输入的提示
      this.isAiTyping = true
      
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
        
        // 隐藏AI正在输入的提示
        this.isAiTyping = false
        
        this.messages.push({
          role: 'assistant',
          content: data.response,
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        })
        
        // 更新情绪状态
        if (data.emotion) {
          this.currentEmotion = {
            icon: this.getEmotionIcon(data.emotion.value),
            text: data.emotion.text
          };
          this.updateEmotionChart(data.emotion);
        }
      } catch (error) {
        console.error('Error:', error)
        this.isAiTyping = false
      }
    },
    getEmotionIcon(value) {
      if (value >= 80) return 'fas fa-laugh-beam';
      if (value >= 60) return 'fas fa-smile';
      if (value >= 40) return 'fas fa-meh';
      if (value >= 20) return 'fas fa-frown';
      return 'fas fa-sad-tear';
    },
    getFloatingIcon(index) {
      const icons = [
        'fa-heart',
        'fa-star',
        'fa-cloud',
        'fa-moon',
        'fa-sun',
        'fa-music',
        'fa-feather',
        'fa-butterfly',
        'fa-sparkles',
        'fa-rainbow',
        'fa-flower',
        'fa-bird'
      ];
      return icons[index % icons.length];
    },
    handleHeartClick() {
      this.isHeartClicked = true;
      
      // 添加情绪值
      const currentValue = this.emotionHistory.length > 0 
        ? this.emotionHistory[this.emotionHistory.length - 1].value 
        : 50;
      const newValue = Math.min(currentValue + 10, 100);
      
      // 更新情绪状态
      this.updateEmotionChart({ value: newValue });
      
      // 更新情绪图标
      this.currentEmotion = {
        icon: this.getEmotionIcon(newValue),
        text: this.getEmotionText(newValue)
      };

      // 触发动画
      this.triggerAnimations();

      // 重置点击状态
      setTimeout(() => {
        this.isHeartClicked = false;
      }, 800);
    },
    getEmotionText(value) {
      if (value >= 80) return '非常开心';
      if (value >= 60) return '开心';
      if (value >= 40) return '平静';
      if (value >= 20) return '低落';
      return '难过';
    },
    triggerAnimations() {
      // 触发状态栏动画
      this.isStatusAnimating = true;
      setTimeout(() => {
        this.isStatusAnimating = false;
      }, 1000);

      // 触发图标动画
      this.isIconAnimating = true;
      setTimeout(() => {
        this.isIconAnimating = false;
      }, 1000);

      // 触发图表动画
      this.isChartAnimating = true;
      setTimeout(() => {
        this.isChartAnimating = false;
      }, 1000);
    },
    setRandomQuote() {
      const idx = Math.floor(Math.random() * dailyQuotes.length);
      this.currentQuote = dailyQuotes[idx];
    },
    changeQuote() {
      let idx;
      do {
        idx = Math.floor(Math.random() * dailyQuotes.length);
      } while (dailyQuotes[idx] === this.currentQuote && dailyQuotes.length > 1);
      this.currentQuote = dailyQuotes[idx];
    },
    switchTab(tab) {
      this.currentTab = tab;
      this.sidebarVisible = false;
    },
    handleAssessmentClick() {
      this.isAssessmentClicked = !this.isAssessmentClicked;
      this.showAssessmentOptions = !this.showAssessmentOptions;
    },
    selectAssessment(type) {
      if (type === 'PHQ-9') {
        const now = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        // 生动专业欢迎词
        const welcome = `欢迎来到PHQ-9抑郁自评小测！🌸\n在这里，你可以用最真实的心情和我聊聊。每个人都会有情绪波动的时候，这很正常。\n接下来我会陪你一起完成9个小问题，请你根据过去两周的真实感受，选择最符合的选项。\n请相信，这里没有对错，也没有评判，只有理解和陪伴。你的每一个答案，都是对自己的一次关心。准备好了吗？我们马上开始！`;
        this.assessmentMessages = [{
          role: 'assistant',
          content: welcome,
          time: now
        }];
        this.currentAssessment = PHQ9;
        this.currentQuestionIndex = 0;
        this.assessmentAnswers = [];
        this.assessmentState = 'questioning';
        this.assessmentStatus = '评估进行中';
        this.assessmentProgress = 0;
        // 发送第一题
        setTimeout(() => {
          this.askNextAssessmentQuestion();
        }, 1200);
      }
      this.showAssessmentOptions = false; // 选择后自动收起下拉
    },
    askNextAssessmentQuestion() {
      const q = this.currentAssessment.questions[this.currentQuestionIndex];
      const optionsText = q.options.map((o, i) => `${i + 1}. ${o.text}`).join('  ');
      const now = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      this.assessmentMessages.push({
        role: 'assistant',
        content: `第${q.id}题：${q.text}\n选项：${optionsText}`,
        time: now
      });
    },
    async sendAssessmentMessage() {
      if (!this.assessmentInput.trim() || !this.currentAssessment) return;
      const now = new Date();
      const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      const userMessage = {
        role: 'user',
        content: this.assessmentInput,
        time: time
      };
      this.assessmentMessages.push(userMessage);
      // 轮答：校验并记录答案
      const q = this.currentAssessment.questions[this.currentQuestionIndex];
      const answer = this.assessmentInput.trim();
      let matched = null;
      const idx = parseInt(answer, 10);
      if (!isNaN(idx) && idx >= 1 && idx <= q.options.length) {
        matched = q.options[idx - 1];
      } else {
        matched = q.options.find(opt => opt.text === answer);
      }
      if (matched) {
        this.assessmentAnswers.push({
          questionId: q.id,
          value: matched.value,
          text: matched.text
        });
        this.assessmentProgress = Math.round((this.currentQuestionIndex + 1) / this.currentAssessment.questions.length * 100);
        if (this.currentQuestionIndex < this.currentAssessment.questions.length - 1) {
          this.currentQuestionIndex++;
          this.assessmentInput = '';
          setTimeout(() => {
            this.askNextAssessmentQuestion();
          }, 600);
        } else {
          // 评估结束
          this.assessmentState = 'finished';
          this.assessmentStatus = '评估已完成';
          this.assessmentProgress = 100;
          this.assessmentInput = '';
          // 优化结束词
          const finishMsg = {
            role: 'assistant',
            content: '🎉 恭喜你完成了PHQ-9抑郁自评量表的全部题目！你的每一个答案都像一颗小星星，照亮了你内心的世界。感谢你信任地分享自己的感受，这本身就是一种勇敢和自我关怀。无论分数如何，你都值得被理解和支持。接下来，我会为你梳理和分析刚才的答题信息，给出温暖、专业的反馈。之后你可以随时和我自由交流，无论是聊聊心情、生活，还是有任何困惑，我都会耐心聆听，陪伴你前行。',
            time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
          };
          this.assessmentMessages.push(finishMsg);
          // 1. 打包用户信息为prompt
          const mood = this.assessmentMessages.find(msg => msg.role === 'user');
          let intro = '';
          if (mood) {
            intro = `用户在欢迎阶段的心情描述：${mood.content}\n`;
          }
          let qa = this.currentAssessment.questions.map((q, idx) => {
            const ans = this.assessmentAnswers[idx];
            return `${idx + 1}. ${q.text}：${ans ? ans.text : ''}`;
          }).join('\n');
          const summaryPrompt = `${intro}以下是用户的PHQ-9答题情况：\n${qa}\n请用温暖、生动、专业的语言为用户做一个心理状态总结和打分分析。`;
          // 2. 显示气泡提示
          this.showReportBubble = true;
          // 3. 切换为心理驿站模式并调用AI分析
          setTimeout(async () => {
            this.currentTab = 'station';
            this.messages = [...this.messages, ...this.assessmentMessages];
            // 先推送动态打字气泡"正在挖掘心里的小九九..."
            const typingBubble = {
              role: 'assistant',
              typing: true,
              content: '正在挖掘心里的小九九...',
              time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
            };
            this.messages.push(typingBubble);
            // 调用AI生成总结
            const aiRes = await fetch('http://localhost:8000/api/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                message: summaryPrompt,
                session_id: this.sessionId
              })
            });
            const aiData = await aiRes.json();
            if (aiData.session_id) {
              this.sessionId = aiData.session_id;
            }
            const summaryMessage = aiData.response || '评估总结已生成。如需进一步交流，请随时告诉我。';
            // 替换动态气泡为正式总结
            const idx = this.messages.findIndex(m => m === typingBubble);
            if (idx !== -1) {
              this.messages.splice(idx, 1, {
                role: 'assistant',
                content: summaryMessage,
                time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
              });
            } else {
              this.messages.push({
                role: 'assistant',
                content: summaryMessage,
                time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
              });
            }
            // 4. 隐藏气泡
            this.showReportBubble = false;
          }, 1800);
        }
      } else {
        // 错误提示
        const errMsg = {
          role: 'assistant',
          content: '啊，我们不是在进行心理评估吗？我还没明白你的选择呢～请再试一次吧！直接输入选项前的数字或完整内容就好哦：' + q.options.map((o, i) => `${i + 1}. ${o.text}`).join('  '),
          time: time
        };
        this.assessmentMessages.push(errMsg);
      }
    },
    formatOptions(options) {
      // 返回带序号的选项字符串
      return options.map((opt, idx) => `${idx + 1}. ${opt.text}`).join('  ');
    },
    parseOptionInput(input, options) {
      // 支持数字或文本
      const trimmed = input.trim();
      // 数字（1~N）
      const idx = parseInt(trimmed, 10);
      if (!isNaN(idx) && idx >= 1 && idx <= options.length) {
        return options[idx - 1];
      }
      // 文本匹配
      return options.find(opt => opt.text === trimmed);
    },
    buildPhq9SummaryPrompt() {
      // 精简：只保留心情描述、每题序号+题干+用户答案，合并为一条user消息
      let intro = '';
      const mood = this.assessmentContext.find(msg => msg.role === 'user');
      if (mood) {
        intro = `用户在欢迎阶段的心情描述：${mood.content}\n`;
      }
      let qa = this.currentAssessment.questions.map((q, idx) => {
        const ans = this.assessmentAnswers[idx];
        // 题干只保留前15字
        const shortQ = q.text.replace(/\n/g, '').slice(0, 15) + (q.text.length > 15 ? '...' : '');
        return `${idx + 1}. ${shortQ}：${ans ? ans.text : ''}`;
      }).join('\n');
      return `${intro}以下是用户的PHQ-9答题情况：\n${qa}\n请用温暖、生动、专业的语言为用户做一个心理状态总结和打分分析。`;
    },
    getRecommendations(level) {
      if (level === '轻度抑郁') {
        return this.currentAssessment.recommendations.mild;
      } else if (level === '中度抑郁') {
        return this.currentAssessment.recommendations.moderate;
      } else if (level === '重度抑郁' || level === '中重度抑郁') {
        return this.currentAssessment.recommendations.severe;
      }
      return null;
    },
    getStatusIcon() {
      if (this.assessmentState === 'welcome') {
        return 'fas fa-comments';
      } else if (this.assessmentState === 'questioning') {
        return 'fas fa-spinner fa-spin';
      } else if (this.assessmentState === 'chat') {
        return 'fas fa-heart';
      }
      return 'fas fa-clipboard-check';
    }
  }
})
</script>

<style>
:root {
  --primary-color: #ffb6c1;
  --secondary-color: #2C3E50;
  --background-color: #fff5f6;
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
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.app-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, 
    rgba(255, 248, 250, 0.95),
    rgba(255, 228, 232, 0.95),
    rgba(255, 240, 245, 0.95)
  );
  overflow: hidden;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
  opacity: 0.5;
  animation: float 15s infinite linear;
}

.particle:nth-child(odd) {
  width: 4px;
  height: 4px;
  animation-duration: 20s;
}

.particle:nth-child(3n) {
  width: 8px;
  height: 8px;
  animation-duration: 25s;
}

.particle:nth-child(3n+1) {
  width: 5px;
  height: 5px;
  animation-duration: 18s;
}

@keyframes float {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.5;
  }
  90% {
    opacity: 0.5;
  }
  100% {
    transform: translateY(-100vh) translateX(100vw) rotate(360deg);
    opacity: 0;
  }
}

/* 为每个粒子设置不同的起始位置和动画延迟 */
.particle:nth-child(1) { left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { left: 20%; animation-delay: 2s; }
.particle:nth-child(3) { left: 30%; animation-delay: 4s; }
.particle:nth-child(4) { left: 40%; animation-delay: 6s; }
.particle:nth-child(5) { left: 50%; animation-delay: 8s; }
.particle:nth-child(6) { left: 60%; animation-delay: 10s; }
.particle:nth-child(7) { left: 70%; animation-delay: 12s; }
.particle:nth-child(8) { left: 80%; animation-delay: 14s; }
.particle:nth-child(9) { left: 90%; animation-delay: 16s; }
.particle:nth-child(10) { left: 15%; animation-delay: 18s; }
.particle:nth-child(11) { left: 25%; animation-delay: 20s; }
.particle:nth-child(12) { left: 35%; animation-delay: 22s; }
.particle:nth-child(13) { left: 45%; animation-delay: 24s; }
.particle:nth-child(14) { left: 55%; animation-delay: 26s; }
.particle:nth-child(15) { left: 65%; animation-delay: 28s; }
.particle:nth-child(16) { left: 75%; animation-delay: 30s; }
.particle:nth-child(17) { left: 85%; animation-delay: 32s; }
.particle:nth-child(18) { left: 95%; animation-delay: 34s; }
.particle:nth-child(19) { left: 5%; animation-delay: 36s; }
.particle:nth-child(20) { left: 15%; animation-delay: 38s; }
.particle:nth-child(21) { left: 25%; animation-delay: 40s; }
.particle:nth-child(22) { left: 35%; animation-delay: 42s; }
.particle:nth-child(23) { left: 45%; animation-delay: 44s; }
.particle:nth-child(24) { left: 55%; animation-delay: 46s; }
.particle:nth-child(25) { left: 65%; animation-delay: 48s; }
.particle:nth-child(26) { left: 75%; animation-delay: 50s; }
.particle:nth-child(27) { left: 85%; animation-delay: 52s; }
.particle:nth-child(28) { left: 95%; animation-delay: 54s; }
.particle:nth-child(29) { left: 5%; animation-delay: 56s; }
.particle:nth-child(30) { left: 15%; animation-delay: 58s; }
.particle:nth-child(31) { left: 25%; animation-delay: 60s; }
.particle:nth-child(32) { left: 35%; animation-delay: 62s; }
.particle:nth-child(33) { left: 45%; animation-delay: 64s; }
.particle:nth-child(34) { left: 55%; animation-delay: 66s; }
.particle:nth-child(35) { left: 65%; animation-delay: 68s; }
.particle:nth-child(36) { left: 75%; animation-delay: 70s; }
.particle:nth-child(37) { left: 85%; animation-delay: 72s; }
.particle:nth-child(38) { left: 95%; animation-delay: 74s; }
.particle:nth-child(39) { left: 5%; animation-delay: 76s; }
.particle:nth-child(40) { left: 15%; animation-delay: 78s; }
.particle:nth-child(41) { left: 25%; animation-delay: 80s; }
.particle:nth-child(42) { left: 35%; animation-delay: 82s; }
.particle:nth-child(43) { left: 45%; animation-delay: 84s; }
.particle:nth-child(44) { left: 55%; animation-delay: 86s; }
.particle:nth-child(45) { left: 65%; animation-delay: 88s; }
.particle:nth-child(46) { left: 75%; animation-delay: 90s; }
.particle:nth-child(47) { left: 85%; animation-delay: 92s; }
.particle:nth-child(48) { left: 95%; animation-delay: 94s; }
.particle:nth-child(49) { left: 5%; animation-delay: 96s; }
.particle:nth-child(50) { left: 15%; animation-delay: 98s; }

/* 调整其他元素的 z-index，确保在粒子效果之上 */
.header, .main-content {
  position: relative;
  z-index: 2;
}

.header {
  padding: 20px 0;
  margin-bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 2;
}

.logo {
  text-align: center;
  position: relative;
  padding: 0 20px;
}

.logo::before,
.logo::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent,
    rgba(255, 182, 193, 0.6),
    rgba(255, 209, 220, 0.8),
    rgba(255, 182, 193, 0.6),
    transparent
  );
  animation: shimmer 3s infinite linear;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.logo::before {
  left: -100px;
  background-size: 200% 100%;
}

.logo::after {
  right: -100px;
  background-size: 200% 100%;
}

.logo h1 {
  font-size: 2.8em;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
  text-shadow: 
    2px 2px 4px rgba(0, 0, 0, 0.1),
    0 0 20px rgba(255, 182, 193, 0.3),
    0 0 40px rgba(255, 182, 193, 0.2),
    0 0 60px rgba(255, 182, 193, 0.1);
  letter-spacing: 3px;
  position: relative;
  display: inline-block;
  animation: glow 3s infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 
      2px 2px 4px rgba(0, 0, 0, 0.1),
      0 0 20px rgba(255, 182, 193, 0.3),
      0 0 40px rgba(255, 182, 193, 0.2),
      0 0 60px rgba(255, 182, 193, 0.1);
  }
  to {
    text-shadow: 
      2px 2px 4px rgba(0, 0, 0, 0.1),
      0 0 30px rgba(255, 182, 193, 0.4),
      0 0 50px rgba(255, 182, 193, 0.3),
      0 0 70px rgba(255, 182, 193, 0.2);
  }
}

.logo h1::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg,
    transparent,
    var(--primary-color),
    rgba(255, 209, 220, 0.8),
    var(--primary-color),
    transparent
  );
  animation: shimmer 3s infinite linear;
  background-size: 200% 100%;
}

.subtitle {
  font-size: 1.1em;
  color: var(--secondary-color);
  margin: 12px 0 0 0;
  opacity: 0.9;
  font-weight: 400;
  letter-spacing: 2px;
  text-shadow: 
    1px 1px 2px rgba(0, 0, 0, 0.05),
    0 0 10px rgba(255, 182, 193, 0.2);
  position: relative;
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.8),
    rgba(255, 248, 250, 0.8)
  );
  border-radius: 20px;
  box-shadow: 
    0 4px 15px rgba(255, 182, 193, 0.2),
    0 1px 3px rgba(255, 182, 193, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(5px);
  transform: translateY(0);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: subtitle-float 3s infinite ease-in-out;
}

@keyframes subtitle-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.subtitle::before,
.subtitle::after {
  content: '';
  position: absolute;
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255, 182, 193, 0.3);
  border-radius: 50%;
  animation: subtitle-sparkle 2s infinite ease-in-out;
}

.subtitle::before {
  top: -5px;
  left: -5px;
  animation-delay: 0s;
}

.subtitle::after {
  bottom: -5px;
  right: -5px;
  animation-delay: 1s;
}

@keyframes subtitle-sparkle {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.6;
  }
}

/* 聊天头部副标题样式 */
.therapist-info .subtitle {
  position: relative;
  top: auto;
  right: auto;
  margin: 5px 0 0 0;
  font-size: 0.95em;
  padding: 6px 15px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.9),
    rgba(255, 248, 250, 0.9)
  );
  color: var(--primary-color);
  letter-spacing: 1.5px;
  text-shadow: 
    1px 1px 2px rgba(0, 0, 0, 0.05),
    0 0 8px rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 4px 12px rgba(255, 182, 193, 0.15),
    0 1px 2px rgba(255, 182, 193, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.4);
  animation: subtitle-float-small 3s infinite ease-in-out;
}

@keyframes subtitle-float-small {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

.therapist-info .subtitle::before,
.therapist-info .subtitle::after {
  width: 10px;
  height: 10px;
  border-width: 1.5px;
}

/* 优化粉色部分的线条效果 */
.chat-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 25%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0.1) 75%,
    transparent 100%
  );
  animation: shimmer-line 3s infinite linear;
  pointer-events: none;
}

.chat-header::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(255, 255, 255, 0.2) 0%,
    transparent 70%
  );
  animation: pulse-glow 4s infinite ease-in-out;
  pointer-events: none;
}

@keyframes shimmer-line {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

/* 添加装饰性波浪线 */
.chat-header .wave-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.5),
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: wave-move 3s infinite linear;
}

@keyframes wave-move {
  0% {
    background-position: 0% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .therapist-info .subtitle {
    position: relative;
    top: auto;
    right: auto;
    margin-top: 10px;
    font-size: 0.9em;
    padding: 5px 12px;
  }

  .chat-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 0;
  box-shadow: none;
  min-height: calc(100vh - 80px);
  border: none;
  position: relative;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, var(--primary-color), #ffc0cb);
  color: white;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.therapist-info {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
}

.avatar {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5em;
  color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
}

.avatar:active {
  transform: scale(0.95);
}

.avatar i {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.avatar.clicked i {
  animation: heart-beat 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  color: #ff4d6d;
}

@keyframes heart-beat {
  0% {
    transform: scale(1);
  }
  15% {
    transform: scale(1.4);
  }
  30% {
    transform: scale(1);
  }
  45% {
    transform: scale(1.4);
  }
  60% {
    transform: scale(1);
  }
  75% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.avatar::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, 
    rgba(255, 182, 193, 0.4) 0%,
    rgba(255, 182, 193, 0.2) 30%,
    transparent 70%
  );
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.avatar.clicked::after {
  animation: ripple 1s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes ripple {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.8;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    transform: translate(-50%, -50%) scale(2.5);
    opacity: 0;
  }
}

.chat-layout {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
  position: relative;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: transparent;
  min-width: 0;
  scroll-behavior: smooth;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 85%;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  align-self: flex-end;
}

.message-bubble {
  background: white;
  padding: 15px 20px;
  border-radius: 20px;
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  word-break: break-word;
  transform-origin: center;
  animation: message-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@keyframes message-pop {
  0% {
    transform: scale(0.8) translateY(20px);
    opacity: 0;
  }
  50% {
    transform: scale(1.05) translateY(-5px);
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #ffb6c1, #ffc0cb);
  color: white;
  box-shadow: 
    0 4px 15px rgba(255, 182, 193, 0.3),
    0 1px 3px rgba(255, 182, 193, 0.2);
  animation: message-pop-user 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes message-pop-user {
  0% {
    transform: scale(0.8) translateY(20px);
    opacity: 0;
  }
  50% {
    transform: scale(1.05) translateY(-5px);
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.emotion-sidebar {
  width: 240px;
  background: rgba(255, 255, 255, 0.75);
  border-left: 1px solid rgba(255, 255, 255, 0.3);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.emotion-status {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transform-origin: center;
  cursor: pointer;
}

.emotion-status:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(255, 182, 193, 0.2),
    0 4px 10px rgba(255, 182, 193, 0.1);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 182, 193, 0.4);
}

.emotion-status:hover .emotion-icon {
  transform: scale(1.1);
  text-shadow: 0 0 20px rgba(255, 182, 193, 0.5);
}

.emotion-status:hover .emotion-text {
  color: #ff4d6d;
  transform: translateY(-2px);
}

.emotion-status.animate {
  animation: status-pulse 1s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes status-pulse {
  0% {
    transform: scale(1);
  }
  20% {
    transform: scale(1.05);
  }
  40% {
    transform: scale(0.98);
  }
  60% {
    transform: scale(1.02);
  }
  80% {
    transform: scale(0.99);
  }
  100% {
    transform: scale(1);
  }
}

.emotion-icon {
  font-size: 2.2em;
  margin: 10px 0;
  color: var(--primary-color);
  animation: pulse 2s infinite;
  text-shadow: 0 0 15px rgba(255, 182, 193, 0.3);
  transform-origin: center;
}

.emotion-icon.animate {
  animation: icon-bounce 1s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes icon-bounce {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.3) rotate(-10deg);
  }
  50% {
    transform: scale(0.9) rotate(10deg);
  }
  75% {
    transform: scale(1.1) rotate(-5deg);
  }
  100% {
    transform: scale(1) rotate(0);
  }
}

.emotion-text {
  font-size: 0.95em;
  color: var(--primary-color);
  margin: 8px 0 0 0;
  font-weight: 500;
  letter-spacing: 1px;
}

.emotion-chart {
  flex: 1;
  min-height: 160px;
  max-height: 200px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 15px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transform-origin: center;
  cursor: pointer;
}

.emotion-chart:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(255, 182, 193, 0.2),
    0 4px 10px rgba(255, 182, 193, 0.1);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 182, 193, 0.4);
}

.emotion-chart:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 182, 193, 0.1),
    transparent
  );
  animation: chart-shine 1.5s infinite;
}

@keyframes chart-shine {
  0% {
    transform: translateX(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) rotate(45deg);
  }
}

.emotion-chart:hover h4 {
  color: #ff4d6d;
  transform: translateY(-2px);
}

.emotion-chart h4 {
  transition: all 0.3s ease;
  margin: 0 0 10px 0;
  color: var(--primary-color);
}

.emotion-chart.animate {
  animation: chart-wave 1s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes chart-wave {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.02) translateY(-2px);
  }
  50% {
    transform: scale(0.98) translateY(2px);
  }
  75% {
    transform: scale(1.01) translateY(-1px);
  }
  100% {
    transform: scale(1) translateY(0);
  }
}

.input-area {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 
    0 -8px 20px rgba(0, 0, 0, 0.05),
    0 -2px 5px rgba(0, 0, 0, 0.02);
  position: relative;
  z-index: 2;
}

.input-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

textarea {
  width: 100%;
  padding: 15px 20px;
  border: 2px solid rgba(255, 182, 193, 0.3);
  border-radius: 20px;
  resize: none;
  font-family: inherit;
  font-size: 1.05em;
  line-height: 1.6;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.03),
    0 1px 3px rgba(0, 0, 0, 0.05);
  color: var(--text-color);
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
}

textarea::placeholder {
  color: rgba(44, 62, 80, 0.5);
  font-style: italic;
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 
    0 0 0 3px rgba(255, 182, 193, 0.2),
    0 8px 20px rgba(0, 0, 0, 0.05);
  background: white;
  transform: translateY(-1px);
}

.send-btn {
  padding: 12px 28px;
  border: none;
  border-radius: 20px;
  background: linear-gradient(135deg, var(--primary-color), #ffc0cb);
  color: white;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.95em;
  align-self: flex-end;
  box-shadow: 
    0 4px 15px rgba(255, 182, 193, 0.3),
    0 1px 3px rgba(255, 182, 193, 0.2);
}

.send-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(255, 182, 193, 0.4),
    0 2px 5px rgba(255, 182, 193, 0.3);
}

.send-btn:active {
  transform: translateY(0);
  box-shadow: 
    0 2px 10px rgba(255, 182, 193, 0.3),
    0 1px 2px rgba(255, 182, 193, 0.2);
}

/* 响应式布局优化 */
@media (max-width: 768px) {
  .chat-layout {
    padding: 10px;
  }

  .emotion-sidebar {
    width: 100%;
    padding: 15px;
    gap: 15px;
  }

  .emotion-status {
    padding: 15px;
  }

  .emotion-chart {
    min-height: 140px;
    max-height: 160px;
    padding: 12px;
  }

  .floating-element {
    font-size: 20px;
  }

  textarea {
    padding: 12px 15px;
  }

  .send-btn {
    padding: 10px 20px;
  }

  .logo h1 {
    font-size: 2.2em;
  }

  .subtitle {
    font-size: 1em;
  }

  .logo::before,
  .logo::after {
    width: 40px;
  }

  .logo::before {
    left: -60px;
  }

  .logo::after {
    right: -60px;
  }
}

/* 自定义鼠标样式 */
* {
  cursor: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%23ffb6c1'><path d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z'/></svg>") 12 12, auto;
}

/* 流光效果 */
.light-beams {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.beam {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(
    circle at center,
    rgba(255, 182, 193, 0.15),
    rgba(255, 209, 220, 0.2),
    rgba(255, 182, 193, 0.15)
  );
  border-radius: 50%;
  filter: blur(40px);
  animation: float-beam 20s infinite ease-in-out;
  mix-blend-mode: soft-light;
}

.beam:nth-child(1) {
  top: 15%;
  left: 10%;
  animation-delay: 0s;
  width: 400px;
  height: 400px;
  background: radial-gradient(
    circle at center,
    rgba(255, 182, 193, 0.2),
    rgba(255, 209, 220, 0.25),
    rgba(255, 182, 193, 0.2)
  );
}

.beam:nth-child(2) {
  top: 60%;
  left: 70%;
  animation-delay: -7s;
  width: 350px;
  height: 350px;
  background: radial-gradient(
    circle at center,
    rgba(255, 209, 220, 0.2),
    rgba(255, 182, 193, 0.25),
    rgba(255, 209, 220, 0.2)
  );
}

.beam:nth-child(3) {
  top: 40%;
  left: 40%;
  animation-delay: -14s;
  width: 300px;
  height: 300px;
  background: radial-gradient(
    circle at center,
    rgba(255, 182, 193, 0.15),
    rgba(255, 209, 220, 0.2),
    rgba(255, 182, 193, 0.15)
  );
}

.beam:nth-child(4) {
  top: 20%;
  right: 15%;
  animation-delay: -10s;
  width: 250px;
  height: 250px;
  background: radial-gradient(
    circle at center,
    rgba(255, 209, 220, 0.15),
    rgba(255, 182, 193, 0.2),
    rgba(255, 209, 220, 0.15)
  );
}

.beam:nth-child(5) {
  bottom: 10%;
  left: 20%;
  animation-delay: -5s;
  width: 280px;
  height: 280px;
  background: radial-gradient(
    circle at center,
    rgba(255, 182, 193, 0.15),
    rgba(255, 209, 220, 0.2),
    rgba(255, 182, 193, 0.15)
  );
}

@keyframes float-beam {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.3;
  }
  25% {
    transform: translate(100px, 50px) rotate(90deg) scale(1.1);
    opacity: 0.5;
  }
  50% {
    transform: translate(50px, 100px) rotate(180deg) scale(1);
    opacity: 0.3;
  }
  75% {
    transform: translate(-50px, 50px) rotate(270deg) scale(0.9);
    opacity: 0.5;
  }
  100% {
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.3;
  }
}

/* 浮动可爱元素 */
.floating-elements {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.floating-element {
  position: absolute;
  font-size: 24px;
  color: rgba(255, 182, 193, 0.8);
  opacity: 0.6;
  animation: float-element 25s infinite ease-in-out;
  text-shadow: 
    0 0 15px rgba(255, 182, 193, 0.4),
    0 0 30px rgba(255, 182, 193, 0.2);
  filter: drop-shadow(0 0 5px rgba(255, 182, 193, 0.3));
  mix-blend-mode: soft-light;
}

.floating-element:nth-child(1) { color: #ffb6c1; top: 10%; left: 5%; font-size: 28px; animation-delay: 0s; }
.floating-element:nth-child(2) { color: #ffd1dc; top: 20%; right: 10%; font-size: 24px; animation-delay: -2s; }
.floating-element:nth-child(3) { color: #ffc0cb; bottom: 15%; left: 15%; font-size: 32px; animation-delay: -4s; }
.floating-element:nth-child(4) { color: #ffb6c1; bottom: 25%; right: 15%; font-size: 26px; animation-delay: -6s; }
.floating-element:nth-child(5) { color: #ffd1dc; top: 50%; left: 5%; font-size: 30px; animation-delay: -8s; }
.floating-element:nth-child(6) { color: #ffc0cb; top: 40%; right: 5%; font-size: 22px; animation-delay: -10s; }
.floating-element:nth-child(7) { color: #ffb6c1; top: 30%; left: 20%; font-size: 25px; animation-delay: -12s; }
.floating-element:nth-child(8) { color: #ffd1dc; bottom: 40%; right: 20%; font-size: 27px; animation-delay: -14s; }
.floating-element:nth-child(9) { color: #ffc0cb; top: 60%; left: 25%; font-size: 23px; animation-delay: -16s; }
.floating-element:nth-child(10) { color: #ffb6c1; bottom: 30%; right: 25%; font-size: 29px; animation-delay: -18s; }
.floating-element:nth-child(11) { color: #ffd1dc; top: 70%; left: 15%; font-size: 24px; animation-delay: -20s; }
.floating-element:nth-child(12) { color: #ffc0cb; bottom: 20%; right: 10%; font-size: 26px; animation-delay: -22s; }

@keyframes float-element {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.6;
  }
  25% {
    transform: translate(50px, 25px) rotate(90deg) scale(1.1);
    opacity: 0.8;
  }
  50% {
    transform: translate(25px, 50px) rotate(180deg) scale(1);
    opacity: 0.6;
  }
  75% {
    transform: translate(-25px, 25px) rotate(270deg) scale(0.9);
    opacity: 0.8;
  }
  100% {
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.6;
  }
}

/* 优化滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
  opacity: 0.5;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #ff9eb5;
}

/* 鸡汤语录浮动框样式 */
.quote-float-box {
  background: linear-gradient(135deg, #ffb6c1 0%, #ffe4e1 100%);
  border-radius: 24px;
  padding: 28px 20px 18px 20px;
  margin: 32px auto 0 auto;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: float-quote 3.5s ease-in-out infinite;
  position: relative;
  cursor: pointer;
  z-index: 10;
  transition: box-shadow 0.3s;
}
.quote-float-box:hover {
  box-shadow: 0 12px 40px rgba(255,182,193,0.28), 0 4px 16px #ffd6e0;
}

@keyframes float-quote {
  0% { transform: translateY(0px);}
  50% { transform: translateY(-12px);}
  100% { transform: translateY(0px);}
}

.quote-text {
  font-size: 1.25rem;
  color: #d6336c;
  font-family: 'FZYaoti', 'STSong', 'KaiTi', 'Arial', sans-serif;
  text-align: center;
  text-shadow: 0 2px 8px #fff0f6;
  margin-bottom: 10px;
  letter-spacing: 1px;
  line-height: 2;
  user-select: text;
  transition: color 0.5s;
  animation: pop-in 0.7s;
}

@keyframes pop-in {
  0% { opacity: 0; transform: scale(0.8);}
  80% { opacity: 1; transform: scale(1.05);}
  100% { opacity: 1; transform: scale(1);}
}

.change-btn {
  background: #fff0f6;
  color: #d6336c;
  border: none;
  border-radius: 16px;
  padding: 6px 18px;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px #ffd6e0;
  transition: background 0.3s, transform 0.2s;
  margin-top: 2px;
  margin-bottom: 2px;
}
.change-btn:hover {
  background: #ffd6e0;
  transform: scale(1.08) rotate(-2deg);
}

.quote-tip {
  font-size: 0.85em;
  color: #d6336c99;
  margin-top: 2px;
  letter-spacing: 1px;
  user-select: none;
}

.fade-float-enter-active, .fade-float-leave-active {
  transition: opacity 0.5s;
}
.fade-float-enter-from, .fade-float-leave-to {
  opacity: 0;
}

/* 聊天头部右侧鸡汤语录样式 */
.header-quote-box {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  max-width: 420px;
  min-width: 180px;
  background: rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 10px 18px 10px 18px;
  box-shadow: 0 2px 12px rgba(255,182,193,0.10);
  animation: float-quote 3.5s ease-in-out infinite;
}

.header-quote-text {
  font-size: 1.08rem;
  color: #d6336c;
  font-family: 'FZYaoti', 'STSong', 'KaiTi', 'Arial', sans-serif;
  text-align: left;
  text-shadow: 0 2px 8px #fff0f6;
  letter-spacing: 1px;
  line-height: 1.7;
  user-select: text;
  transition: color 0.5s;
  animation: pop-in 0.7s;
  max-width: 320px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-quote-btn {
  background: #fff0f6;
  color: #d6336c;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 2px 8px #ffd6e0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s, transform 0.2s;
  margin-left: 4px;
}
.header-quote-btn:hover {
  background: #ffd6e0;
  transform: scale(1.12) rotate(-8deg);
}

@keyframes float-quote {
  0% { transform: translateY(0px);}
  50% { transform: translateY(-6px);}
  100% { transform: translateY(0px);}
}

@keyframes pop-in {
  0% { opacity: 0; transform: scale(0.8);}
  80% { opacity: 1; transform: scale(1.05);}
  100% { opacity: 1; transform: scale(1);}
}

/* 响应式优化 */
@media (max-width: 768px) {
  .header-quote-box {
    max-width: 180px;
    min-width: 80px;
    padding: 6px 8px;
  }
  .header-quote-text {
    font-size: 0.92rem;
    max-width: 100px;
  }
  .header-quote-btn {
    width: 28px;
    height: 28px;
    font-size: 1rem;
  }
}

/* 仅显示箭头，弹出菜单浮层 */
.sidebar-arrow-container {
  position: fixed;
  top: 60px;
  left: 0;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.sidebar-arrow-btn {
  background: #fff0f6;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  color: #d6336c;
  box-shadow: 0 2px 8px #ffd6e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
  cursor: pointer;
  margin-left: 4px;
  margin-bottom: 6px;
  transition: background 0.3s;
}
.sidebar-arrow-btn:hover {
  background: #ffd6e0;
}
.sidebar-popup {
  position: absolute;
  left: 40px;
  top: 0;
  background: linear-gradient(135deg, #fff0f6 0%, #ffd6e0 100%);
  border-radius: 18px;
  box-shadow: 2px 4px 24px 0 rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  padding: 12px 0;
  min-width: 120px;
  margin-top: 0;
  animation: dropdown-pop 0.3s;
  z-index: 1001;
}
@keyframes dropdown-pop {
  0% { transform: scale(0.8) translateY(-10px); opacity: 0;}
  100% { transform: scale(1) translateY(0); opacity: 1;}
}
.sidebar-popup ul {
  list-style: none;
  padding: 0 10px;
  margin: 0;
}
.sidebar-popup li {
  display: flex;
  align-items: center;
  color: #d6336c;
  font-size: 0.98em;
  cursor: pointer;
  border-radius: 12px;
  padding: 8px 10px;
  margin-bottom: 4px;
  transition: background 0.2s, color 0.2s;
  font-family: 'ZCOOL KuaiLe', 'FZYaoti', 'STSong', 'KaiTi', 'Arial', sans-serif;
  letter-spacing: 1px;
  position: relative;
}
.sidebar-popup li.active,
.sidebar-popup li:hover {
  background: #ffe4ec;
  color: #ff69b4;
  font-weight: bold;
}
.sidebar-popup i {
  font-size: 1.1em;
  margin-right: 8px;
  transition: color 0.2s;
}
.sidebar-popup span {
  font-size: 0.98em;
  user-select: none;
}
.sidebar-fade-enter-active, .sidebar-fade-leave-active {
  transition: opacity 0.2s;
}
.sidebar-fade-enter-from, .sidebar-fade-leave-to {
  opacity: 0;
}

.main-content-full {
  margin-left: 0;
  width: 100vw;
  box-sizing: border-box;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 0;
  background: transparent;
}
@media (max-width: 768px) {
  .sidebar-arrow-container {
    top: 10px;
  }
  .sidebar-arrow-btn {
    width: 24px;
    height: 24px;
    font-size: 1em;
    margin-left: 0;
  }
  .sidebar-popup {
    left: 28px;
    min-width: 90px;
    padding: 6px 0;
  }
  .sidebar-popup li {
    font-size: 0.85em;
    padding: 6px 8px;
  }
  .main-content-full {
    margin-left: 0;
    width: 100vw;
    min-width: 0;
    padding: 0;
  }
}

/* 添加打字动画样式 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  background: #2C3E50;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator .dot:nth-child(1) { animation-delay: 0s; }
.typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-4px); }
}

.typing-text {
  color: #666;
  font-size: 0.9em;
  font-style: italic;
}

/* 评估界面样式 */
.assessment-options {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  background: linear-gradient(135deg, #fff0f6 0%, #ffd6e0 100%);
  border-radius: 18px;
  box-shadow: 2px 4px 24px 0 rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  padding: 12px 0;
  min-width: 180px;
  z-index: 100;
  animation: dropdown-pop 0.3s;
}

.assessment-options::before {
  content: '';
  position: absolute;
  top: -8px;
  left: 20px;
  width: 16px;
  height: 16px;
  background: linear-gradient(135deg, #fff0f6 0%, #ffd6e0 100%);
  transform: rotate(45deg);
  box-shadow: -2px -2px 5px rgba(255,182,193,0.1);
}

@keyframes dropdown-pop {
  0% { 
    transform: scale(0.8) translateY(-10px); 
    opacity: 0;
  }
  100% { 
    transform: scale(1) translateY(0); 
    opacity: 1;
  }
}

.option-item {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s;
  color: #d6336c;
  font-family: 'ZCOOL KuaiLe', 'FZYaoti', 'STSong', 'KaiTi', 'Arial', sans-serif;
  letter-spacing: 1px;
}

.option-item:hover {
  background: #ffe4ec;
  color: #ff69b4;
  font-weight: bold;
}

.option-item i {
  font-size: 1.1em;
  transition: transform 0.3s;
}

.option-item:hover i {
  transform: scale(1.1);
}

.typing-text {
  color: #d6336c;
  font-size: 0.95em;
  font-style: italic;
  font-family: 'ZCOOL KuaiLe', 'FZYaoti', 'STSong', 'KaiTi', 'Arial', sans-serif;
  letter-spacing: 1px;
}

.typing-indicator .dot {
  width: 8px;
  height: 8px;
  background: #d6336c;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

@keyframes dropdown-pop {
  0% { transform: scale(0.8) translateY(-10px); opacity: 0;}
  100% { transform: scale(1) translateY(0); opacity: 1;}
}

.assessment-progress {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.assessment-progress:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(255, 182, 193, 0.2),
    0 4px 10px rgba(255, 182, 193, 0.1);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 182, 193, 0.4);
}

.progress-bar {
  height: 8px;
  background: rgba(255, 182, 193, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin: 12px 0;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #ffb6c1, #ffc0cb);
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(255, 182, 193, 0.5);
}

.progress-text {
  text-align: center;
  color: var(--primary-color);
  font-size: 1.1em;
  font-weight: 500;
  margin: 8px 0 0 0;
  text-shadow: 0 1px 2px rgba(255, 182, 193, 0.3);
}

.assessment-status {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.assessment-status:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(255, 182, 193, 0.2),
    0 4px 10px rgba(255, 182, 193, 0.1);
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 182, 193, 0.4);
}

.status-content {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.status-content:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateX(5px);
}

.status-content i {
  font-size: 1.4em;
  color: var(--primary-color);
  text-shadow: 0 0 10px rgba(255, 182, 193, 0.3);
}

.status-content p {
  margin: 0;
  color: var(--primary-color);
  font-size: 1.1em;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(255, 182, 193, 0.3);
}

.assessment-sidebar h4 {
  color: var(--primary-color);
  margin: 0 0 12px 0;
  font-size: 1.2em;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(255, 182, 193, 0.3);
  letter-spacing: 1px;
}

/* 动画效果 */
.assessment-popup-enter-active,
.assessment-popup-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.assessment-popup-enter-from,
.assessment-popup-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.report-bubble {
  position: fixed;
  left: 50%;
  top: 120px;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #ffe0f7 0%, #b5eaff 100%);
  color: #d6336c;
  font-size: 1.15em;
  padding: 18px 32px;
  border-radius: 32px;
  box-shadow: 0 8px 32px rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  z-index: 9999;
  animation: bubble-float 2.5s infinite ease-in-out;
  display: flex;
  align-items: center;
  gap: 10px;
}
@keyframes bubble-float {
  0%, 100% { transform: translateX(-50%) translateY(0);}
  50% { transform: translateX(-50%) translateY(-18px);}
}
.bubble-float-enter-active, .bubble-float-leave-active {
  transition: opacity 0.5s;
}
.bubble-float-enter-from, .bubble-float-leave-to {
  opacity: 0;
}
</style> 