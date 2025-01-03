<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <el-container class="login-title">
        <img src="../assets/img/personal_icon.png" class="logo">
        <h1>高校论坛平台登录</h1>
      </el-container>
      <el-form :model="form" :rules="rules" label-width="100px">
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
              <!-- <el-icon><user /></el-icon> -->
            </template>
          </el-input>
        </el-form-item>

        <!-- 密码 -->
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" placeholder="请输入密码" show-password>
            <template #prefix>
              <!-- <el-icon><lock /></el-icon> -->
            </template>
          </el-input>
        </el-form-item>

        <!-- 验证码 -->
        <!-- <el-form-item label="验证码" prop="captcha">
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

        <!-- 登录和注册按钮 -->
        <el-form-item>
          <el-row :gutter="0">
            <el-col :span="12">
              <el-button type="default" @click="handleLogin" plain block>
                登录
              </el-button>
            </el-col>
            <el-col :span="12">
              <el-button type="default" @click="handleRegister" plain block>
                没有账号，前往注册
              </el-button>
            </el-col>
          </el-row>
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
      // const loginForm = ref("loginForm");
      try {
        if (form.userType == "admin") {
          axios.post("/auth/admin_login", form).then((res) => {
            console.log(res.data.message);
            if (res.data.sucess == true) {
              ElMessage.success("登录成功");
              const homeUrl = window.location.href.replace(/\/admin_login$/, "/admin_home");
              setTimeout(() => {
                window.location.href = homeUrl;
              }, 1000); // 等待 1 秒
            } else {
              ElMessage.error(res.data.message || "登录失败");
              // refreshCaptcha();
            }
          })
        }
        else {
          axios.post("/auth/login", form).then((res) => {
            // loading.value = true;
            console.log(res.data.message);
            if (res.data.success == true) {
              ElMessage.success({
                message: "登录成功", duration: 1200,
                onClose: () => {
                  const Url = window.location.href.replace(/\/login$/, "/home");
                  window.location.href = Url;
                }
              });
            } else {
              ElMessage.error(res.data.message || "登录失败");
              // refreshCaptcha();
            }
          })
        }
      } catch (error) {
        // loading.value = false;
        ElMessage.error(error.message || "请求出错");
        // refreshCaptcha();
      }
    };
    const handleRegister = () => {
      try {
        const Url = window.location.href.replace(/\/login$/, "/register");
        window.location.href = Url;
      } catch (error) {
        ElMessage.error(error.message || "请求出错");
      }
    };

    return {
      form,
      rules,
      // loading,
      // captchaSrc,
      // refreshCaptcha,
      handleLogin,
      handleRegister,
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
  background: url('../assets/img/background.jpg');
  background-size: cover;
}

.login-card {
  width: 410px;
}

.login-title {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  flex-grow: 0;
}

.login-title h1 {
  font-size: 22px;
  line-height: 22px;
  margin: 0;
  margin-left: 5px;
  font-weight: 500;
}

/* .captcha-img-container {
  text-align: center;
  cursor: pointer;
} */
.logo {
  width: 50px;
  height: 50px;
}
</style>
