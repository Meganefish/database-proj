<template>
  <div class="admin-container">
    <admin-head></admin-head>
    <div class="admin-content">
      <admin-side @update-content="updateContent" :current-component="currentComponent"></admin-side>
      <div class="admin-body">
        <component :is="currentComponent"></component>
      </div>
    </div>
  </div>
</template>

<script>
import AdminHead from './admin_box/admin_head.vue'
import AdminSide from './admin_box/admin_side.vue'
import AdminUser from './admin_box/admin_user.vue'
import AdminPost from './admin_box/admin_post.vue'
import AdminComment from './admin_box/admin_comment.vue'
import AdminApplyForum from './admin_box/admin_apply_forum.vue'
import AdminReportPost from './admin_box/admin_report_post.vue'
import AdminReportComment from './admin_box/admin_report_comment.vue'
import AdminForum from './admin_box/admin_forum.vue'

export default {
  name: 'AdminDashboard',
  components: {
    AdminHead,
    AdminSide,
    AdminUser,
    AdminPost,
    AdminComment,
    AdminApplyForum,
    AdminReportPost,
    AdminReportComment,
    AdminForum,
  },
  data() {
    return {
      currentComponent: 'AdminUser'  // 默认加载管理用户组件
    }
  },
  created() {
    const savedComponent = localStorage.getItem('currentComponent');
    if (savedComponent) {
      this.currentComponent = savedComponent;
    }
  },
  methods: {
    updateContent(key) {
      switch (key) {
        case '1':
          this.currentComponent = 'AdminUser';
          break;
        case '2':
          this.currentComponent = 'AdminPost';
          break;
        case '3':
          this.currentComponent = 'AdminComment';
          break;
        case '4-1':
          this.currentComponent = 'AdminApplyForum';
          break;
        case '5-1':
          this.currentComponent = 'AdminReportPost';
          break;
        case '5-2':
          this.currentComponent = 'AdminReportComment';
          break;
        case '6':
          this.currentComponent = 'AdminForum';
          break;
        default:
          this.currentComponent = 'AdminUser';
      }
      localStorage.setItem('currentComponent', this.currentComponent);
    }
  }
}
</script>


<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.admin-content {
  display: flex;
  flex: 1;
}

.admin-body {
  flex: 1;
  padding: 20px;
}
</style>
