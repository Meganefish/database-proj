<template>
    <div class="post-container">
        <span class="back-button" @click="BackToHome">{{ "↩️返回" }}</span>
        <el-header class="header">
            <div class="header-title">
                {{ post_info.title }}<br>
            </div>
        </el-header>
        <el-header class="header">
            <div class="auther-subtitle">
                <span class="author-name" @click="goToUserDetail(post_info.user_id)">
                    作者:{{ post_info.nickname }}
                </span>
                <span>所属版块：{{ post_info.forum_name }}</span>
                <span>发表时间： {{ post_info.created }}</span>
                <span>更新时间：{{ post_info.updated }}</span>
            </div>
        </el-header>
        <el-main class="content">
            <div class="post-content">
                <p v-for="(paragraph, index) in formattedContent" :key="index">
                    {{ paragraph }}
                </p>
            </div>
        </el-main>
        <div class="actions">
            <el-button @click="likePost" :type="post_info.like_or_not ? 'primary' : 'default'">
                <span class="highlight">{{ '🖒' }}</span> ({{ post_info.liked }})
            </el-button>
            <el-button :type="reportingTo_p ? 'info' : 'warning'"
                @click="showReportBox_p()">举报</el-button>
            <el-button v-if="yourid === post_info.user_id" type="success"
                @click="editPost(post_info.post_id)">编辑</el-button>
            <el-button v-if="yourid === post_info.user_id" type="danger" @click="deletePost">删除</el-button>
        </div>
        <!--举报框-->
        <div v-if="reportingTo_p" class="reply_box">
            举报理由：
            <el-input v-model="reportContent_p" placeholder="感谢你为维护论坛贡献的一份力量"
                @keyup.enter="submitReport(0)"></el-input>
            <el-button @click="submitReport(0)">提交</el-button>
        </div>
        <hr>
        <div>
            <h2>评论区 ({{ comment_info.length }} 条评论)</h2>
            <div class="comment_action">
                <el-input v-model="newComment" placeholder="良言一句三冬暖，恶语伤人六月寒" @keyup.enter="postComment(0)"></el-input>
                <el-button type="primary" @click="postComment(0)">发布</el-button>
            </div>
            <div v-for="comment in comment_info" :key="comment.comment_id">
                <span class="comment-author-name" @click="goToUserDetail(comment.user_id)">
                    <br>{{ comment.nickname }}:<br>
                </span>
                <div class="comment-content">
                    <div class="parent_comment" v-if="comment.parent_comment_id">
                        {{ comment_info.find(c => c.comment_id === comment.parent_comment_id).body.length > 10
                            ?
                            comment_info.find(c => c.comment_id === comment.parent_comment_id).body.slice(0, 10) +
                            '...' :
                            comment_info.find(c => c.comment_id === comment.parent_comment_id).body }}
                    </div>
                    <span style="cursor: pointer;font-weight:bold; color: red;" v-if="comment.parent_comment_id"
                        @click="goToUserDetail(comment_info.find(c => c.comment_id === comment.parent_comment_id).user_id)">
                        {{ "@" + comment_info.find(c => c.comment_id === comment.parent_comment_id).nickname }}
                    </span>
                    {{ comment.body }}<br>
                </div>
                <div class="comment_button">
                    <span>
                        <el-button @click="likeComment(comment.comment_id)"
                            :type="comment.like_or_not ? 'primary' : 'default'">
                            <span class="highlight">{{ '🖒' }}</span> ({{ comment.liked }})
                        </el-button>
                        <el-button :type="reportingTo_c === comment.comment_id ? 'info' : 'warning'"
                            @click="showReportBox_c(comment.comment_id)">举报</el-button>
                        <el-button :type="replyingTo === comment.comment_id ? 'info' : 'success'"
                            @click="showReplyBox(comment.comment_id)">回复</el-button>
                        <el-button v-if="yourid === comment.user_id" type="danger" @click="deleteComment">删除</el-button>
                    </span>
                </div>
                <!-- 回复框 -->
                <div v-if="replyingTo === comment.comment_id" class="reply_box">
                    <el-input v-model="replyContent" :placeholder="'回复@' + comment.nickname"
                        @keyup.enter="postComment(comment.comment_id)"></el-input>
                    <el-button @click="postComment(comment.comment_id)">发布</el-button>
                </div>
                <!--举报框-->
                <div v-if="reportingTo_c === comment.comment_id" class="reply_box">
                    举报理由：
                    <el-input v-model="reportContent_c" placeholder="感谢你为维护论坛贡献的一份力量"
                        @keyup.enter="submitReport(1)"></el-input>
                    <el-button @click="submitReport(1)">提交</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import axios from "axios";
