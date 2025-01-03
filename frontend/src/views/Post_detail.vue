<template>
    <div>
        <h1>{{ post_info.title }}</h1>
        <p>作者: 
            <!--router-link :to="{ name: 'UserProfile', params: { id: post_info.user_id } }"-->
            {{ post_info.nickname}}
            <!--/router-link-->
        </p>
        <p>{{ post_info.body }}</p>

        <div class="actions">
            <el-button @click="likePost" :icon="liked ? 'el-icon-star-off' : 'el-icon-star-on'">
                {{ liked ? '取消点赞' : '点赞' }} ({{ post_info.liked }})
            </el-button>
            <el-button @click="reportPost">举报</el-button>
        </div>

        <hr>

        <!-- 评论区 -->
        <div class="comments">
            <h2>评论区 ({{ comment_info.length }} 条评论)</h2>

            <el-input v-model="newComment" placeholder="良言一句三冬暖，恶语伤人六月寒" @keyup.enter="postComment"></el-input>

            <div v-for="comment in comment_info" :key="comment.comment_id" class="comment">
                <p>
                    <!--router-link :to="{ name: 'UserProfile', params: { id: comment.user_id } }">{{ comment.nickname
                        }}</router-link-->
                        : {{ comment.content }}
                    <el-button @click="likeComment(comment.comment_id)"
                        :icon="comment.like_it_or_not ? 'el-icon-star-off' : 'el-icon-star-on'">
                        {{ comment.like_it_or_not ? '取消点赞' : '点赞' }} ({{ comment.like_num }})
                    </el-button>
                    <el-button @click="reportComment(comment.comment_id)">举报</el-button>
                    <el-button @click="replyToComment(comment.comment_id)">回复</el-button>
                </p>

                <!-- 回复框 -->
                <div v-if="comment.showReplyBox">
                    <el-input v-model="replyContent[comment.comment_id]" placeholder="回复 @{{ comment.nickname }}"
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
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from "axios";

export default {
    name: 'DetailPage',
    setup() {
        const route = useRoute();
        const postId = ref(null);
        const post_info = ref({});
        const comment_info = ref([]);
        const newComment = ref('');
        // const replyContent = ref({});
        const liked = ref(false);
        // const reportReason = ref('');
        // const showReportInput = ref(false);

        // 获取帖子详情
        onMounted(async () => {
            postId.value = route.query.id;
            getPostDetails();
            liked.value = post_info.value.like_it_or_not;
        });
        const getPostDetails = async () => {
            try {
                const response = await axios.get("/post"+postId.value);
                post_info.value = response.data.post;
                comment_info.value = response.data.comment;
            } catch (error) {
                console.error("获取数据失败：", error);
            }
        };

        // 点赞帖子
        const likePost = async () => {
            try {
                await axios.get("/post"+postId.value+"/click_like");
            } catch (error) {
                console.error("获取数据失败：", error);
            }
            liked.value = !liked.value;
            post_info.value.liked += liked.value ? 1 : -1;
        };

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
                await axios.get("/comment"+commentId+"/click_like");
            } catch (error) {
                console.error("获取数据失败：", error);
            }
            liked.value = !liked.value;
            post_info.value.liked += liked.value ? 1 : -1;

            // const comment = post.value.comments.find(c => c.id === commentId);
            // comment.liked = !comment.liked;
            // await likeComment(commentId);
            // comment.likesCount += comment.liked ? 1 : -1;
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

        return {
            post_info,
            comment_info,
            newComment,
            // navigateToDetails,
            likePost,
            // reportPost,
            postComment,
            likeComment,
            // reportComment,
            // replyToComment,
            // submitReply,
            // likeReply,
            // reportReply
        };
    }
};
</script>

<style scoped>
.actions {
    margin-bottom: 20px;
}

.comments {
    margin-top: 20px;
}

.comment,
.reply {
    margin-bottom: 10px;
}
</style>