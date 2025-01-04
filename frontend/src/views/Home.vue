<template>
    <div class="home-container">
        <!-- 顶部标题栏 -->
        <el-header class="header">
            <div class="header-title">
                高校论坛平台
            </div>
        </el-header>
        <!-- 操作栏 -->
        <el-header class="action-bar">
            <el-select v-model="selectedBlockId" placeholder="请选择版块" class="block-selector" @change="handleBlockChange">
                <el-option label="总版块" :value="null" />
                <el-option v-for="block in forumBlocks" :key="block.forum_id" :label="block.forum_name"
                    :value="block.forum_id" />
            </el-select>
            <el-input class="action-search" placeholder="搜索帖子或内容" v-model="searchQuery" clearable
                prefix-icon="el-icon-search" @keyup.enter="handleSearch" />
            <el-button type="primary" @click="goToRoute('/post_create')">发布帖子</el-button>
            <el-button type="primary" @click="submitApply()">申请版块</el-button>
            <el-dropdown trigger="click">
                <span class="avatar-dropdown">
                    <el-avatar src="person.ico" />
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="goToRoute('/profile')">个人界面</el-dropdown-item>
                        <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </el-header>
        <!-- 主体布局 -->
        <el-container class="main-content">
            <el-main class="content">
                <div v-if="selectedBlockId" class="section-description">
                    <span>版块简介：{{ Description }}</span>
                </div>
                <el-row :gutter="20" v-for="post in paginatedPosts" :key="post.post_id">
                    <el-col :span="24" class="post-card">
                        <el-card shadow="hover">
                            <h3 class="post-title" @click="goToPostDetail(post.post_id)">
                                {{ post.title.length > 10 ? post.title.slice(0, 10) + '...' : post.title }}
                            </h3>
                            <p style="font-size: 1em">
                                {{ post.body.length > 15
                                    ? post.body.slice(0, 15) + '...'
                                    : post.body }}
                            </p>
                            <div class="post-stats">
                                <span>👤{{ post.nickname.length > 10 ? post.nickname.slice(0, 10) + '...' :
                                    post.nickname
                                    }}</span>
                                <span>👍 {{ post.liked }}</span>
                                <span>💬 {{ post.commented }}</span>
                                <span>发表时间： {{ Timetrans(post.created) }}</span>
                                <span>更新时间：{{ Timetrans(post.updated) }}</span>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="totalPosts"
                    v-model:page-size="pageSize" v-model:current-page="currentPage" :page-sizes="[5, 10, 20, 50]"
                    @current-change="updatePagination" @size-change="updatePagination" />
            </el-main>
        </el-container>
    </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import router from '@/router/Router.js'
import { ElMessageBox, ElMessage } from "element-plus";

