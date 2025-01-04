<template>
  <div class="admin-report">
    <el-table :data="paginatedData" style="width: 100%">
      <el-table-column prop="report_id" label="报告ID" width="80"></el-table-column>
      <el-table-column prop="body" label="举报评论内容" width="200">
        <template v-slot="scope">
          <!-- 通过计算显示举报理由，长度大于30则显示省略号 -->
          <span>{{ formatReason(scope.row.body) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="username" label="举报者" width="120"></el-table-column>
      <el-table-column prop="reason" label="举报理由" width="200">
        <template v-slot="scope">
          <!-- 通过计算显示举报理由，长度大于30则显示省略号 -->
          <span>{{ formatReason(scope.row.reason) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="report_status" label="状态" width="120">
        <template v-slot="scope">
          <span>{{ reportStatusText(scope.row.report_status) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="created" label="举报时间" width="180"></el-table-column>

      <!-- 操作列：接受/拒绝按钮 -->
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button 
            @click="acceptReport(scope.row.report_id)" 
            type="primary" 
            size="small"
            :disabled="scope.row.report_status !== 0">
            接受
          </el-button>
          <el-button 
            @click="rejectReport(scope.row.report_id)" 
            type="danger" 
            size="small"
            :disabled="scope.row.report_status !== 0">
            拒绝
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页部分 -->
    <el-pagination :page-size="pageSize" :current-page="currentPage" :total="reports.length"
      layout="prev, pager, next, jumper" @current-change="handlePageChange"></el-pagination>
  </div>
</template>

<script>
import { ElTable, ElTableColumn, ElButton, ElPagination } from 'element-plus';
import axios from 'axios';

export default {
  name: 'AdminReportComment',
  components: {
    ElTable,
    ElTableColumn,
    ElButton,
    ElPagination
  },
  data() {
    return {
      reports: [],  // 存储举报数据
      pageSize: 10, // 每页显示 10 条数据
      currentPage: 1 // 当前页
    };
  },
  created() {
    this.fetchReports();  // 获取举报数据
  },
  computed: {
    // 分页数据
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.reports.slice(start, end);  // 返回当前页的数据
    }
  },
  methods: {
    // 格式化举报理由：如果长度大于30，则显示省略号
    formatReason(reason) {
      if (reason.length > 30) {
        return reason.slice(0, 30) + '...';
      }
      return reason;
    },
    // 格式化举报状态
    reportStatusText(status) {
      switch (status) {
        case 0: return '待处理';
        case 1: return '已解决';
        case 2: return '已拒绝';
        default: return '未知状态';
      }
    },
    // 分页切换
    handlePageChange(page) {
      this.currentPage = page;  // 更新当前页
    },
    // 获取举报数据
    async fetchReports() {
      try {
        const response = await axios.get('/admin/get_reports');
        this.reports = response.data.report_comments;  // 假设接口返回的是举报列表
      } catch (error) {
        console.error('获取举报数据失败', error);
      }
    },
    // 接受举报
    async acceptReport(reportId) {
      try {
        await axios.post(`/admin/accept_report${reportId}`);  // 调用后端接口接受举报
        this.$message.success('举报已接受');
        this.fetchReports();  // 接受后重新获取举报数据
      } catch (error) {
        console.error('接受举报失败', error);
        this.$message.error('接受举报失败');
      }
    },
    // 拒绝举报
    async rejectReport(reportId) {
      try {
        await axios.post(`/admin/reject_report${reportId}`);  // 调用后端接口拒绝举报
        this.$message.success('举报已拒绝');
        this.fetchReports();  // 拒绝后重新获取举报数据
      } catch (error) {
        console.error('拒绝举报失败', error);
        this.$message.error('拒绝举报失败');
      }
    }
  }
};
</script>

<style scoped>
.admin-report {
  padding: 20px;
}

.el-table {
  width: 100%;
  margin-top: 20px;
}
</style>
