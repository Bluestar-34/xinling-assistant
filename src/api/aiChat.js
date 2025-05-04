import axios from 'axios';

/**
 * 发送AI对话请求，参照心聆驿站风格
 * @param {Array} messages - 聊天历史消息数组
 * @returns {Promise} - Promise resolves to { reply }
 */
export function sendAiChat(messages) {
  return axios.post('/api/chat', { messages });
} 