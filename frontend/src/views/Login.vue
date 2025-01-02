<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <h2 class="login-title">登录</h2>
      <el-form :model="form" :rules="rules"  label-width="100px">
        <!-- 登录身份选择 -->
        <el-form-item label="登录类型">
          <el-radio-group v-model="form.userType">
            <el-radio label="user">普通用户</el-radio>
            <el-radio label="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 用户名 -->
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon><user /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <!-- 密码 -->
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            show-password
          >
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <!-- 验证码
        <el-form-item label="验证码" prop="captcha">
          <el-row>
            <el-col :span="14">
              <el-input v-model="form.captcha" placeholder="请输入验证码" />
            </el-col>
            <el-col :span="10" class="captcha-img-container">
              <img
                :src="captchaSrc"
                @click="refreshCaptcha"
                alt="captcha"
                title="点击刷新验证码"
              />
            </el-col>
          </el-row>
        </el-form-item> -->

        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            @click="handleLogin"
            plain
            block
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { reactive } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
// import { User, Lock } from "@element-plus/icons-vue";

export default {
  name: "Login-Form",
  // components: {
  //   user: User,
  //   lock: Lock,
  // },
  setup() {
    const form = reactive({
      userType: "user", // 登录类型
      username: "",
      password: "",
      // captcha: "",
    });
    const rules = {
      username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
      password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      // captcha: [{ required: true, message: "请输入验证码", trigger: "blur" }],
    };

    // const loading = ref(false);
    // const captchaSrc = ref("/api/captcha"); // 验证码图片地址

    // const refreshCaptcha = () => {
    //   captchaSrc.value = `/api/captcha?${new Date().getTime()}`;
    // };

    const handleLogin = () => {   // 表单验证
      console.log(5);
      console.log("123456");
      // const loginForm = ref("loginForm");
      try{axios.post("/auth/login", form,{
                    withCredentials: true  // 确保每个请求都带上 cookie
                }).then((res) => {
            // loading.value = true;
            console.log(1);
            console.log("798879");
            console.log(res.data.sucess);
            console.log(res.data.message);
            if (res.data.sucess == true) {
              ElMessage.success("登录成功");
              const homeUrl = window.location.href.replace(/\/login$/, "/home");
              setTimeout(() => {
                window.location.href = homeUrl; 
              }, 1000); // 等待 1 秒
            } else {
              ElMessage.error(res.data.message || "登录失败");
              // refreshCaptcha();
            }
          })
      }catch(error){
            // loading.value = false;
            ElMessage.error(error.message || "请求出错");
            // refreshCaptcha();
      }
    };

    return {
      form,
      rules,
      // loading,
      // captchaSrc,
      // refreshCaptcha,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}
.login-card {
  width: 400px;
}
.login-title {
  text-align: center;
  margin-bottom: 20px;
}
.captcha-img-container {
  text-align: center;
  cursor: pointer;
}
</style>
