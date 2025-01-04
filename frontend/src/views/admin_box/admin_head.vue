<template>
  <div class="admin-head">
    <div class="left">
      高校论坛管理平台
    </div>
    <div class="right">
      <a-button type="primary" @click="logout">Log out</a-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from "element-plus";

export default {
  name: 'AdminHead',
  methods: {
    // 处理登出请求
    async logout() {
      try {
        const response = await axios.post('/auth/logout');
        
        if (response.data.success === true) {
          ElMessage.success({
                message: "登出成功", duration: 500,
                onClose: () => {
                  window.location.href = '/login';
                }
              });
        } else {
          ElMessage.error(response.data.message || "登录失败");
        }
      } catch (error) {
        this.$message.error('登出请求失败，请检查网络连接');
      }
    }
  }
}
</script>

<style scoped>
.admin-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #4c536b; /* 蓝色背景 */
  padding: 10px 20px;
  color: white;
}

.left {
  font-size: 20px;
  font-weight: bold;
}

.right {
  display: flex;
  align-items: center;
  background-color: #2b201f; 
  padding: 5px 10px;
}

.right .ant-btn {
  background-color: #403535; /* 红色的登出按钮 */
  color: white;
  border: none;
}

.right .ant-btn:hover {
  background-color: #746a6a; /* 鼠标悬停时的颜色 */
}
</style>
