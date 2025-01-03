<template>
    <div class="home-container">
      <!-- 顶部标题栏 -->
      <el-header class="header">
        <div :class="['header-title', { 'shifted-title': selectedBlockId !== null }]">
          高校论坛平台
        </div>
        <el-select
          v-model="selectedBlockId"
          placeholder="请选择版块"
          class="block-selector"
          @change="handleBlockChange"
        >
          <el-option
            label="总版块"
            :value="null"
          />
          <el-option
            v-for="block in forumBlocks"
            :key="block.id"
            :label="block.name"
            :value="block.id"
          />
        </el-select>
        <el-input
          class="header-search"
          placeholder="搜索帖子或内容"
          v-model="searchQuery"
          clearable
          prefix-icon="el-icon-search"
          @keyup.enter="handleSearch"
        />
        <el-dropdown trigger="click">
            <span class="username-dropdown">
            {{ username }}</span>
            <template #dropdown>
        <el-dropdown-menu>
            <el-dropdown-item @click="goToRoute('/profile')">个人界面</el-dropdown-item>
        <el-dropdown-item>退出登录</el-dropdown-item>
        </el-dropdown-menu>
        </template>
        </el-dropdown>
      </el-header>
  
      <!-- 主体布局 -->
      <el-container>
        <!-- 中间内容区 -->
        <el-main class="content">
          <el-row :gutter="20" v-for="post in displayedPosts" :key="post.post_id">
            <el-col :span="24" class="post-card">
              <el-card shadow="hover">
                <h3 class="post-title" @click="goToPostDetail(post.post_id)">
                  {{ post.title.length > 10 ? post.title.slice(0, 10) + '...' : post.title }}
                </h3>
                <p>
                  作者：{{ post.nickname.length > 10 ? post.nickname.slice(0, 10) + '...' : post.nickname }}
                </p>
                <p>
                  内容：
                  {{ post.body.length > 50
                    ? post.body.slice(0, 50) + '...'
                    : post.body }}
                </p>
                <div class="post-stats">
                  <span>👍 {{ post.liked }}</span>
                  <span>💬 {{ post.commented }}</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-pagination
            background
            layout="prev, pager, next"
            :total="totalPosts"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="fetchPosts"
          />
        </el-main>
      </el-container>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router";
  
  export default {
    name: "Home_page",
    setup() {
      const router = useRouter();
      const searchQuery = ref("");
      const forumBlocks = ref([]);
      const selectedBlockId = ref(null); // 默认选择 "总版块"
      const displayedPosts = ref([]);
      const totalPosts = ref(0);
      const currentPage = ref(1);
      const pageSize = 5;
  
      const fetchForumBlocks = async () => {
        try {
          const response = await axios.get("/get_forums");
          forumBlocks.value = response.data;
        } catch (error) {
          console.error("获取论坛版块数据失败：", error);
        }
      };
  
      const fetchPosts = async () => {
        try {
          const response = await axios.get("/p"+ currentPage.value);
          displayedPosts.value = response.data;
          totalPosts.value = response.data.length;
        } catch (error) {
          console.error("获取帖子数据失败：", error);
        }
      };
  
      const handleBlockChange = () => {
        currentPage.value = 1; // 切换版块时重置页码
        fetchPosts();
      };
  
      const handleSearch = () => {
        alert(`搜索：${searchQuery.value}`);
      };
  
      const goToRoute = (route) => {
        router.push(route);
      };
  
      const goToPostDetail = (postId) => {
        router.push(`/post${postId}`);
      };
  
      onMounted(() => {
        fetchForumBlocks();
        fetchPosts();
      });
  
      return {
        searchQuery,
        forumBlocks,
        selectedBlockId,
        displayedPosts,
        totalPosts,
        currentPage,
        pageSize,
        fetchPosts,
        handleBlockChange,
        handleSearch,
        goToRoute,
        goToPostDetail,
      };
    },
  };
  </script>
  
  <style scoped>
  .home-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
  }
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    background-color: #409eff;
    color: #fff;
  }
  .header-title {
    font-size: 1.5em;
    font-weight: bold;
    transition: margin-left 0.3s ease;
  }
  .shifted-title {
    margin-left: 20px;
  }
  .block-selector {
    width: 200px;
    margin-right: 20px;
  }
  .header-search {
    flex: 1;
    margin-right: 20px;
  }
  .avatar-dropdown {
    cursor: pointer;
  }
  .content {
    overflow-y: auto;
    padding: 20px;
  }
  .post-card {
    margin-bottom: 20px;
  }
  .post-title {
    cursor: pointer;
    color: #409eff;
    transition: color 0.3s;
  }
  .post-title:hover {
    color: #66b1ff;
  }
  .post-stats {
    display: flex;
    justify-content: space-between;
    font-size: 0.9em;
    color: #606266;
  }
  </style>
  