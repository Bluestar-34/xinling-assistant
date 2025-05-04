<template>
  <div class="science-house-container">
    <!-- 背景点缀元素 -->
    <div class="floating-elements">
      <div v-for="(element, index) in floatingElements" 
           :key="index" 
           class="floating-element"
           :style="element.style">
        <i :class="element.icon"></i>
        <span v-if="element.text">{{ element.text }}</span>
      </div>
    </div>
    <div class="science-title-row">
      <span class="science-subtitle" @click="animateIcon">
        <i class="fas fa-home house-icon" :class="{ 'icon-float': isFloating }"></i>
        心理小屋
      </span>
    </div>
    <div class="daily-quote-box" @click="changeQuote" title="点击换一句鸡汤">
      <span class="daily-quote">{{ dailyQuote }}</span>
    </div>
    <!-- 上方大卡片，支持横向滚动 -->
    <div class="science-card-list-scroll custom-scrollbar">
      <div class="science-card-list">
        <div class="science-card science-card-float science-card-large" 
             v-for="(card, idx) in cards" 
             :key="card.title"
             @click="showCardDetail(card, $event)">
          <h3>{{ card.title }}</h3>
          <p>{{ card.summary }}</p>
        </div>
      </div>
    </div>
    <!-- AI对话悬浮框 -->
    <div class="ai-chat-float" v-if="selectedCard" :class="{ 'show': selectedCard }" :style="chatPosition">
      <div class="ai-chat-header">
        <div class="ai-chat-title">
          <span>小屋辅导员</span>
        </div>
        <button class="pin-btn" :class="{ pinned: isPinned }" @click="togglePin" title="固定/取消固定">
          <i class="fas fa-thumbtack"></i>
        </button>
        <button class="close-btn" @click="closeCardDetail">×</button>
      </div>
      <div class="ai-chat-body">
        <div class="chat-messages" ref="chatMessages">
          <div v-if="aiResponse" class="message ai-message">
            <div class="message-content">{{ aiResponse }}</div>
          </div>
          <div v-if="aiPrompt" class="message ai-message">
            <div class="message-content">{{ aiPrompt }}</div>
          </div>
          <div v-if="userMessages.length" class="message user-message">
            <div class="message-content">{{ userMessages[userMessages.length - 1] }}</div>
          </div>
          <div v-if="aiMessages.length" class="message ai-message">
            <div class="message-content">{{ aiMessages[aiMessages.length - 1] }}</div>
          </div>
          <div v-if="isWaiting" class="message ai-message waiting-message">
            <div class="message-content">
              正在刨心理树洞<span class="dot-ani"><span v-for="n in dotCount" :key="n">.</span></span>
            </div>
          </div>
        </div>
        <div class="chat-input">
          <input type="text" 
                 v-model="userInput" 
                 @keyup.enter="sendMessage"
                 placeholder="和小屋辅导员聊聊..."
                 :disabled="!aiPrompt && !aiResponse">
          <button @click="sendMessage" :disabled="(!aiPrompt && !aiResponse) || !userInput.trim()">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>
    <!-- 下方资源轮滑条 -->
    <div class="resource-strip-wrapper">
      <div class="resource-strip custom-scrollbar" ref="strip">
        <div class="resource-strip-card" v-for="(res, idx) in resources" :key="res.title">
          <a :href="res.link" target="_blank" rel="noopener" class="resource-title">{{ res.title }}</a>
          <span class="resource-desc">{{ res.desc }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScienceHouse',
  data() {
    return {
      isFloating: false,
      selectedCard: null,
      aiResponse: null,
      aiPrompt: null,
      userInput: '',
      userMessages: [],
      aiMessages: [],
      isWaiting: false,
      chatPosition: {
        top: '0px',
        left: '0px'
      },
      sessionId: null,
      floatingElements: [
        { icon: 'fas fa-heart', text: 'Love', style: { left: '10%', top: '15%', animationDelay: '0s' } },
        { icon: 'fas fa-brain', text: 'Mind', style: { left: '85%', top: '25%', animationDelay: '1s' } },
        { icon: 'fas fa-cloud', text: 'Peace', style: { left: '20%', top: '45%', animationDelay: '2s' } },
        { icon: 'fas fa-star', text: 'Hope', style: { left: '75%', top: '60%', animationDelay: '3s' } },
        { icon: 'fas fa-sun', text: 'Warm', style: { left: '35%', top: '75%', animationDelay: '4s' } },
        { icon: 'fas fa-moon', text: 'Calm', style: { left: '65%', top: '85%', animationDelay: '5s' } },
        { icon: 'fas fa-feather', text: 'Light', style: { left: '90%', top: '40%', animationDelay: '6s' } },
        { icon: 'fas fa-leaf', text: 'Grow', style: { left: '15%', top: '90%', animationDelay: '7s' } },
        { icon: 'fas fa-dove', text: 'Free', style: { left: '50%', top: '30%', animationDelay: '8s' } },
        { icon: 'fas fa-rainbow', text: 'Joy', style: { left: '40%', top: '10%', animationDelay: '9s' } }
      ],
      quotes: [
        '每一天都是新的开始，温柔以待自己。',
        '你已经很棒了，别忘了给自己一个微笑。',
        '情绪有波动很正常，慢慢来，一切都会好起来。',
        '给心灵放个假，世界依然美好。',
        '你值得被温柔以待，也值得拥有快乐。',
        '偶尔脆弱没关系，重要的是你一直在努力生活。',
        '别忘了欣赏沿途的风景，也要善待自己。'
      ],
      dailyQuote: '每一天都是新的开始，温柔以待自己。',
      cards: [
        { title: '什么是抑郁症？', summary: '抑郁症是一种常见的情绪障碍，表现为持续的情绪低落、兴趣减退等。' },
        { title: '正念呼吸法', summary: '正念呼吸法是一种简单有效的自我调节方法，有助于缓解焦虑和压力。' },
        { title: '自我关怀小练习', summary: '学会善待自己，是心理健康的重要一步。' },
        { title: '如何应对压力', summary: '学会识别压力源，采用健康的方式进行压力管理。' },
        { title: '睡眠与心理健康', summary: '良好的睡眠有助于情绪稳定和心理健康。' },
        { title: '积极自我对话', summary: '用温柔的语言和自己对话，能提升自信和幸福感。' },
        { title: '社交小贴士', summary: '建立良好的人际关系有助于心理健康。' },
        { title: '情绪ABC法则', summary: '掌握情绪ABC法则，学会自我调节。' },
        { title: '心理求助指南', summary: '遇到困扰时，及时寻求专业帮助很重要。' }
      ],
      resources: [
        { title: '《少有人走的路》', desc: '心理成长经典，探讨自律、爱与成长。', link: 'https://book.douban.com/subject/1084336/' },
        { title: '《蛤蟆先生去看心理医生》', desc: '用童话讲述心理咨询过程，温暖治愈。', link: 'https://book.douban.com/subject/30468597/' },
        { title: '《接纳不完美的自己》', desc: '自我接纳与自我关怀的实用指南。', link: 'https://book.douban.com/subject/27093653/' },
        { title: '心理健康科普（中国心理学会）', desc: '权威心理健康知识平台。', link: 'http://www.cpsbeijing.org/' },
        { title: '《被讨厌的勇气》', desc: '阿德勒心理学入门，学会勇敢做自己。', link: 'https://book.douban.com/subject/26369699/' },
        { title: '《自卑与超越》', desc: '阿德勒心理学代表作，探讨自我成长。', link: 'https://book.douban.com/subject/1054536/' },
        { title: '《活出生命的意义》', desc: '意义疗法创始人弗兰克尔的经典之作。', link: 'https://book.douban.com/subject/1083403/' },
        { title: '壹心理', desc: '国内知名心理学科普与咨询平台。', link: 'https://www.xinli001.com/' },
        { title: '心理月刊', desc: '心理学前沿资讯与深度文章。', link: 'https://www.psychologies.com/' },
        { title: '心理健康热线（中国）', desc: '24小时心理援助热线：12320、400-161-9995', link: 'http://www.chinadepression.org/' },
        { title: '世界卫生组织心理健康', desc: 'WHO权威心理健康知识库。', link: 'https://www.who.int/zh/health-topics/mental-health' },
        { title: '心理学空间', desc: '心理学理论、案例与资讯分享。', link: 'https://www.psychspace.com/' },
        { title: '《情绪急救》', desc: '实用情绪调节与心理自助技巧。', link: 'https://book.douban.com/subject/25862578/' },
        { title: '《我们为何会分离》', desc: '亲密关系心理学，理解分离与成长。', link: 'https://book.douban.com/subject/35231313/' },
        { title: '《亲密关系》', desc: '心理学视角下的亲密关系解读。', link: 'https://book.douban.com/subject/1084332/' }
      ],
      dotCount: 1, // 动态点点动画
      dotAniTimer: null,
      isPinned: false // 新增
    }
  },
  mounted() {
    this.startRandomMovement();
    document.addEventListener('mousedown', this.handleClickOutside);
    // 自动滚动到底部
    this.$nextTick(() => {
      const el = this.$refs.chatMessages;
      if (el) el.scrollTop = el.scrollHeight;
    });
    // 动态点点动画
    this.dotAniTimer = setInterval(() => {
      this.dotCount = this.dotCount % 3 + 1;
    }, 500);
  },
  updated() {
    // 每次更新自动滚动到底部
    this.$nextTick(() => {
      const el = this.$refs.chatMessages;
      if (el) el.scrollTop = el.scrollHeight;
    });
  },
  beforeDestroy() {
    document.removeEventListener('mousedown', this.handleClickOutside);
    if (this.dotAniTimer) clearInterval(this.dotAniTimer);
  },
  unmounted() {
    document.removeEventListener('mousedown', this.handleClickOutside);
    if (this.dotAniTimer) clearInterval(this.dotAniTimer);
  },
  methods: {
    startRandomMovement() {
      setInterval(() => {
        this.floatingElements.forEach(element => {
          const randomX = Math.random() * 80 + 10; // 10% to 90%
          const randomY = Math.random() * 80 + 10; // 10% to 90%
          element.style.left = `${randomX}%`;
          element.style.top = `${randomY}%`;
        });
      }, 15000); // 每15秒随机移动一次
    },
    animateIcon() {
      this.isFloating = true;
      setTimeout(() => {
        this.isFloating = false;
      }, 1000);
    },
    changeQuote() {
      let idx;
      do {
        idx = Math.floor(Math.random() * this.quotes.length);
      } while (this.quotes[idx] === this.dailyQuote && this.quotes.length > 1);
      this.dailyQuote = this.quotes[idx];
    },
    scrollStrip(dir) {
      const el = this.$refs.strip;
      if (!el) return;
      const cardWidth = 260;
      // 优化循环滚动：先滑到尽头再瞬间跳到另一端
      if (dir > 0 && el.scrollLeft + el.offsetWidth >= el.scrollWidth - 10) {
        el.scrollTo({ left: el.scrollWidth, behavior: 'smooth' });
        setTimeout(() => el.scrollTo({ left: 0, behavior: 'auto' }), 350);
      } else if (dir < 0 && el.scrollLeft <= 10) {
        el.scrollTo({ left: 0, behavior: 'smooth' });
        setTimeout(() => el.scrollTo({ left: el.scrollWidth, behavior: 'auto' }), 350);
      } else {
        el.scrollBy({ left: dir * cardWidth, behavior: 'smooth' });
      }
    },
    showCardDetail(card, event) {
      this.selectedCard = card;
      this.aiResponse = null;
      this.aiPrompt = null;
      this.userMessages = [];
      this.aiMessages = [];
      this.isWaiting = false;
      // 计算悬浮框位置
      const cardRect = event.currentTarget.getBoundingClientRect();
      const containerRect = this.$el.getBoundingClientRect();
      const floatWidth = 360; // 悬浮框宽度
      const margin = 20;
      let left = cardRect.right - containerRect.left + margin;
      let top = cardRect.top - containerRect.top;
      // 检查是否超出右侧
      const pageRight = left + floatWidth;
      const maxRight = window.innerWidth - 12; // 12px安全边距
      if (pageRight > maxRight) {
        left = Math.max(cardRect.left - containerRect.left - floatWidth - margin, 8); // 尽量贴卡片左侧
      }
      this.chatPosition = {
        top: `${top}px`,
        left: `${left}px`
      };
      // 先展示预设含义和辅导员主动提问
      setTimeout(() => {
        this.aiResponse = this.generateCardMeaning(card);
        setTimeout(() => {
          this.aiPrompt = '你想进一步聊聊这个话题吗？或者有相关的困扰想和我说说吗？';
        }, 800);
      }, 400);
    },
    generateCardMeaning(card) {
      // 预设含义
      const meanings = {
        '什么是抑郁症？': '“什么是抑郁症？”：这是关于情绪障碍的常见问题。抑郁症不仅仅是心情不好，更是一种需要关注和理解的心理状态。',
        '正念呼吸法': '“正念呼吸法”是一种帮助我们回归当下、缓解压力的简单练习。',
        '自我关怀小练习': '“自我关怀小练习”鼓励我们善待自己，学会自我接纳。',
        '如何应对压力': '“如何应对压力”是每个人都会遇到的话题，找到适合自己的方法很重要。',
        '睡眠与心理健康': '“睡眠与心理健康”密切相关，良好的睡眠有助于情绪稳定。',
        '积极自我对话': '“积极自我对话”能帮助我们建立自信，培养乐观心态。',
        '社交小贴士': '“社交小贴士”帮助我们建立更好的人际关系。',
        '情绪ABC法则': '“情绪ABC法则”是理解和调节情绪的实用工具。',
        '心理求助指南': '“心理求助指南”提醒我们在需要时勇敢寻求帮助。'
      };
      return meanings[card.title] || '这是一个重要的心理健康话题，让我们一起了解吧。';
    },
    generateCardPrompt(card) {
      // 主动互动
      return '你对这个话题有什么想法吗？或者最近有类似的困扰吗？';
    },
    sendMessage() {
      if ((!this.aiPrompt && !this.aiResponse) || !this.userInput.trim()) return;
      this.userMessages.push(this.userInput);
      const userQuestion = this.userInput;
      this.userInput = '';
      this.isWaiting = true;
      // 先显示"让我想想..."
      setTimeout(() => {
        this.isWaiting = false;
        // 模拟API调用
        this.callAIAPI(userQuestion);
      }, 1200);
    },
    async callAIAPI(question) {
      this.isWaiting = true;
      try {
        // 拼接卡片信息和用户信息
        const cardInfo = `当前主题卡片：「${this.selectedCard.title}」——${this.generateCardMeaning(this.selectedCard)}`;
        const userInfo = this.userProfile
          ? `用户信息：昵称：${this.userProfile.nickname}，性别：${this.userProfile.gender}，年龄：${this.userProfile.age}`
          : '';
        const systemPrompt = `你是温柔的小屋辅导员，善于心理疏导。${cardInfo}${userInfo ? '。' + userInfo : ''}你将基于当前主题和用户信息，给出最合适的回复。`;
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: question,
            session_id: this.sessionId,
            system_prompt: systemPrompt
          })
        });
        const data = await res.json();
        this.sessionId = data.session_id;
        this.aiMessages.push(data.response || '小屋辅导员暂时没有更好的建议哦~');
      } catch (e) {
        this.aiMessages.push('网络异常，请稍后再试~');
      }
      this.isWaiting = false;
    },
    closeCardDetail() {
      this.selectedCard = null;
      this.aiResponse = null;
      this.aiPrompt = null;
      this.userMessages = [];
      this.aiMessages = [];
    },
    togglePin() {
      this.isPinned = !this.isPinned;
    },
    handleClickOutside(e) {
      if (!this.selectedCard || this.isPinned) return;
      const chat = this.$el.querySelector('.ai-chat-float');
      if (chat && !chat.contains(e.target)) {
        const cards = this.$el.querySelectorAll('.science-card-float');
        for (let card of cards) {
          if (card.contains(e.target)) return;
        }
        this.closeCardDetail();
      }
    }
  }
}
</script>

