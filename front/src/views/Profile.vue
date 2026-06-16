<template>
  <div class="profile-page">
    <div class="profile-header">
      <div class="avatar">
        <van-icon name="user-o" size="80" />
      </div>
      <div class="user-info">
        <h2 class="username">{{ user?.username || '未登录' }}</h2>
        <p class="level">Lv.{{ user?.level || 0 }}</p>
        <p class="points">积分：{{ user?.points || 0 }}</p>
      </div>
    </div>

    <van-cell-group v-if="isLoggedIn">
      <van-cell title="我的提问" icon="edit" @click="goToMyQuestions" />
      <van-cell title="我的回答" icon="message-o" @click="goToMyAnswers" />
      <van-cell title="我的收藏" icon="star-o" @click="goToMyCollections" />
      <van-cell title="设置" icon="settings" @click="goToSettings" />
      <van-cell title="退出登录" icon="log-out" @click="handleLogout" />
    </van-cell-group>

    <div v-else class="login-prompt">
      <van-button type="primary" @click="goToLogin">立即登录</van-button>
      <p class="register-link">
        还没有账号？
        <router-link to="/register">立即注册</router-link>
      </p>
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
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { showToast } from "vant";

const router = useRouter();
const userStore = useUserStore();

const user = computed(() => userStore.user);
const isLoggedIn = computed(() => userStore.isLoggedIn());
const active = ref(4);

const goToLogin = () => {
  router.push("/login");
};

const goToMyQuestions = () => {
  showToast("功能开发中");
};

const goToMyAnswers = () => {
  showToast("功能开发中");
};

const goToMyCollections = () => {
  showToast("功能开发中");
};

const goToSettings = () => {
  showToast("功能开发中");
};

const handleLogout = async () => {
  userStore.logout();
  showToast("已退出登录");
  router.push("/");
};

onMounted(() => {
  userStore.fetchUser();
});
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

.profile-header {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  padding: 40px 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info {
  color: #fff;
}

.username {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.level {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.points {
  font-size: 14px;
  opacity: 0.9;
}

.login-prompt {
  padding: 40px 30px;
  text-align: center;
}

.register-link {
  margin-top: 16px;
  font-size: 14px;
  color: #999;
}

.register-link a {
  color: #667eea;
}
</style>