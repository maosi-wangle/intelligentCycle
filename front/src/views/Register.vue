<template>
  <div class="register-page">
    <div class="register-header">
      <h1>智答圈</h1>
      <p>创建账号，开始探索</p>
    </div>

    <van-form @submit="handleSubmit">
      <van-field v-model="username" placeholder="用户名" required clearable />
      <van-field v-model="email" type="email" placeholder="邮箱" required clearable />
      <van-field
        v-model="password"
        type="password"
        placeholder="密码"
        required
        clearable
        :show-password="showPassword"
        right-icon="eye"
        @click-right-icon="showPassword = !showPassword"
      />
      <van-field v-model="confirmPassword" type="password" placeholder="确认密码" required clearable />
      <van-button type="primary" native-type="submit" block :loading="loading">注册</van-button>
    </van-form>

    <div class="register-footer">
      <span>已有账号？</span>
      <router-link to="/login">立即登录</router-link>
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
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const loading = ref(false);

const handleSubmit = async () => {
  if (!username.value || !email.value || !password.value) {
    showToast("请填写完整信息");
    return;
  }

  if (password.value !== confirmPassword.value) {
    showToast("两次输入的密码不一致");
    return;
  }

  loading.value = true;
  try {
    await userStore.register(username.value, password.value, email.value);
    showToast("注册成功");
    router.push("/login");
  } catch (error) {
    showToast(error.response?.data?.message || "注册失败");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  padding: 40px 30px;
  min-height: 100vh;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.register-header {
  text-align: center;
  color: #fff;
  margin-bottom: 40px;
}

.register-header h1 {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.register-header p {
  font-size: 16px;
  opacity: 0.9;
}

.van-form {
  background: #fff;
  border-radius: 16px;
  padding: 30px;
}

.register-footer {
  text-align: center;
  margin-top: 30px;
  color: #fff;
  font-size: 14px;
}

.register-footer a {
  color: #fff;
  margin-left: 8px;
}
</style>