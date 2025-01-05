<template>
  <div class="profile-head">
    <div class="left">
      高校论坛平台
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from "element-plus";

export default {
  name: 'profileHead',
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
.profile-head {
  width: 100%;
  background-image: url('../../assets/img/headline_bg.jpg');
  background-size: cover;
  background-position: center;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.left {
  font-size: 1.5em;
  font-weight: bold;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.right {
  display: flex;
  align-items: center;
  background-color: #2b201f;
  padding: 5px 10px;
}

.right .ant-btn {
  background-color: #403535;
  /* 红色的登出按钮 */
  color: white;
  border: none;
}

.right .ant-btn:hover {
  background-color: #746a6a;
  /* 鼠标悬停时的颜色 */
}
</style>