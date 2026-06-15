<template>
  <div class="home-page">
    <van-search v-model="keyword" placeholder="搜索问题" show-action @search="handleSearch" />

    <van-tabs v-model="activeTab" sticky>
      <van-tab title="推荐">
        <div class="tab-content">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="loadRecommendations"
          >
            <div
              v-for="question in questions"
              :key="question.id"
              class="question-card"
              @click="goToDetail(question.id)"
            >
              <h3 class="question-title">{{ question.title }}</h3>
              <div class="question-footer">
                <span class="author">{{ question.author }}</span>
                <span class="tags">
                  <van-tag v-for="tag in question.tags" :key="tag" size="small">{{ tag }}</van-tag>
                </span>
                <div class="stats">
                  <van-icon name="eye-o" size="14" />
                  <span>{{ question.view_count }}</span>
                  <van-icon name="message-o" size="14" />
                  <span>{{ question.answer_count }}</span>
                  <van-icon name="like-o" size="14" />
                  <span>{{ question.like_count }}</span>
                </div>
              </div>
            </div>
          </van-list>
        </div>
      </van-tab>
      <van-tab title="最新">
        <div class="tab-content">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="loadLatest"
          >
            <div
              v-for="question in questions"
              :key="question.id"
              class="question-card"
              @click="goToDetail(question.id)"
            >
              <h3 class="question-title">{{ question.title }}</h3>
              <div class="question-footer">
                <span class="author">{{ question.author }}</span>
                <span class="tags">
                  <van-tag v-for="tag in question.tags" :key="tag" size="small">{{ tag }}</van-tag>
                </span>
                <div class="stats">
                  <van-icon name="eye-o" size="14" />
                  <span>{{ question.view_count }}</span>
                  <van-icon name="message-o" size="14" />
                  <span>{{ question.answer_count }}</span>
                </div>
              </div>
            </div>
          </van-list>
        </div>
      </van-tab>
    </van-tabs>

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
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useQuestionStore } from "@/stores/question";
import { getRecommendedQuestions } from "@/api/recommendations";
import { showToast } from "vant";

const router = useRouter();
const questionStore = useQuestionStore();

const keyword = ref("");
const activeTab = ref(0);
const active = ref(0);
const questions = ref([]);
const loading = ref(false);
const finished = ref(false);
const page = ref(1);

const loadRecommendations = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await getRecommendedQuestions();
    if (res.length === 0) {
      finished.value = true;
    } else {
      questions.value = [...questions.value, ...res];
      finished.value = true;
    }
  } catch (error) {
    console.error("加载推荐失败:", error);
    showToast("加载失败");
  } finally {
    loading.value = false;
  }
};

const loadLatest = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await questionStore.loadQuestions({
      page: page.value,
      page_size: 10
    });
    if (res.items.length === 0) {
      finished.value = true;
    } else {
      questions.value = [...questions.value, ...res.items];
      page.value++;
    }
  } catch (error) {
    console.error("加载最新失败:", error);
    showToast("加载失败");
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  if (keyword.value.trim()) {
    router.push({ path: "/", query: { keyword: keyword.value } });
  }
};

const goToDetail = id => {
  router.push(`/question/${id}`);
};

watch(activeTab, () => {
  questions.value = [];
  page.value = 1;
  finished.value = false;
  if (activeTab.value === 0) {
    loadRecommendations();
  } else {
    loadLatest();
  }
});

onMounted(() => {
  loadRecommendations();
});
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

.tab-content {
  padding: 10px;
}

.question-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 10px;
}

.question-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.question-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.author {
  margin-right: 10px;
}

.tags {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stats span {
  margin-left: 2px;
}
</style>