<style scoped>
/* 美化横向滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  height: 10px;
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #ffd6e0 0%, #b5eaff 100%);
  border-radius: 8px;
  min-width: 40px;
  box-shadow: 0 2px 8px #ffd6e0;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar {
  scrollbar-color: #ffd6e0 #fff0f7;
  scrollbar-width: thin;
}
.science-house-container {
  padding: 40px 0 0 0;
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f6 0%, #e0f7fa 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}
.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}
.floating-element {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: rgba(177, 151, 252, 0.15);
  font-size: 0.9em;
  animation: float 12s ease-in-out infinite;
  transition: all 8s cubic-bezier(0.4, 0, 0.2, 1);
}
.floating-element i {
  font-size: 1.1em;
  margin-bottom: 2px;
}
.floating-element span {
  font-size: 0.7em;
  white-space: nowrap;
  font-weight: 500;
  letter-spacing: 0.5px;
}
@keyframes float {
  0% { transform: translateY(0) rotate(0); }
  25% { transform: translateY(-12px) rotate(2deg); }
  50% { transform: translateY(-6px) rotate(-2deg); }
  75% { transform: translateY(-15px) rotate(2deg); }
  100% { transform: translateY(0) rotate(0); }
}
.science-title-row {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 12px;
  padding-left: 32px;
}
.science-subtitle {
  font-size: 1.08em;
  color: #b197fc;
  font-weight: 500;
  letter-spacing: 0.1em;
  opacity: 0.85;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.science-subtitle:hover {
  transform: scale(1.05);
}
.house-icon {
  font-size: 1.2em;
  color: #b197fc;
  transition: all 0.3s ease;
}
.icon-float {
  animation: iconFloat 1s ease-in-out;
}
@keyframes iconFloat {
  0% { transform: translateY(0) rotate(0); }
  25% { transform: translateY(-15px) rotate(-10deg); }
  50% { transform: translateY(-20px) rotate(0); }
  75% { transform: translateY(-15px) rotate(10deg); }
  100% { transform: translateY(0) rotate(0); }
}
.daily-quote-box {
  background: linear-gradient(135deg, #ffe0f7 0%, #b5eaff 100%);
  border-radius: 24px;
  padding: 18px 32px;
  margin-bottom: 36px;
  box-shadow: 0 8px 32px rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  font-size: 1.18em;
  color: #d6336c;
  animation: float-quote 3.5s ease-in-out infinite;
  cursor: pointer;
  user-select: none;
  transition: box-shadow 0.2s, background 0.2s;
  z-index: 2;
}
.daily-quote-box:hover {
  box-shadow: 0 12px 40px rgba(255,182,193,0.28), 0 4px 16px #ffd6e0;
  background: linear-gradient(135deg, #ffd6e0 0%, #b5eaff 100%);
}
@keyframes float-quote {
  0% { transform: translateY(0px);}
  50% { transform: translateY(-10px);}
  100% { transform: translateY(0px);}
}
/* 横向滚动容器 */
.science-card-list-scroll {
  width: 100vw;
  max-width: 1200px;
  overflow-x: auto;
  padding-bottom: 8px;
  margin-bottom: 36px;
  scroll-behavior: smooth;
}
.science-card-list {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-start;
  gap: 24px;
  min-width: 600px;
}
.science-card-float {
  min-width: 210px;
  max-width: 320px;
  padding: 24px 18px;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(255,182,193,0.15), 
              0 4px 16px rgba(181,234,255,0.15),
              0 2px 8px rgba(255,214,224,0.2);
  color: #2C3E50;
  background: linear-gradient(135deg, #fff5f6 0%, #f0f9ff 100%);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-align: left;
  font-size: 1.08em;
  perspective: 1000px;
  transform-style: preserve-3d;
  position: relative;
  z-index: 1;
  will-change: transform, box-shadow;
  backdrop-filter: blur(8px);
}
.science-card-float:hover {
  box-shadow: 0 16px 48px rgba(255,182,193,0.25), 
              0 8px 24px rgba(181,234,255,0.25),
              0 4px 16px rgba(255,214,224,0.3);
  transform: translateY(-8px) scale(1.02) rotateY(-5deg) rotateX(2deg);
}
.science-card-float:active {
  transform: translateY(-4px) scale(0.98) rotateY(-2deg) rotateX(1deg);
}
.science-card-large {
  min-width: 240px;
  max-width: 340px;
  font-size: 1.12em;
  padding: 28px 18px;
}
.resource-strip-wrapper {
  width: 100vw;
  max-width: 1200px;
  margin: 0 auto 32px auto;
  padding-bottom: 24px;
  z-index: 2;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.resource-strip {
  display: flex;
  overflow-x: auto;
  gap: 18px;
  padding: 10px 0;
  scroll-behavior: smooth;
  width: 80vw;
  max-width: 900px;
}
.resource-strip-card {
  background: linear-gradient(135deg, #e0f7fa 0%, #ffe0f7 100%);
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(255,182,193,0.18), 0 2px 8px #ffd6e0;
  padding: 14px 22px 12px 22px;
  min-width: 200px;
  max-width: 240px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 1em;
  transition: box-shadow 0.25s, transform 0.25s;
  cursor: pointer;
  perspective: 600px;
  transform-style: preserve-3d;
  position: relative;
}
.resource-strip-card:hover {
  box-shadow: 0 16px 48px #ffd6e0, 0 4px 16px #b5eaff;
  transform: translateY(-8px) scale(1.06) rotateY(-8deg) rotateX(4deg);
}
.resource-title {
  color: #d6336c;
  font-weight: 600;
  font-size: 1.08em;
  text-decoration: none;
  margin-bottom: 4px;
  transition: color 0.2s;
}
.resource-title:hover {
  color: #ff69b4;
  text-decoration: underline;
}
.resource-desc {
  color: #2C3E50;
  opacity: 0.88;
  font-size: 0.98em;
}
.strip-btn {
  background: #fff0f7;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  color: #d6336c;
  box-shadow: 0 2px 8px #ffd6e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  cursor: pointer;
  margin: 0 8px;
  transition: background 0.3s;
  position: relative;
  z-index: 3;
}
.strip-btn:hover {
  background: #ffd6e0;
}
.strip-btn.left {
  left: 0;
}
.strip-btn.right {
  right: 0;
}
.ai-chat-float {
  position: absolute;
  width: 360px;
  max-width: 96vw;
  min-width: 260px;
  height: 480px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  transform: translateX(20px);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  overflow: hidden;
  right: auto;
}
.ai-chat-float.show {
  transform: translateX(0);
  opacity: 1;
}
@media (max-width: 600px) {
  .ai-chat-float {
    width: 98vw;
    min-width: unset;
    left: 1vw !important;
    right: unset !important;
  }
}
.ai-chat-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #ffe0f7 0%, #b5eaff 100%);
  border-bottom: 1px solid rgba(255,182,193,0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.ai-chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d6336c;
  font-size: 1.1em;
  font-weight: 500;
}
.ai-chat-title i {
  color: #d6336c;
}
.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #d6336c;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 50%;
  transition: all 0.2s;
}
.close-btn:hover {
  background: rgba(255,182,193,0.1);
  color: #ff69b4;
}
.pin-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #b197fc;
  cursor: pointer;
  margin-right: 8px;
  transition: color 0.2s, transform 0.2s;
}
.pin-btn.pinned {
  color: #d6336c;
  transform: rotate(-30deg) scale(1.2);
}
.pin-btn:hover {
  color: #ff69b4;
}
.ai-chat-body {
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100%;
  min-height: 0;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.message {
  display: flex;
  flex-direction: row;
  width: 100%;
  animation: messageSlide 0.3s ease;
}
.ai-message {
  justify-content: flex-start;
}
.user-message {
  justify-content: flex-end;
}
.message-content {
  max-width: 340px;
  min-width: 48px;
  padding: 18px 22px;
  border-radius: 18px;
  font-size: 1.08em;
  line-height: 1.7;
  word-break: break-word;
  box-shadow: 0 8px 32px rgba(255,182,193,0.15), 0 4px 16px rgba(181,234,255,0.15), 0 2px 8px rgba(255,214,224,0.2);
  margin-bottom: 2px;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: inherit;
}
.ai-message .message-content {
  background: linear-gradient(135deg, #fff5f6 0%, #f0f9ff 100%);
  color: #d6336c;
  border-bottom-left-radius: 8px;
  border-top-right-radius: 18px;
  border-top-left-radius: 18px;
  border-bottom-right-radius: 18px;
  align-self: flex-start;
}
.user-message .message-content {
  background: linear-gradient(135deg, #b197fc 0%, #8a7aff 100%);
  color: #fff;
  border-bottom-right-radius: 8px;
  border-top-left-radius: 18px;
  border-top-right-radius: 18px;
  border-bottom-left-radius: 18px;
  align-self: flex-end;
}
.waiting-message .message-content {
  background: #f3f0ff;
  color: #b197fc;
  font-style: italic;
}
.chat-input {
  display: flex;
  align-items: center;
  gap: 8px;
  position: sticky;
  bottom: 0;
  background: white;
  z-index: 2;
  padding: 16px;
  border-top: 1px solid rgba(255,182,193,0.2);
}
.chat-input input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid rgba(255,182,193,0.3);
  border-radius: 20px;
  font-size: 0.95em;
  background: rgba(255,255,255,0.8);
  transition: all 0.2s;
}
.chat-input button {
  background: linear-gradient(135deg, #ffe0f7 0%, #b5eaff 100%);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 20px;
  color: #d6336c;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chat-input button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(255,182,193,0.3);
}
.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.dot-ani {
  display: inline-block;
  min-width: 12px;
  letter-spacing: 1px;
  font-weight: bold;
  color: #b197fc;
  animation: dotWave 1.2s infinite linear;
}
@keyframes dotWave {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}
@keyframes messageSlide {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style> 