<template>
    <div class="profile-courses">
        <strong>参与课程</strong>
        <!-- 课程列表 -->
        <el-table :data="paginatedCourses" style="width: 100%">
            <el-table-column prop="course_name" label="课程名称" width="150"></el-table-column>
            <el-table-column prop="dept" label="院系" width="150"></el-table-column>
            <el-table-column prop="teacher_name" label="任课教师" width="120"></el-table-column>
            <el-table-column prop="created_at" label="选课时间" width="240"></el-table-column>
        </el-table>

        <!-- 分页部分 -->
        <el-pagination :page-size="pageSize" :current-page="currentPage" :total="courses.length"
            layout="prev, pager, next, jumper" @current-change="handlePageChange"></el-pagination>
    </div>
</template>

<script>
import { ElTable, ElTableColumn, ElPagination } from 'element-plus';
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
    name: 'ProfileCourses',
    components: {
        ElTable,
        ElTableColumn,
        ElPagination
    },
    data() {
        return {
            courses: [],  // 存储课程数据
            pageSize: 10, // 每页显示 10 条数据
            currentPage: 1 // 当前页
        };
    },
    created() {
        this.fetchCourses();  // 获取课程数据
    },
    computed: {
        // 分页数据
        paginatedCourses() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.courses.slice(start, end);  // 返回当前页的数据
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
        };
    },
    methods: {
        // 获取课程列表
        async fetchCourses() {
            const route = useRoute();
            const userId = route.params.user_id;
            try {
                const response = await axios.get(`/auth/profile${userId}`);  // 获取课程数据接口
                this.courses = response.data.courses;  // 假设返回的接口数据包含课程列表
                this.courses.forEach(course => {
                    course.created_at = this.Timetrans(course.created_at);  // 格式化时间
                });
            } catch (error) {
                console.error('获取课程数据失败', error);
            }
        },

        // 分页处理
        handlePageChange(page) {
            this.currentPage = page;  // 更新当前页
        }
    }
};
</script>

<style scoped>
.profile-courses {
    width: 75%;
    padding: 20px;
}

.el-table {
    width: 100%;
    margin-top: 20px;
}

.chart-title {
    font-size: 22px;
    margin-top: 30px;
    margin-bottom: 20px;
}

.loading-text {
    text-align: center;
    font-size: 18px;
    color: #888;
}
</style>