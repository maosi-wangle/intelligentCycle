<template>
  <div class="ask-page">
    <van-nav-bar title="发起提问" left-arrow @click-left="goBack" />

    <van-form @submit="handleSubmit">
      <van-field v-model="title" placeholder="问题标题" required label="标题" label-width="60px" />
      <van-field
        v-model="content"
        placeholder="问题描述"
        required
        label="描述"
        label-width="60px"
        rows="5"
        type="textarea"
      />
      <div class="tags-section">
        <span class="tags-label">选择标签：</span>
        <div class="tags-list">
          <van-tag
            v-for="tag in availableTags"
            :key="tag.id"
            :type="selectedTags.includes(tag.id) ? 'primary' : 'default'"
            @click="toggleTag(tag.id)"
          >{{ tag.name }}</van-tag>
        </div>
      </div>
      <van-button type="primary" native-type="submit" block :loading="loading">发布提问</van-button>
    </van-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useQuestionStore } from "@/stores/question";
import { getTags } from "@/api/tags";
import { showToast } from "vant";

const router = useRouter();
const questionStore = useQuestionStore();

const title = ref("");
const content = ref("");
const availableTags = ref([]);
const selectedTags = ref([]);
const loading = ref(false);

const loadTags = async () => {
  try {
    const res = await getTags();
    availableTags.value = res.items || res;
  } catch {
    showToast("加载标签失败");
  }
};

const toggleTag = tagId => {
  const index = selectedTags.value.indexOf(tagId);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  } else {
    selectedTags.value.push(tagId);
  }
};

const handleSubmit = async () => {
  if (!title.value.trim()) {
    showToast("请输入问题标题");
    return;
  }
  if (title.value.trim().length < 4) {
    showToast("标题至少需要4个字符");
    return;
  }
  if (!content.value.trim()) {
    showToast("请输入问题描述");
    return;
  }

  loading.value = true;
  try {
    await questionStore.addQuestion({
      title: title.value,
      content: content.value,
      tag_ids: selectedTags.value
    });
    showToast("发布成功");
    router.push("/");
  } catch {
    showToast("发布失败");
  } finally {
    loading.value = false;
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  loadTags();
});
</script>

<style scoped>
.ask-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 16px;
}

.tags-section {
  margin: 16px 0;
}

.tags-label {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
  display: block;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>