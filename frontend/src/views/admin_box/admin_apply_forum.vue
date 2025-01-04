<template>
  <div class="admin-apply-forum">
    <el-table :data="paginatedData" style="width: 100%">
      <el-table-column prop="apply_id" label="apply_ID" width="80"></el-table-column>
      <el-table-column prop="name" label="板块标题" width="180"></el-table-column>
      <el-table-column prop="description" label="板块描述" width="250">
        <template v-slot="scope">
          <span>{{ formatDescription(scope.row.description) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="username" label="申请者" width="150"></el-table-column>
      <el-table-column prop="apply_status" label="状态" width="120">
        <template v-slot="scope">
          <span>{{ formatStatus(scope.row.apply_status) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>

      <!-- 操作列：同意、拒绝按钮 -->
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button @click="acceptApply(scope.row.apply_id, scope.row.name, scope.row.description)" type="primary" size="small"
            :disabled="scope.row.apply_status !== 0">
            同意
          </el-button>
          <el-button @click="rejectApply(scope.row.apply_id)" type="danger" size="small"
            :disabled="scope.row.apply_status !== 0">
            拒绝
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页部分 -->
    <el-pagination :page-size="pageSize" :current-page="currentPage" :total="applyList.length"
      layout="prev, pager, next, jumper" @current-change="handlePageChange"></el-pagination>
  </div>
</template>

<script>
import { ElTable, ElTableColumn, ElButton, ElPagination } from 'element-plus';
import axios from 'axios';

export default {
  name: 'AdminApplyForum',
  components: {
    ElTable,
    ElTableColumn,
    ElButton,
    ElPagination,
  },
  data() {
    return {
      applyList: [], // 存储申请数据
      pageSize: 10, // 每页显示 10 条数据
      currentPage: 1, // 当前页
    };
  },
  created() {
    this.fetchApplications(); // 获取申请数据
  },
  computed: {
    // 分页数据
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.applyList.slice(start, end); // 返回当前页的数据
    },
  },
  methods: {
    // 格式化板块描述（超过30个字符显示为...）
    formatDescription(description) {
      if (description.length > 30) {
        return description.slice(0, 30) + '...';
      }
      return description;
    },
    // 格式化申请状态
    formatStatus(status) {
      switch (status) {
        case 0:
          return '待处理';
        case 1:
          return '已解决';
        case 2:
          return '已拒绝';
        default:
          return '未知状态';
      }
    },
    handlePageChange(page) {
      this.currentPage = page; // 更新当前页
    },
    // 获取申请列表
    async fetchApplications() {
      try {
        const response = await axios.get('/admin/get_applies'); // 调用后端接口获取申请数据
        this.applyList = response.data; // 假设接口返回的数据是申请列表
      } catch (error) {
        console.error('获取申请数据失败', error);
      }
    },
    // 同意申请
    async acceptApply(applyId, forumName, description) {
      try {
        const response = await axios.post(`/admin/accept_apply${applyId}`, {
          forum_name: forumName,  // 要发送的数据
          description: description
        }); // 调用后端接口同意申请
        if (response.data.success !== true) {
          throw new Error(response.data.message || '同意申请失败');
        }
        this.$message.success('申请已同意');
        this.fetchApplications(); // 同意后重新获取申请数据
      } catch (error) {
        console.error('同意申请失败', error);
        this.$message.error('同意申请失败');
      }
    },
    // 拒绝申请
    async rejectApply(applyId) {
      try {
        const response = await axios.post(`/admin/reject_apply${applyId}`); // 调用后端接口拒绝申请
        if (response.data.success !== true) {
          throw new Error(response.data.message || '拒绝申请失败');
        }
        this.$message.success('申请已拒绝');
        this.fetchApplications(); // 拒绝后重新获取申请数据
      } catch (error) {
        console.error('拒绝申请失败', error);
        this.$message.error('拒绝申请失败');
      }
    },
  },
};
</script>

<style scoped>
.admin-apply-forum {
  padding: 20px;
}

.el-table {
  width: 100%;
  margin-top: 20px;
}
</style>
