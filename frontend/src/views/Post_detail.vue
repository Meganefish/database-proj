<template>
    <div class="post-container">
        <div><span class="back-button" @click="BackToHome">{{ "<返回" }}</span>
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
                        <el-button type="warning" @click="reportPost">举报</el-button>
                        <el-button v-if="isAuthor" type="success" @click="editPost(post_info.post_id)">编辑</el-button>
                        <el-button v-if="isAuthor" type="danger" @click="deletePost">删除</el-button>
                    </div>

                    <hr>

                    <!-- 评论区 -->
                    <div class="comments">
                        <h2>评论区 ({{ comment_info.length }} 条评论)</h2>
                        <div class="comment_action">
                            <el-input v-model="newComment" placeholder="良言一句三冬暖，恶语伤人六月寒"
                                @keyup.enter="postComment"></el-input>
                            <el-button type="primary" @click="releaseComment">发布</el-button>
                        </div>
                        <div v-for="comment in comment_info" :key="comment.comment_id">
                            <span class="comment-author-name" @click="goToUserDetail(comment.user_id)">
                                <br>{{ comment.nickname }}:<br>
                            </span>
                            <div class="comment-content">
                                {{ comment.body }}<br>
                            </div>
                            <br>
                            <el-button @click="likeComment(comment.comment_id)"
                                :type="comment.like_or_not ? 'primary' : 'default'">
                                <span class="highlight">{{ '🖒' }}</span> ({{ comment.liked }})
                            </el-button>
                            <el-button type="warning" @click="reportComment(comment.comment_id)">举报</el-button>
                            <el-button type="success" @click="replyToComment(comment.comment_id)">回复</el-button>
                            <br>

                            <!-- 回复框 -->
                            <div v-if="comment.showReplyBox">
                                <el-input v-model="replyContent[comment.comment_id]"
                                    placeholder="回复 @{{ comment.nickname }}"
                                    @keyup.enter="submitReply(comment.comment_id)"></el-input>
                            </div>
                            <!-- 子评论 -->
                            <!-- <div v-if="comment.replies.length">
                    <div v-for="reply in comment.replies" :key="reply.id" class="reply">
                        <p>
                            <router-link :to="{ name: 'UserProfile', params: { id: reply.authorId } }">{{
                                reply.authorName }}</router-link>: {{ reply.content }}
                            <el-button @click="likeReply(reply.id)"
                                :icon="reply.liked ? 'el-icon-star-off' : 'el-icon-star-on'">
                                {{ reply.liked ? '取消点赞' : '点赞' }} ({{ reply.likesCount }})
                            </el-button>
                            <el-button @click="reportReply(reply.id)">举报</el-button>
                        </p>
                    </div>
                </div> -->
                        </div>
                    </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from "axios";
import router from '@/router/Router.js';

export default {
    name: 'DetailPage',
    setup() {
        const route = useRoute();
        const postId = ref(null);
        const post_info = ref({});
        const comment_info = ref([]);
        const newComment = ref('');
        // const replyContent = ref({});
        // const liked = ref(false);
        // const reportReason = ref('');
        // const showReportInput = ref(false);
        const isAuthor = ref(false); // 当前用户是否是作者
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
                const response2 = await axios.get("/auth/profile");
                isAuthor.value = (response2.data.user.user_id == response.data.post.user_id)
            } catch (error) {
                console.error("获取数据失败：", error);
            }
        };
        const formattedContent = computed(() =>
            String(post_info.value.body).split("\n").filter((p) => p.trim())
        );
        const goToUserDetail = (UserId) => {
            router.push({ path: '/user', query: { id: UserId } });
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

        // 点赞帖子
        const likePost = async () => {
            try {
                await axios.post("/post" + postId.value + "/click_like");
            } catch (error) {
                console.error("获取数据失败：", error);
            }
            post_info.value.like_or_not = !post_info.value.like_or_not;
            post_info.value.liked += post_info.value.like_or_not ? 1 : -1;
        };

        const editPost =(PostId) =>{
            console.log(PostId);
            console.log(post_info.value.post_id);
            router.push({ path: '/post_edit', query: { id: PostId } });
        }

        //     // 举报帖子
        //     const reportPost = async () => {
        //         // await reportPost(postId.value);
        //         // router.push({ name: 'ReportPage', params: { postId: postId.value } });
        //     };
        //     // 显示举报输入框
        // const showReportCommentInput = (commentId) => {
        //   const comment = post.value.comments.find(c => c.id === commentId);
        //   comment.showReportInput = true;
        // };

        // // 提交举报
        // const submitReport = async (commentId) => {
        //   if (!reportReason.value.trim()) return;
        //   await submitReport(postId.value, commentId, reportReason.value);
        //   reportReason.value = '';
        //   showReportInput.value = false;
        // };


        // 发布评论
        const postComment = async () => {
            // if (!newComment.value.trim()) return;
            // const comment = await postComment(postId.value, newComment.value);
            // post.value.comments.push(comment);
            // newComment.value = '';
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

        // // 举报评论
        // const reportComment = async (commentId) => {
        //     // await reportComment(commentId);
        //     // router.push({ name: 'ReportPage', params: { commentId } });
        // };

        // // 回复评论
        // const replyToComment = (commentId) => {
        //     // post.value.comments.find(c => c.id === commentId).showReplyBox = true;
        // };

        // // 提交回复
        // const submitReply = async (commentId) => {
        //     // const reply = {
        //     //     authorId: post.value.authorId, // 回复人的 ID
        //     //     content: replyContent[commentId]
        //     // };
        //     // const submittedReply = await submitReply(commentId, reply);
        //     // post.value.comments.find(c => c.id === commentId).replies.push(submittedReply);
        //     // replyContent[commentId] = '';
        // };

        // // 点赞子评论
        // const likeReply = async (replyId) => {
        //     // const reply = post.value.comments.flatMap(c => c.replies).find(r => r.id === replyId);
        //     // reply.liked = !reply.liked;
        //     // await likeReply(replyId);
        //     // reply.likesCount += reply.liked ? 1 : -1;
        // };

        // // 举报子评论
        // const reportReply = async (replyId) => {
        //     // await reportReply(replyId);
        //     // router.push({ name: 'ReportPage', params: { replyId } });
        // };
        //     const reportPost = () => {
        //   alert("点击了举报按钮");
        //   // 调用后端 API 提交举报
        // };

        // // 编辑功能
        // const editPost = () => {
        //   alert("点击了编辑按钮");
        //   // 跳转到编辑页面或弹出编辑框
        // };

        // // 删除功能
        // const deletePost = () => {
        //   if (confirm("确定删除该文章吗？")) {
        //     alert("文章已删除");
        //     // 调用后端 API 删除文章
        //   }
        // };

        return {
            post_info,
            comment_info,
            newComment,
            likePost,
            // reportPost,
            postComment,
            likeComment,
            // reportComment,
            // replyToComment,
            // submitReply,
            // likeReply,
            // reportReply,
            Timetrans,
            goToUserDetail,
            BackToHome,
            formattedContent,
            isAuthor,
            editPost,
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
    font-style: italic;
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
    max-width: 800px;
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
</style>