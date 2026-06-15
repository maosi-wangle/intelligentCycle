<template>
  <div class="question-detail">
    <van-nav-bar title="问题详情" left-arrow @click-left="goBack" />

    <div v-if="question" class="question-content">
      <h1 class="question-title">{{ question.title }}</h1>
      <p class="question-body">{{ question.content }}</p>
      <div class="question-meta">
        <span class="author">{{ question.author }}</span>
        <span class="time">{{ formatTime(question.created_at) }}</span>
      </div>
      <div class="question-tags">
        <van-tag v-for="tag in question.tags" :key="tag" size="medium">{{ tag }}</van-tag>
      </div>
      <div class="question-stats">
        <van-icon name="eye-o" />
        <span>{{ question.view_count }}</span>
        <van-icon name="message-o" />
        <span>{{ question.answer_count }}</span>
        <van-icon name="like-o" />
        <span>{{ question.like_count }}</span>
      </div>
      <div class="question-actions">
        <van-button :type="question.is_liked ? 'primary' : 'default'" @click="handleLike">
          <van-icon :name="question.is_liked ? 'like' : 'like-o'" />
          {{ question.is_liked ? '已赞' : '点赞' }}
        </van-button>
        <van-button :type="question.is_collected ? 'primary' : 'default'" @click="handleCollect">
          <van-icon :name="question.is_collected ? 'star' : 'star-o'" />
          {{ question.is_collected ? '已收藏' : '收藏' }}
        </van-button>
        <van-button type="default" @click="goToAnswer">
          <van-icon name="edit" />写回答
        </van-button>
      </div>
    </div>

    <div class="answers-section">
      <van-divider content-position="left">
        <span>回答 ({{ answerCount }})</span>
      </van-divider>
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="loadAnswers"
      >
        <div v-for="answer in answers" :key="answer.id" class="answer-card">
          <div class="answer-header">
            <span class="answer-author">{{ answer.author }}</span>
            <span class="answer-time">{{ formatTime(answer.created_at) }}</span>
            <van-tag v-if="answer.is_accepted" color="#07c160">最佳回答</van-tag>
          </div>
          <p class="answer-content">{{ answer.content }}</p>
          <div class="answer-footer">
            <van-button
              :type="answer.is_liked ? 'primary' : 'default'"
              size="small"
              @click="handleLikeAnswer(answer.id)"
            >
              <van-icon :name="answer.is_liked ? 'like' : 'like-o'" />
              {{ answer.like_count }}
            </van-button>
            <van-button
              v-if="showAcceptButton(answer)"
              type="primary"
              size="small"
              @click="handleAcceptAnswer(answer.id)"
            >采纳为最佳答案</van-button>
          </div>
        </div>
      </van-list>
    </div>

    <div class="bottom-input" v-if="showAnswerInput">
      <van-field
        v-model="answerContent"
        placeholder="写下你的回答..."
        rows="3"
        show-word-limit
        maxlength="500"
      />
      <van-button type="primary" block @click="submitAnswer">发布回答</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuestionStore } from "@/stores/question";
import { useUserStore } from "@/stores/user";
import { showToast } from "vant";

const route = useRoute();
const router = useRouter();
const questionStore = useQuestionStore();
const userStore = useUserStore();

const question = ref(null);
const answers = ref([]);
const loading = ref(false);
const finished = ref(false);
const showAnswerInput = ref(false);
const answerContent = ref("");

const answerCount = computed(() => answers.value.length);

const loadQuestion = async () => {
  try {
    const res = await questionStore.loadQuestionDetail(route.params.id);
    question.value = res;
  } catch (error) {
    console.error("加载问题失败:", error);
    showToast("加载失败");
  }
};

const loadAnswers = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await questionStore.loadAnswers(route.params.id);
    if (res.length === 0) {
      finished.value = true;
    } else {
      answers.value = [...answers.value, ...res];
    }
  } catch (error) {
    console.error("加载回答失败:", error);
    showToast("加载失败");
  } finally {
    loading.value = false;
  }
};

const handleLike = async () => {
  try {
    await questionStore.toggleLikeQuestion(route.params.id);
    question.value.is_liked = !question.value.is_liked;
    question.value.like_count += question.value.is_liked ? 1 : -1;
  } catch (error) {
    console.error("点赞失败:", error);
    showToast("操作失败");
  }
};

const handleCollect = async () => {
  try {
    await questionStore.toggleCollectQuestion(route.params.id);
    question.value.is_collected = !question.value.is_collected;
  } catch (error) {
    console.error("收藏失败:", error);
    showToast("操作失败");
  }
};

const handleLikeAnswer = async answerId => {
  try {
    await questionStore.toggleLikeAnswer(answerId);
    const answer = answers.value.find(a => a.id === answerId);
    if (answer) {
      answer.is_liked = !answer.is_liked;
      answer.like_count += answer.is_liked ? 1 : -1;
    }
  } catch (error) {
    console.error("回答点赞失败:", error);
    showToast("操作失败");
  }
};

const handleAcceptAnswer = async answerId => {
  try {
    await questionStore.confirmAcceptAnswer(answerId);
    const answer = answers.value.find(a => a.id === answerId);
    if (answer) {
      answer.is_accepted = true;
    }
    showToast("采纳成功");
  } catch (error) {
    console.error("采纳失败:", error);
    showToast("操作失败");
  }
};

const goToAnswer = () => {
  if (!userStore.isLoggedIn()) {
    showToast("请先登录");
    router.push("/login");
    return;
  }
  showAnswerInput.value = true;
};

const submitAnswer = async () => {
  if (!answerContent.value.trim()) {
    showToast("请输入回答内容");
    return;
  }
  try {
    await questionStore.addAnswer(route.params.id, answerContent.value);
    showToast("发布成功");
    answerContent.value = "";
    showAnswerInput.value = false;
    answers.value = [];
    finished.value = false;
    loadAnswers();
  } catch (error) {
    console.error("发布回答失败:", error);
    showToast("发布失败");
  }
};

const showAcceptButton = answer => {
  return (
    userStore.user?.username === question.value?.author && !answer.is_accepted
  );
};

const formatTime = timeStr => {
  const date = new Date(timeStr);
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  loadQuestion();
  loadAnswers();
});
</script>

<style scoped>
.question-detail {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.question-content {
  background: #fff;
  padding: 16px;
  margin-bottom: 10px;
}

.question-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.5;
}

.question-body {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 12px;
}

.question-meta {
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.author {
  margin-right: 16px;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.question-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: #999;
  margin-bottom: 16px;
}

.question-stats span {
  margin-left: 4px;
}

.question-actions {
  display: flex;
  gap: 12px;
}

.answers-section {
  padding: 0 16px;
}

.answer-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 10px;
}

.answer-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 12px;
}

.answer-author {
  color: #333;
  font-weight: 500;
}

.answer-time {
  color: #999;
}

.answer-content {
  font-size: 15px;
  color: #333;
  line-height: 1.8;
  margin-bottom: 12px;
}

.answer-footer {
  display: flex;
  gap: 12px;
}

.bottom-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}
</style>