import router from '@/router/Router.js';
import { ElMessage } from "element-plus";

export default {
    name: 'DetailPage',
    setup() {
        const route = useRoute();
        const postId = ref(null);
        const post_info = ref({});
        const comment_info = ref([]);
        const newComment = ref('');
        const replyingTo = ref(null);
        const reportingTo_c = ref(null);
        const reportingTo_p = ref(false);
        const replyContent = ref('');
        const reportContent_c = ref('');
        const reportContent_p = ref('');

        const yourid = ref(0); // 当前用户是否是作者
        // 获取帖子详情
        onMounted(async () => {
            postId.value = route.query.id;
            getPostDetails();
            console.log(post_info.value.updated);
        });
        const getPostDetails = async () => {
            try {
                const response = await axios.get("/post" + postId.value);
                post_info.value = response.data.post;
                comment_info.value = response.data.comment;
                post_info.value.created = Timetrans(post_info.value.created);
                post_info.value.updated = Timetrans(post_info.value.updated);
                const response2 = await axios.get("/get_logged_user");
                yourid.value = response2.data.user_id;
            } catch (error) {
                console.error("获取数据失败：", error);
            }
        };
        const formattedContent = computed(() =>
            String(post_info.value.body).split("\n").filter((p) => p.trim())
        );
        const goToUserDetail = (UserId) => {
            router.push(`/profile/user${UserId}`);
        };

        const BackToHome = () => {
            router.push({ path: '/home' });
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

        const likePost = async () => {
            try {
                await axios.post("/post" + postId.value + "/click_like");
            } catch (error) {
                console.error("获取数据失败：", error);
            }
            post_info.value.like_or_not = !post_info.value.like_or_not;
            post_info.value.liked += post_info.value.like_or_not ? 1 : -1;
        };

        const editPost = (PostId) => {
            router.push({ path: '/post_edit', query: { id: PostId } });
        }


        // 发布评论
        const postComment = async (pcid) => {
            try {
                const form = reactive({ body: newComment.value, });
                var tip = "/post" + postId.value + "/release_comment";
                if (!pcid) { tip += "0"; if (!newComment.value.trim()) return; }
                else { if (!replyContent.value.trim()) return; tip += pcid; form.body = replyContent.value; replyingTo.value = 0; }
                axios.post(tip, form).then((res) => {
                    console.log(res.data.message);
                    if (res.data.success == true) {
                        ElMessage.success({
                            message: res.data.message, duration: 1200,
                            onClose: () => {
                                getPostDetails();
                                if (!pcid) { newComment.value = ''; }
                                else { replyContent.value = ''; }
                            }
                        });
                    } else { ElMessage.error(res.data.message || "评论失败"); }
                })
            } catch (error) {
                console.error("获取数据失败：", error);
            }
        };

        // 点赞评论
        const likeComment = async (commentId) => {
            try {
                await axios.get("/comment" + commentId + "/click_like");
            } catch (error) {
                console.error("获取数据失败：", error);
            }
            const comment = comment_info.value.find(c => c.comment_id === commentId);
            comment.like_or_not = !comment.like_or_not;
            comment.liked += comment.like_or_not ? 1 : -1;
        };
        //回复评论
        const showReplyBox = (commentId) => {
            if (replyingTo.value == commentId) { replyingTo.value = null; }
            else { replyingTo.value = commentId; }
            replyContent.value = "";
        };
        const showReportBox_c = (commentId) => {
            if (reportingTo_c.value == commentId) { reportingTo_c.value = null; }
            else { reportingTo_c.value = commentId; }
            reportContent_c.value = "";
        };
        const showReportBox_p = () => {
            if (reportingTo_p.value) { reportingTo_p.value = 0; }
            else { reportingTo_p.value = 1; }
            reportContent_p.value = "";
        };

        const submitReport = async (c_flag) => {
            try {
                const form = reactive({ reason: reportContent_c.value, });
                var tip = "/submit_report_";
                if (c_flag) {
                    tip += "comment" + reportingTo_c.value;
                    if (!reportContent_c.value.trim()) return;
                    reportingTo_c.value = 0;
                }
                else {
                    if (!reportContent_p.value.trim()) return;
                    tip += "post" + post_info.value.post_id;
                    form.reason = reportContent_p.value;
                    reportingTo_p.value = 0;
                }
                axios.post(tip, form).then((res) => {
                    console.log(res.data.message);
                    if (res.data.success == true) {
                        ElMessage.success({
                            message: res.data.message, duration: 1200,
                            onClose: () => {
                                getPostDetails();
                                if (c_flag) { reportContent_c.value = ''; }
                                else { reportContent_p.value = ''; }
                            }
                        });
                    } else { ElMessage.error(res.data.message || "评论失败"); }
                })
            } catch (error) {
                console.error("获取数据失败：", error);
            }
        };

        return {
            post_info,
            comment_info,
            newComment,
            likePost,
            postComment,
            likeComment,
            submitReport,
            Timetrans,
            goToUserDetail,
            BackToHome,
            formattedContent,
            yourid,
            editPost,
            showReplyBox,
            showReportBox_c,
            showReportBox_p,
            replyingTo,
            replyContent,
            reportingTo_c,
            reportingTo_p,
            reportContent_c,
            reportContent_p,
        };
    }
};
</script>

<style scoped>
.post-container {
    width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    background-color: #ffffff;
}

.header {
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #000000;
}

.back-button {
    height: 10px;
    color: #000000;
    cursor: pointer;
    align-items: center;
    justify-content: flex-start;
}

.comment_button {
    margin: 20px auto;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.header-title {
    font-size: 2em;
    font-weight: bold;
}

.auther-subtitle {
    height: 10px;
    font-size: 0.6em;
    color: #00000061;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
}

.author-name {
    color: blue;
    cursor: pointer;
    text-decoration: underline;
}

.comment-author-name {
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

.comment-content {
    font-style: oblique;
    margin: 0px auto;
    background-color: #f9f9f9af;
    border: 1px solid #ddd;
    font-size: 16px;
    line-height: 1.6;
    text-indent: 1em;
    padding: 10px 40px;
    overflow-y: auto;
}

.content {
    width: 800px;
    margin: 0px auto;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    line-height: 1.6;
    text-indent: 2em;
    /* 设置段首空两格 */
    padding: 10px 40px;
    overflow-y: auto;
}

.actions {
    margin: 20px auto;
    display: flex;
    gap: 10px;
    justify-content: flex-start;
    /* margin-bottom: 20px; */
}

.comment_action {
    margin: 20px auto;
    display: flex;
    gap: 10px;
    justify-content: flex-start;
    font-size: 10px;
}

.comments {
    margin-top: 20px;
    margin-bottom: 10px;
}

.highlight {
    font-size: 24px;
    /* 放大部分字体大小 */
}

.parent_comment {
    font-style: italic;
    font-weight: lighter;
    margin: 0px auto;
    background-color: #e8e6d0;
    font-size: 16px;
    line-height: 1.6;
    text-indent: 1em;
    padding: 10px 0px;
    overflow-y: auto;
}

.reply_box {
    width: 100%;
    white-space: nowrap;
    vertical-align: middle;
    margin-top: 10px;
    display: flex;
    gap: 10px;
    /* justify-content: center; */
}
</style>