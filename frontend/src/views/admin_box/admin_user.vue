<template>
  <div class="admin-user">
    <strong>管理用户</strong>
    <el-table :data="paginatedData" style="width: 100%">
      <el-table-column prop="user_id" label="ID" width="80"></el-table-column>
      <el-table-column prop="username" label="用户名" width="180"></el-table-column>
      <el-table-column prop="nickname" label="昵称" width="120"></el-table-column>
      <el-table-column prop="password" label="密码" width="180">
        <template v-slot="scope">
          <!-- 通过计算显示密码，长度大于20则显示省略号 -->
          <span>{{ formatPassword(scope.row.password) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="grade" label="年级" width="80"></el-table-column>
      <el-table-column prop="major" label="专业" width="150"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>

      <!-- 操作列：删除按钮 -->
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button 
            @click="deleteUser(scope.row.user_id)" 
            type="danger" 
            size="small"
            :disabled="scope.row.category === 'admin'">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页部分 -->
    <el-pagination :page-size="pageSize" :current-page="currentPage" :total="users.length"
      layout="prev, pager, next, jumper" @current-change="handlePageChange"></el-pagination>
  </div>
</template>

<script>
import { ElTable, ElTableColumn, ElButton, ElPagination } from 'element-plus';
import axios from 'axios';

export default {
  name: 'AdminUser',
  components: {
    ElTable,
    ElTableColumn,
    ElButton,
    ElPagination
  },
  data() {
    return {
      users: [],  // 存储用户数据
      pageSize: 10, // 每页显示 10 条数据
      currentPage: 1 // 当前页
    };
  },
  created() {
    this.fetchUsers();  // 获取用户数据
  },
  computed: {
    // 分页数据
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.users.slice(start, end);  // 返回当前页的数据
    }
  },
  setup() {
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
    };
  },
  methods: {
    formatPassword(password) {
      if (password.length > 20) {
        return password.slice(0, 20) + '...';
      }
      return password;
    },
    handlePageChange(page) {
      this.currentPage = page;  // 更新当前页
    },
    // 获取用户列表
    async fetchUsers() {
      try {
        const response = await axios.get('/admin/get_users', {});  // 调用后端接口获取用户数据
        this.users = response.data;  // 假设接口返回的数据是用户列表
        this.users.forEach(user => {
          user.created_at = this.Timetrans(user.created_at);  // 格式化时间
        });
      } catch (error) {
        console.error('获取用户数据失败', error);
      }
    },
    // 删除用户
    async deleteUser(userId) {
      try {
        const response = await axios.post(`/admin/delete_user${userId}`);  // 调用后端接口删除用户
        if(response.data.success !== true) {
          throw new Error(response.data.message||'删除用户失败');
        }
        this.$message.success('删除成功');
        this.fetchUsers();  // 删除成功后重新获取用户数据
      } catch (error) {
        console.error('删除用户失败', error);
        this.$message.error('删除用户失败');
      }
    }
  }
};
</script>

<style scoped>
.admin-user {
  padding: 20px;
}

.el-table {
  width: 100%;
  margin-top: 20px;
}
</style>
