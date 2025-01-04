<template>
  <div class="profile-side">
    <div class="return-to-home" @click="BackToHome"><strong>{{ '<返回主页' }}</strong>
    </div>
    <el-menu class="el-menu-vertical-demo" @select="handleSelect" :default-active="currentComponentIndex">
      <el-menu-item index="1">个人信息</el-menu-item>
      <el-menu-item index="2">参与课程</el-menu-item>
      <el-menu-item index="3">发帖记录</el-menu-item>
      <el-menu-item index="4">评论记录</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import { ElMenu, ElMenuItem } from 'element-plus';
import router from '@/router/Router.js';
export default {
  name: 'profileSide',
  components: {
    ElMenu,
    ElMenuItem
  },
  props: {
    currentComponent: {
      type: String,
      required: true
    }
  },
  setup() {
    const BackToHome = () => {
      router.push({ path: '/home' });
    };
    return {
      BackToHome,
    }
  },
  computed: {
    currentComponentIndex() {
      // 根据传递的 currentComponent 返回对应的菜单索引
      switch (this.currentComponent) {
        case 'profileUser':
          return '1';
        case 'profileCourse':
          return '2';
        case 'profilePost':
          return '3';
        case 'profileComment':
          return '4';
        default:
          return '1';
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
.profile-side {
  width: 250px;
  background-color: #f8f9fa;
  height: 100vh;
}

.return-to-home {
  font-size: 16px;
  padding: 10px;
  cursor: pointer;
}

.el-menu-item {
  font-size: 16px;
  cursor: pointer;
}

.el-menu-item:hover {
  background-color: #e6f7ff;
}
</style>
