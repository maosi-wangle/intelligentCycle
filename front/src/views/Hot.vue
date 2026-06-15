<template>
  <div class="hot-page">
    <van-nav-bar title="热榜" />

    <van-tabs v-model="activeTab" sticky>
      <van-tab title="热门问题">
        <div class="tab-content">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="loadHotQuestions"
          >
            <div
              v-for="(question, index) in hotQuestions"
              :key="question.id"
              class="hot-card"
              @click="goToDetail(question.id)"
            >
              <div class="hot-rank" :class="getRankClass(index)">{{ index + 1 }}</div>
              <div class="hot-content">
                <h3 class="hot-title">{{ question.title }}</h3>
                <div class="hot-stats">
                  <van-icon name="eye-o" size="12" />
                  <span>{{ question.view_count }}</span>
                  <van-icon name="message-o" size="12" />
                  <span>{{ question.answer_count }}</span>
                  <van-icon name="like-o" size="12" />
                  <span>{{ question.like_count }}</span>
                </div>
              </div>
            </div>
          </van-list>
        </div>
      </van-tab>
      <van-tab title="用户排行">
        <div class="tab-content">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="loadUserRankings"
          >
            <div v-for="(user, index) in userRankings" :key="user.id" class="user-card">
              <div class="user-rank" :class="getRankClass(index)">{{ index + 1 }}</div>
              <div class="user-avatar">
                <van-icon name="user-o" size="40" />
              </div>
              <div class="user-info">
                <h4 class="user-name">{{ user.username }}</h4>
                <p class="user-level">Lv.{{ user.level }}</p>
              </div>
              <div class="user-points">
                <span class="points-label">积分</span>
                <span class="points-value">{{ user.points }}</span>
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
import { getHotQuestions, getUserRankings } from "@/api/rankings";
import { showToast } from "vant";

const router = useRouter();

const activeTab = ref(0);
const active = ref(1);
const hotQuestions = ref([]);
const userRankings = ref([]);
const loading = ref(false);
const finished = ref(false);

const loadHotQuestions = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await getHotQuestions();
    if (res.length === 0) {
      finished.value = true;
    } else {
      hotQuestions.value = [...hotQuestions.value, ...res];
    }
  } catch (error) {
    console.error("加载热榜失败:", error);
    showToast("加载失败");
  } finally {
    loading.value = false;
  }
};

const loadUserRankings = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await getUserRankings();
    if (res.length === 0) {
      finished.value = true;
    } else {
      userRankings.value = [...userRankings.value, ...res];
    }
  } catch (error) {
    console.error("加载排行榜失败:", error);
    showToast("加载失败");
  } finally {
    loading.value = false;
  }
};

const getRankClass = index => {
  if (index === 0) return "rank-1";
  if (index === 1) return "rank-2";
  if (index === 2) return "rank-3";
  return "";
};

const goToDetail = id => {
  router.push(`/question/${id}`);
};

watch(activeTab, () => {
  finished.value = false;
  if (activeTab.value === 0) {
    loadHotQuestions();
  } else {
    loadUserRankings();
  }
});

onMounted(() => {
  loadHotQuestions();
});
</script>

<style scoped>
.hot-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

.tab-content {
  padding: 10px;
}

.hot-card {
  display: flex;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 10px;
}

.hot-rank {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: #999;
  margin-right: 16px;
}

.hot-rank.rank-1 {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  color: #fff;
}

.hot-rank.rank-2 {
  background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
  color: #fff;
}

.hot-rank.rank-3 {
  background: linear-gradient(135deg, #ffd93d 0%, #f9ca24 100%);
  color: #fff;
}

.hot-content {
  flex: 1;
}

.hot-title {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.hot-stats {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.user-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 10px;
}

.user-rank {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: #999;
  margin-right: 12px;
}

.user-rank.rank-1 {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
  color: #fff;
}

.user-rank.rank-2 {
  background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
  color: #fff;
}

.user-rank.rank-3 {
  background: linear-gradient(135deg, #ffd93d 0%, #f9ca24 100%);
  color: #fff;
}

.user-avatar {
  margin-right: 12px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.user-level {
  font-size: 12px;
  color: #999;
}

.user-points {
  text-align: right;
}

.points-label {
  font-size: 12px;
  color: #999;
  display: block;
}

.points-value {
  font-size: 18px;
  font-weight: bold;
  color: #ff6b6b;
}
</style>