export default {
    name: "Home_Page",
    setup() {
        const searchQuery = ref("");
        const forumBlocks = ref([]);
        const selectedBlockId = ref(null);
        const displayedPosts = ref([]);
        const totalPosts = ref(0);
        const currentPage = ref(1);
        const pageSize = ref(5);
        const Description = ref("");
        const title = ref('');
        const description = ref('');

        // 计算当前页显示的帖子
        const paginatedPosts = computed(() => {
            const start = (currentPage.value - 1) * pageSize.value;
            const end = start + pageSize.value;
            return displayedPosts.value.slice(start, end);
        });
        const submitApply = async () => {
            ElMessageBox({
                title: '创建板块',
                message: `
                    <div>
                        <div>
                        <label for="title">版块名称:</label>
                        <input id="title" placeholder="请输入版块名称"></input>
                        </div>
                        <div>
                        <label for="description">版块描述:</label>
                        <input id="description" type="textarea" placeholder="请输入版块描述"></input>
                        </div>
                    </div>
                `,
                dangerouslyUseHTMLString: true, // 允许使用 HTML 字符串
                showCancelButton: true,
                confirmButtonText: "提交申请",
                cancelButtonText: "取消",
                beforeClose: (action, instance, done) => {
                    if (action === 'confirm') {
                        const titleValue = document.getElementById("title").value;
                        const descriptionValue = document.getElementById("description").value;
                        if (!titleValue || !descriptionValue) {
                            ElMessage({
                                type: 'warning',
                                message: '标题和描述都不能为空！',
                            });
                            done();
                            return;
                        }
                        title.value = titleValue;
                        description.value = descriptionValue;
                        submitForum(title.value, description.value);
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
        const submitForum = async (title, description) => {
            try {

                const response = await axios.post('/apply_forum', { 'forum_name':title, 'description':description });
                if(response.data.success !== true){                    
                    ElMessage.error(response.data.message || '提交申请失败');
                }else{
                    ElMessage.success('提交申请成功');
                }
                
            } catch (error) {
                console.error('申请失败:', error);
                ElMessage({
                    type: 'error',
                    message: '提交申请失败，请重试',
                });
            }
        };

        const fetchForumBlocks = async () => {
            try {
                const response = await axios.get("/get_forums");
                forumBlocks.value = response.data;
            } catch (error) {
                console.error("获取论坛版块数据失败：", error);
            }
        };

        const fetchPosts = async () => {
            try {
                var tip = "/";
                if (selectedBlockId.value == null) {
                    tip = "/";
                    Description.value = "";
                }
                else {
                    tip = "/forum" + selectedBlockId.value;
                    Description.value = forumBlocks.value[selectedBlockId.value - 1].description;
                    console.log(Description.value);
                }
                const response = await axios.get(tip);
                displayedPosts.value = response.data;
                totalPosts.value = response.data.length;
            } catch (error) {
                console.error("获取帖子数据失败：", error);
            }
        };
        //转换时间显示格式
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
        const updatePagination = () => { };

        const handleBlockChange = () => {
            currentPage.value = 1;
            fetchPosts();
        };
        const handleLogout = () => {
            try {
                axios.post("/auth/logout").then((res) => {
                    console.log(res.data.message);
                    if (res.data.success == true) {
                        ElMessage.success({
                            message: "登出成功", duration: 1200,
                            onClose: () => {
                                const Url = window.location.href.replace(/\/home$/, "/login");
                                window.location.href = Url;
                            }
                        });
                    } else { ElMessage.error(res.data.message || "登出失败"); }
                })
            } catch (error) { ElMessage.error(error.message || "请求出错"); }
        };

        const handleSearch = () => {
            alert(`搜索：${searchQuery.value}`);
        };

        const goToRoute = (route) => {
            router.push(route);
        };

        const goToPostDetail = (postId) => {
            // router.push("/post/"+postId);
            router.push({ path: '/post', query: { id: postId } })
        };

        onMounted(() => {
            fetchForumBlocks();
            fetchPosts();
        });

        return {
            searchQuery,
            forumBlocks,
            selectedBlockId,
            displayedPosts,
            totalPosts,
            currentPage,
            pageSize,
            fetchPosts,
            handleBlockChange,
            handleLogout,
            handleSearch,
            goToRoute,
            goToPostDetail,
            Timetrans,
            updatePagination,
            paginatedPosts,
            Description,
            submitApply
        };
    },
};
</script>

<style scoped>
.home-container {
    width: 75%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    background-color: #f5f5f5;
}

.header {
    background-image: url('../assets/img/headline_bg.jpg');
    background-size: cover;
    background-position: center;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
}

.header-title {
    font-size: 3em;
    font-weight: bold;
}

.action-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background-color: #004f9f;
}

.block-selector {
    width: 200px;
}

.action-search {
    flex: 1;
    margin: 0 20px;
}

.avatar-dropdown {
    margin: 0 20px;
    cursor: pointer;
}

.main-content {
    padding: 20px;
}

.content {
    overflow-y: auto;
}

.post-card {
    margin-bottom: 20px;
}

.post-title {
    cursor: pointer;
    color: #007dfa;
    transition: color 0.3s;
}

.post-title:hover {
    color: #66b1ff;
}

.post-stats {
    display: flex;
    justify-content: space-between;
    font-size: 0.9em;
    color: #606266;
}

.section-description {
    font-size: 14px;
    color: #000000;
    background-color: #ffffff;
    padding: 10px 20px;
    /* 上下10px，左右20px内边距 */
    border-radius: 5px;
    max-width: 100%;
    margin-top: 0px;
    margin-bottom: 30px;
    /* 居中对齐 */
    font-style: italic;
    /* 增加轻微阴影美观 */
}
</style>
