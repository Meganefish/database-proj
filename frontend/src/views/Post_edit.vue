<template>
    <div class="post-edit">
        <h2 class="title">{{ isEditing ? "编辑帖子" : "新建帖子" }}</h2>
        <div v-if="!isEditing" class="forum-select">
            <el-select v-model="selectedForum" placeholder="请选择论坛" clearable class="select-forum">
                <el-option v-for="forum in forums" :key="forum.forum_id" :label="forum.forum_name"
                    :value="forum.forum_id"></el-option>
            </el-select>
        </div>
        <el-input v-model="postTitle" placeholder="请输入标题" clearable class="input-title"></el-input>
        <el-input v-model="postContent" type="textarea" rows="10" placeholder="请输入正文" clearable
            class="input-content"></el-input>
        <el-form-item label="上传图片">
            <el-upload :file-list="fileList" :auto-upload="false" :on-change="handleImageUpload" accept="image/*"
                list-type="picture">
                <el-button type="primary">选择图片</el-button>
            </el-upload>
            <div v-if="previewImages.length" class="image-preview">
                <div v-for="(image, index) in previewImages" :key="index" class="image-container">
                    <el-image :src="image" style="margin: 10px; width: 150px; height: auto;" />
                    <el-button size="mini" type="danger" icon="el-icon-close" class="delete-button"
                        @click="removeImage(index)">
                        删除
                    </el-button>
                </div>
            </div>
        </el-form-item>

        <div class="buttons">
            <el-button type="primary" @click="handleSubmit">发布</el-button>
            <el-button type="danger" @click="handleCancel">取消</el-button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, reactive } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import router from '@/router/Router.js';
import { ElMessage } from "element-plus";

export default {
    name: "PostEdit",
    setup() {
        const route = useRoute();
        const postId = route.query.id || null; // 从 query 参数获取 postId
        const isEditing = ref(!!postId); // 判断是新建还是编辑
        const postTitle = ref("");
        const postContent = ref("");
        const selectedForum = ref(null); // 新建时的论坛选择
        const forums = ref([]);
        const fileList = ref([]); // 用于展示已选图片的列表
        const previewImages = ref([]); // 预览图片的 Base64 数据
        const form = reactive({
            title: "",
            body: "",
            images: [],
        });

        const loadForums = async () => {
            try {
                const { data } = await axios.get("/get_forums");
                forums.value = data;
            } catch (error) {
                console.error("加载论坛数据失败", error);
            }
        };
        const loadPostData = async () => {
            if (isEditing.value) {
                try {
                    const { data } = await axios.get("/post" + postId);
                    postTitle.value = data.post.title;
                    postContent.value = data.post.body;
                    previewImages.value = data.image;
                } catch (error) {
                    console.error("加载帖子失败", error);
                }
            }
        };
        const handleImageUpload = async (file) => {
            // 将文件读取为 Base64 编码
            const reader = new FileReader();
            reader.onload = (e) => {
                const base64 = e.target.result;
                previewImages.value.push(base64);
                // form.images.push(base64); // 保存到表单数据中
            };
            reader.readAsDataURL(file.raw);
        };
        const removeImage = (index) => {
            // 删除预览和 Base64 数据
            previewImages.value.splice(index, 1);
            // form.images.splice(index, 1);
        };
        // 提交表单
        const handleSubmit = async () => {
            if (!postTitle.value.trim() || !postContent.value.trim()) {
                return alert("标题和正文均不能为空！");
            }
            if (!isEditing.value && !selectedForum.value) {
                return alert("请选择一个论坛！");
            }
            try {
                form.title = postTitle.value;
                form.body = postContent.value;
                form.images = previewImages.value;
                if (isEditing.value) {
                    axios.post(`/post${postId}/edit_post`, form).then((res) => {
                        console.log(res.data.message);
                        if (res.data.success == true) {
                            ElMessage.success({
                                message: "修改成功", duration: 1200,
                                onClose: () => {
                                    router.push({ path: '/post', query: { id: postId } });
                                }
                            });
                        } else { ElMessage.error(res.data.message || "修改失败"); }
                    })
                } else {
                    axios.post("/forum" + selectedForum.value + "/release_post", form).then((res) => {
                        console.log(res.data.message);
                        if (res.data.success == true) {
                            ElMessage.success({
                                message: "发布成功", duration: 1200,
                                onClose: () => {
                                    router.push("/home");
                                }
                            });
                        } else { ElMessage.error(res.data.message || "发布失败"); }
                    })
                }
            } catch (error) {
                console.error("提交失败", error);
                alert("提交失败，请稍后再试！");
            }
        };
        // 取消操作
        const handleCancel = () => {
            if (confirm("您确定要取消吗？内容将不会被保存。")) {
                if (!isEditing.value) { router.push("/home"); } // 返回主页
                else { router.push({ path: '/post', query: { id: postId } }); }
            }
        };
        onMounted(() => {
            if (isEditing.value) {
                loadPostData(); // 编辑模式加载数据
            } else {
                loadForums(); // 新建模式加载论坛数据
            }
        });
        return {
            postTitle,
            postContent,
            selectedForum,
            forums,
            handleSubmit,
            handleCancel,
            isEditing,
            fileList,
            previewImages,
            handleImageUpload,
            removeImage
        };
    },
};
</script>

<style scoped>
.post-edit {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.forum-select {
    margin-bottom: 20px;
}

.select-forum {
    width: 100%;
}

.input-title,
.input-content {
    width: 100%;
    margin-bottom: 20px;
}

.input-content {
    resize: none;
}

.buttons {
    display: flex;
    justify-content: space-between;
}

.buttons .el-button {
    width: 48%;
}

.image-preview {
    display: flex;
    flex-wrap: wrap;
    margin-top: 10px;
}

.image-container {
    position: relative;
    display: inline-block;
    margin: 10px;
}

.delete-button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: rgba(255, 0, 0, 0.7);
    color: white;
}
</style>