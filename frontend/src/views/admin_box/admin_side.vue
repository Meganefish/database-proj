<template>
  <div class="admin-side">
    <el-menu class="el-menu-vertical-demo" @select="handleSelect" :default-active="currentComponentIndex">
      <!-- 管理用户 -->
      <el-menu-item index="1">管理用户</el-menu-item>
      <!-- 管理帖子 -->
      <el-menu-item index="2">管理帖子</el-menu-item>
      <!-- 管理评论 -->
      <el-menu-item index="3">管理评论</el-menu-item>

      <!-- 管理申请下拉框 -->
      <el-submenu index="4" popper-append-to-body>
        <template #title>管理申请</template>
        <el-menu-item index="4-1">创建板块申请</el-menu-item>
      </el-submenu>

      <!-- 管理举报下拉框 -->
      <el-submenu index="5" popper-append-to-body>
        <template #title>管理举报</template>
        <el-menu-item index="5-1">帖子举报</el-menu-item>
        <el-menu-item index="5-2">评论举报</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import { ElMenu, ElMenuItem } from 'element-plus';

export default {
  name: 'AdminSide',
  components: {
    ElMenu,
    ElMenuItem,
  },
  props: {
    currentComponent: {
      type: String,
      required: true
    }
  },
  computed: {
    currentComponentIndex() {
      // 根据传递的 currentComponent 返回对应的菜单索引
      switch (this.currentComponent) {
        case 'AdminUser':
          return '1';
        case 'AdminPost':
          return '2';
        case 'AdminComment':
          return '3';
        case 'AdminApplyForum':
          return '4-1';
        case 'AdminReportPost':
          return '5-1';
        case 'AdminReportComment':
          return '5-2';
        default:
          return '1';  // 默认是管理用户
      }
    }
  },
  methods: {
    handleSelect(index) {
      // 触发父组件事件，传递选择的项
      this.$emit('update-content', index);
    }
  }
}
</script>

<style scoped>
.admin-side {
  width: 250px;
  background-color: #f8f9fa;
  height: 100vh;
}

.el-menu-item {
  font-size: 16px;
  cursor: pointer;
}

.el-menu-item:hover {
  background-color: #e6f7ff;
}
</style>
