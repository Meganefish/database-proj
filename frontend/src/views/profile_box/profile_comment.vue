<template>
    <div class="admin-comment">
        <strong>评论记录</strong>
        <el-table :data="paginatedData" style="width: 100%">
            <el-table-column prop="comment_id" label="comment_ID" width="120"></el-table-column>
            <el-table-column prop="body" label="评论内容" width="320">
                <template v-slot="scope">
                    <!-- 通过计算显示帖子内容，限制为20个字，超过则显示... -->
                    <span>{{ formatcommentBody(scope.row.body) }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="created_at" label="评论创建时间" width="240"></el-table-column>
        </el-table>

        <!-- 分页部分 -->
        <el-pagination :page-size="pageSize" :current-page="currentPage" :total="comments.length"
            layout="prev, pager, next, jumper" @current-change="handlePageChange">
        </el-pagination>
    </div>
</template>

<script>
import { ElTable, ElTableColumn, ElPagination } from 'element-plus';
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
    name: 'AdminComment',
    components: {
        ElTable,
        ElTableColumn,
        ElPagination
    },
    data() {
        return {
            comments: [],  // 存储帖子数据
            pageSize: 10, // 每页显示 10 条数据
            currentPage: 1 // 当前页
        };
    },
    created() {
        this.fetchcomments();  // 获取帖子数据
    },
    computed: {
        // 分页数据
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.comments.slice(start, end);  // 返回当前页的数据
        }
    },
    setup() {
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
        return {
            Timetrans
        }
    },
    methods: {
        formatcommentBody(body) {
            if (body.length > 30) {
                return body.slice(0, 30) + '...';
            }
            return body;
        },
        handlePageChange(page) {
            this.currentPage = page;  // 更新当前页
        },
        // 获取帖子列表
        async fetchcomments() {
            const route = useRoute();
            const userId = route.params.user_id;
            try {
                const response = await axios.get(`/auth/profile${userId}`);  // 调用后端接口获取帖子数据
                this.comments = response.data.comments;  // 假设接口返回的数据是帖子列表
                this.comments.forEach(comment => {
                    comment.created_at = this.Timetrans(comment.created_at);  // 格式化时间
                });
            } catch (error) {
                console.error('获取帖子数据失败', error);
            }
        },
    }
};
</script>

<style scoped>
.admin-comment {
    padding: 20px;
}

.el-table {
    width: 100%;
    margin-top: 20px;
}
</style>