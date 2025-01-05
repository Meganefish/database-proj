<template>
    <div v-if="user" class="profile-container">
        <h1 class="profile-title">个人资料</h1>

        <!-- 用户信息显示部分 -->
        <div class="profile-info">
            <p><strong>用户名:</strong> {{ user.username }}</p>
            <p><strong>昵称:</strong> {{ user.nickname }}</p>
            <p><strong>年级:</strong> {{ user.grade }}</p>
            <p><strong>专业:</strong> {{ user.major }}</p>
            <p><strong>创建时间:</strong> {{ trans_created_at }}</p>
        </div>

        <!-- 如果当前用户是登录用户，显示编辑功能 -->
        <div v-if="loggedUser && loggedUser.user_id === user.user_id" class="profile-edit">
            <div class="input-group">
                <label for="username">用户名:</label>
                <input v-model="editedUser.username" id="username" type="text" disabled />
            </div>
            <div class="input-group">
                <label for="nickname">昵称:</label>
                <input v-model="editedUser.nickname" id="nickname" type="text" placeholder="请输入新的昵称" />
                <button @click="edit_nickname('nickname')">提交</button>
            </div>
            <div class="input-group">
                <label for="grade">年级:</label>
                <input v-model="editedUser.grade" id="grade" type="text" placeholder="请输入新的年级" />
                <button @click="edit_grade('grade')">提交</button>
            </div>
            <div class="input-group">
                <label for="major">专业:</label>
                <input v-model="editedUser.major" id="major" type="text" placeholder="请输入新的专业" />
                <button @click="edit_major('major')">提交</button>
            </div>
            <div class="input-group">
                <label for="created_at">创建时间:</label>
                <input v-model="trans_created_at" id="created_at" type="text" disabled />
            </div>
            <div class="button-group">
                <button @click="reset_password" class="reset-password-button">重设密码</button>
                <button @click="logout" class="logout-button">退出登录</button>
            </div>
        </div>
    </div>

    <div v-else>
        <p class="loading-text">加载中...</p>
    </div>
</template>

