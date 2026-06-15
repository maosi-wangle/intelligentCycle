<template>
  <div class="ai-page">
    <van-nav-bar title="AI助手" />

    <div class="chat-container">
      <div v-for="(msg, index) in messages" :key="index" class="message-item" :class="msg.type">
        <div class="avatar">
          <van-icon :name="msg.type === 'user' ? 'user-o' : 'bot-o'" />
        </div>
        <div class="message-content">
          <p>{{ msg.content }}</p>
          <div v-if="msg.sources && msg.sources.length" class="sources">
            <p class="sources-title">参考来源：</p>
            <van-cell-group>
              <van-cell
                v-for="source in msg.sources"
                :key="source.id"
                :title="source.title"
                clickable
              />
            </van-cell-group>
          </div>
        </div>
      </div>

      <van-loading v-if="loading" />
    </div>

    <div class="input-area">
      <van-field
        v-model="question"
        placeholder="输入你的问题..."
        :loading="loading"
        show-action
        @click-action="handleSend"
      />
      <van-button type="primary" block @click="handleSend" :loading="loading">发送</van-button>
    </div>

    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="trending-up" to="/hot">热榜</van-tabbar-item>
      <van-tabbar-item icon="plus" to="/ask">提问</van-tabbar-item>
      <van-tabbar-item icon="message-circle-o" to="/ai">AI助手</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { aiAsk } from "@/api/ai";
import { showToast } from "vant";

const messages = ref([
  {
    type: "bot",
    content: "你好！我是智答圈的AI助手，有什么问题可以问我。"
  }
]);
const question = ref("");
const loading = ref(false);
const active = ref(3);

const handleSend = async () => {
  if (!question.value.trim()) {
    showToast("请输入问题");
    return;
  }

  messages.value.push({
    type: "user",
    content: question.value
  });

  loading.value = true;
  question.value = "";

  try {
    const res = await aiAsk({
      question: messages.value[messages.value.length - 1].content,
      use_retrieval: true
    });

    messages.value.push({
      type: "bot",
      content: res.answer,
      sources: res.sources
    });
  } catch {
    showToast("请求失败，请稍后重试");
    messages.value.push({
      type: "bot",
      content: "抱歉，我暂时无法回答这个问题。"
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.ai-page {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-item.user .message-content {
  background: #667eea;
  color: #fff;
  border-radius: 16px 4px 16px 16px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #e8e8e8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user .avatar {
  margin-left: 12px;
}

.bot .avatar {
  margin-right: 12px;
}

.message-content {
  max-width: 75%;
  background: #fff;
  border-radius: 4px 16px 16px 16px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-content p {
  font-size: 15px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.sources {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.sources-title {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.input-area {
  padding: 16px;
  background: #fff;
  padding-bottom: calc(16px + env(safe-area-inset-bottom) + 60px);
}

.van-loading {
  text-align: center;
  padding: 16px;
}
</style>