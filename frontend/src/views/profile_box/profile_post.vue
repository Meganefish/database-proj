<template>
    <div class="admin-post">
      <strong>发帖记录</strong>
      <el-table :data="paginatedData" style="width: 100%">
        <el-table-column prop="post_id" label="post_ID" width="80"></el-table-column>
        <el-table-column prop="title" label="帖子标题" width="180"></el-table-column>
        <el-table-column prop="body" label="帖子内容" width="250">
          <template v-slot="scope">
            <!-- 通过计算显示帖子内容，限制为20个字，超过则显示... -->
            <span>{{ formatPostBody(scope.row.body) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created" label="帖子创建时间" width="180"></el-table-column>

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
  import { ElTable, ElTableColumn, ElPagination } from 'element-plus';
  import axios from 'axios';  
import { useRoute } from 'vue-router';
  
  export default {
    name: 'AdminPost',
    components: {
      ElTable,
      ElTableColumn,
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
    setup(){
      function Timetrans(gmtTime) {
        const date = new Date(gmtTime);
        const options = {
          timeZone: "Asia/Shanghai",
          year: "numeric",
          month: "long",
          day: "numeric",
          weekday: "long",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        };
        const formatter = new Intl.DateTimeFormat("zh-CN", options);
        return formatter.format(date);
      }
      return {
        Timetrans
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
            const route = useRoute();
            const userId = route.params.user_id;
        try {
          const response = await axios.get(`/auth/profile${userId}`);  // 调用后端接口获取帖子数据
          this.posts = response.data.posts;  // 假设接口返回的数据是帖子列表
          this.posts.forEach(post => {
            post.created = this.Timetrans(post.created);  // 格式化时间
          });
        } catch (error) {
          console.error('获取帖子数据失败', error);
        }
      },
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
  