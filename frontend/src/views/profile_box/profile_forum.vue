<template>
    <div class="admin-forum">
        <strong>论坛记录</strong>
        <el-table :data="paginatedData" style="width: 100%">
            <el-table-column prop="forum_id" label="forum_ID" width="90"></el-table-column>
            <el-table-column prop="forum_name" label="论坛名称" width="150"></el-table-column>
            <el-table-column prop="description" label="论坛描述" width="180">
                <template v-slot="scope">
                    <span>{{ formatDescription(scope.row.description) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="240">
                <template v-slot="scope">
                    <el-button @click="goToForumDetail()" type="primary" size="small">跳转</el-button>
                    <el-button @click="transferForum(scope.row.forum_id)" type="warning" size="small">转让</el-button>
                    <el-button @click="deleteForum(scope.row.forum_id)" type="danger" size="small">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页部分 -->
        <el-pagination :page-size="pageSize" :current-page="currentPage" :total="forums.length"
            layout="prev, pager, next, jumper" @current-change="handlePageChange">
        </el-pagination>
    </div>
</template>

<script>
import { ElTable, ElTableColumn, ElPagination, ElButton } from 'element-plus';
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
    name: 'ProfileForum',
    components: {
        ElTable,
        ElTableColumn,
        ElPagination,
        ElButton
    },
    data() {
        return {
            forums: [],  // 存储论坛数据
            pageSize: 10, // 每页显示 10 条数据
            currentPage: 1 // 当前页
        };
    },
    created() {
        this.fetchForums();  // 获取论坛数据
    },
    computed: {
        // 分页数据
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.forums.slice(start, end);  // 返回当前页的数据
        }
    },
    methods: {
        // 格式化论坛描述，超过50个字符显示省略号
        formatDescription(description) {
            if (description.length > 30) {
                return description.slice(0, 30) + '...';
            }
            return description;
        },
        // 分页页码变更处理
        handlePageChange(page) {
            this.currentPage = page;  // 更新当前页
        },
        // 获取论坛列表数据
        async fetchForums() {
            const route = useRoute();
            const userId = route.params.user_id; // 获取userId
            try {
                const response = await axios.get(`/auth/profile${userId}`);  // 调用后端接口获取论坛数据
                this.forums = response.data.forums;  // 假设接口返回的数据是论坛列表
            } catch (error) {
                console.error('获取论坛数据失败', error);
            }
        },
        // 跳转到论坛详情页面
        goToForumDetail() {
            this.$router.push('/home');
        },
        // 转让论坛
        transferForum(forumId) {
            // 此处可以弹出一个确认框或者进一步操作
            this.$confirm('确认转让该论坛吗?', '提示', {
                type: 'warning',
            }).then(() => {
                console.log('论坛转让:', forumId);
                // 在这里处理转让逻辑

            }).catch(() => {
                console.log('取消转让');
            });
        },
        // 删除论坛
        async deleteForum(forumId) {
            this.$confirm('确认删除该论坛吗?', '提示', {
                type: 'danger',
            }).then(async () => {
                console.log('论坛删除:', forumId);
                try {
                    const response = await axios.post(`/safe_delete_forum${forumId}`);
                    if (response.data.success !== true) {
                        this.$message.error(response.data.message || '删除论坛失败');
                    }
                    this.$message.success('删除成功');
                } catch (error) {
                    console.error('删除帖子失败', error);
                    this.$message.error('删除失败');
                }
            }).catch(() => {
                console.log('取消删除');
            });
        }
    }
};
</script>

<style scoped>
.admin-forum {
    width: 75%;
    padding: 20px;
}

.el-table {
    width: 100%;
    margin-top: 20px;
}

.el-button {
    margin-right: 10px;
}
</style>