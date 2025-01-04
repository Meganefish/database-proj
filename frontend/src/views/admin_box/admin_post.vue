<template>
  <div class="admin-post">
    <el-table :data="paginatedData" style="width: 100%">
      <el-table-column prop="post_id" label="post_ID" width="80"></el-table-column>
      <el-table-column prop="title" label="帖子标题" width="180"></el-table-column>
      <el-table-column prop="body" label="帖子内容" width="250">
        <template v-slot="scope">
          <!-- 通过计算显示帖子内容，限制为20个字，超过则显示... -->
          <span>{{ formatPostBody(scope.row.body) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="forum_name" label="所属论坛名称" width="120"></el-table-column>
      <el-table-column prop="username" label="发布者" width="120"></el-table-column>
      <el-table-column prop="created" label="帖子创建时间" width="180"></el-table-column>
      <!-- 操作列：删除按钮 -->
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button 
            @click="deletePost(scope.row.post_id)" 
            type="danger" 
            size="small">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页部分 -->
    <el-pagination 
      :page-size="pageSize" 
      :current-page="currentPage" 
      :total="posts.length"
      layout="prev, pager, next, jumper" 
      @current-change="handlePageChange">
    </el-pagination>
  </div>
</template>

<script>
import { ElTable, ElTableColumn, ElButton, ElPagination } from 'element-plus';
import axios from 'axios';

export default {
  name: 'AdminPost',
  components: {
    ElTable,
    ElTableColumn,
    ElButton,
    ElPagination
  },
  data() {
    return {
      posts: [],  // 存储帖子数据
      pageSize: 10, // 每页显示 10 条数据
      currentPage: 1 // 当前页
    };
  },
  created() {
    this.fetchPosts();  // 获取帖子数据
  },
  computed: {
    // 分页数据
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.posts.slice(start, end);  // 返回当前页的数据
    }
  },
  methods: {
    formatPostBody(body) {
      if (body.length > 30) {
        return body.slice(0, 30) + '...';
      }
      return body;
    },
    handlePageChange(page) {
      this.currentPage = page;  // 更新当前页
    },
    // 获取帖子列表
    async fetchPosts() {
      try {
        const response = await axios.get('/admin/get_posts');  // 调用后端接口获取帖子数据
        this.posts = response.data;  // 假设接口返回的数据是帖子列表
      } catch (error) {
        console.error('获取帖子数据失败', error);
      }
    },
    // 删除帖子
    async deletePost(postId) {
      try {
        const response = await axios.post(`/admin/delete_post${postId}`);  // 调用后端接口删除帖子
        if(response.data.success !== true) {
          throw new Error(response.data.message||'删除帖子失败');
        }
        this.$message.success('删除成功');
        this.fetchPosts();  // 删除成功后重新获取帖子数据
      } catch (error) {
        console.error('删除帖子失败', error);
        this.$message.error('删除失败');
      }
    }
  }
};
</script>

<style scoped>
.admin-post {
  padding: 20px;
}

.el-table {
  width: 100%;
  margin-top: 20px;
}
</style>
