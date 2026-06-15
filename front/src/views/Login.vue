<template>
  <div class="login-page">
    <div class="login-header">
      <h1>智答圈</h1>
      <p>专业知识问答社区</p>
    </div>

    <van-form @submit="handleSubmit">
      <van-field v-model="username" placeholder="用户名" required clearable />
      <van-field
        v-model="password"
        :type="showPassword ? 'text' : 'password'"
        placeholder="密码"
        required
        clearable
        right-icon="eye"
        @click-right-icon="showPassword = !showPassword"
      />
      <van-button type="primary" native-type="submit" block :loading="loading">登录</van-button>
    </van-form>

    <div class="login-footer">
      <span>还没有账号？</span>
      <router-link to="/register">立即注册</router-link>
    </div>

    <div class="tips">
      <p>测试账号：student01 / 123456</p>
      <p>请确保后端服务已启动在 http://127.0.0.1:8000</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { showToast } from "vant";

const router = useRouter();
const userStore = useUserStore();

const username = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);

const handleSubmit = async () => {
  if (!username.value.trim()) {
    showToast("请输入用户名");
    return;
  }

  if (!password.value.trim()) {
    showToast("请输入密码");
    return;
  }

  loading.value = true;
  try {
    await userStore.login(username.value, password.value);
    showToast("登录成功");
    router.push("/");
  } catch (error) {
    console.error("登录失败:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  padding: 40px 30px;
  min-height: 100vh;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.login-header {
  text-align: center;
  color: #fff;
  margin-bottom: 40px;
}

.login-header h1 {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.login-header p {
  font-size: 16px;
  opacity: 0.9;
}

.van-form {
  background: #fff;
  border-radius: 16px;
  padding: 30px;
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  color: #fff;
  font-size: 14px;
}

.login-footer a {
  color: #fff;
  margin-left: 8px;
}

.tips {
  margin-top: 40px;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.tips p {
  margin-bottom: 4px;
}
</style>