<script>
import axios from 'axios';
import { ElMessageBox, ElMessage } from 'element-plus';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
    name: 'ProfileUser',
    setup() {
        const user = ref(null);
        const loggedUser = ref(null);
        const editedUser = ref({
            username: '',
            nickname: '',
            grade: '',
            major: '',
            created_at: ''
        });
        const trans_created_at = ref(null);
        const route = useRoute();

        const userId = route.params.user_id;

        // 获取用户信息
        const getUserProfile = async () => {
            try {
                const response = await axios.get(`/auth/profile${userId}`);
                user.value = response.data.user;
                trans_created_at.value = Timetrans(user.value.created_at);
                editedUser.value = { ...user.value }; // 初始化编辑用户信息
            } catch (error) {
                console.error('获取用户资料失败:', error);
            }
        };

        // 获取登录用户信息
        const getLoggedUser = async () => {
            try {
                const response = await axios.get('/get_logged_user');
                loggedUser.value = response.data;
            } catch (error) {
                console.error('获取登录用户失败:', error);
            }
        };
        const edit_nickname = async () => {
            try {
                const response = await axios.post('auth/set_nickname', {
                    nickname: editedUser.value.nickname
                });
                if (response.data.success === true) {
                    ElMessage.success('更新成功');
                    setTimeout(() => {
                        location.reload(); // 强制刷新页面
                    }, 500);
                }
                else {
                    ElMessage.error(response.data.message || '更新失败');
                }
            } catch (error) {
                console.error('更新失败:', error);
                alert('更新失败');
            }
        };
        const edit_grade = async () => {
            try {
                const response = await axios.post('auth/set_grade', {
                    grade: editedUser.value.grade
                });
                if (response.data.success === true) {
                    ElMessage.success('更新成功');
                    setTimeout(() => {
                        location.reload(); // 强制刷新页面
                    }, 500);
                }
                else {
                    ElMessage.error(response.data.message || '更新失败');
                }
            } catch (error) {
                console.error('更新失败:', error);
                alert('更新失败');
            }
        };
        const edit_major = async () => {
            try {
                const response = await axios.post('auth/set_major', {
                    major: editedUser.value.major
                });
                if (response.data.success === true) {
                    ElMessage.success('更新成功');
                    setTimeout(() => {
                        location.reload(); // 强制刷新页面
                    }, 500);
                }
                else {
                    ElMessage.error(response.data.message || '更新失败');
                }
            } catch (error) {
                console.error('更新失败:', error);
                alert('更新失败');
            }
        };

        const reset_password = async () => {
            ElMessageBox({
                title: '重设密码',
                message: `
                    <div>
                        <div>
                        <label for="old_password">旧密码:&nbsp;&nbsp;</label>
                        <input id="old_password" type="password" placeholder="请输入旧密码"></input>
                        </div>
                        <div>
                        <label for="new_password">新密码:&nbsp;&nbsp;</label>
                        <input id="new_password" type="password" placeholder="请输入新密码"></input>
                        </div>
                        <div>
                        <label for="new_password_again">重复新密码:</label>
                        <input id="new_password_again" type="password" placeholder="请再次输入新密码"></input>
                        </div>
                    </div>
                `,
                dangerouslyUseHTMLString: true, // 允许使用 HTML 字符串
                showCancelButton: true,
                confirmButtonText: "重设密码",
                cancelButtonText: "取消",
                beforeClose: (action, instance, done) => {
                    if (action === 'confirm') {
                        const oldPasswordValue = document.getElementById("old_password").value;
                        const newPassordValue = document.getElementById("new_password").value;
                        const newPassordAgainValue = document.getElementById("new_password_again").value;
                        if (!oldPasswordValue || !newPassordValue || !newPassordAgainValue) {
                            ElMessage({
                                type: 'warning',
                                message: '旧密码和新密码都不能为空！',
                            });
                            done();
                            return;
                        }
                        if (newPassordValue !== newPassordAgainValue) {
                            ElMessage({
                                type: 'warning',
                                message: '两次输入的新密码不一致！',
                            });
                            done();
                            return;
                        }
                        submitResetPassword(oldPasswordValue, newPassordValue);
                    }
                    done();
                }
            })
                .catch(() => {
                    ElMessage({
                        type: "info",
                        message: "申请已取消",
                    });
                });
        };

        const submitResetPassword = async (oldPassword, newPassword) => {
            try {
                const response = await axios.post('/auth/reset_password', {
                    old_password: oldPassword,
                    new_password: newPassword
                });

                if (response.data.success === true) {
                    ElMessage.success('密码重设成功');
                } else {
                    ElMessage.error(response.data.message || '密码重设失败');
                }
            } catch (error) {
                console.error('密码重设失败:', error);
                alert('密码重设失败');
            }
        };

        // 退出登录
        const logout = async () => {
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
        };
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

        onMounted(() => {
            getUserProfile();
            getLoggedUser();
        });

        return {
            user,
            loggedUser,
            trans_created_at,
            editedUser,
            edit_nickname,
            edit_grade,
            edit_major,
            reset_password,
            logout,
            Timetrans
        };
    }
};
</script>

<style scoped>
/* 样式调整 */
.profile-container {
    width: 75%;
    margin: 0 auto;
    padding: 20px;
}

.profile-title {
    font-size: 24px;
    margin-bottom: 20px;
}

.profile-info {
    font-size: 16px;
    color: #333;
}

.input-group {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.input-group input {
    width: 70%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.input-group button {
    padding: 8px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.input-group button:hover {
    background-color: #45a049;
}
.button-group {
    display: flex;
    margin: 0 auto;
    justify-content: center; 
    gap: 40px; 
}

.logout-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.reset-password-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.logout-button:hover {
    background-color: #e53935;
}

.rest-password-button:hover {
    background-color: #45a049;
}

.loading-text {
    text-align: center;
    font-size: 18px;
    color: #888;
}
</style>