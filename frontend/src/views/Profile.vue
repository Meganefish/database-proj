<template>
    <div class="profile-container">
        <profile-head></profile-head>
        <div class="profile-content">
            <profile-side @update-content="updateContent" :current-component="currentComponent"></profile-side>
            <div class="profile-body">
                <component :is="currentComponent"></component>
            </div>
        </div>
    </div>
</template>

<script>
import profileHead from './profile_box/profile_head.vue'
import profileSide from './profile_box/profile_side.vue'
import profileUser from './profile_box/profile_user.vue'
import profilePost from './profile_box/profile_post.vue'
import profileComment from './profile_box/profile_comment.vue'
import profileCourse from './profile_box/profile_course.vue'

export default {
    name: 'UserProfile',
    components: {
        profileHead,
        profileSide,
        profileUser,
        profilePost,
        profileComment,
        profileCourse,
    },
    data() {
        return {
            currentComponent: 'profileUser'  // 默认加载管理用户组件
        }
    },
    created() {
        const savedComponent = localStorage.getItem('currentComponent');
        if (savedComponent) {
            this.currentComponent = savedComponent;
        }
    },
    methods: {
        updateContent(key) {
            switch (key) {
                case '1':
                    this.currentComponent = 'profileUser';
                    break;
                case '2':
                    this.currentComponent = 'profileCourse';
                    break;
                case '3':
                    this.currentComponent = 'profilePost';
                    break;
                case '4':
                    this.currentComponent = 'profileComment';
                    break;
                default:
                    this.currentComponent = 'profileUser';
            }
            localStorage.setItem('currentComponent', this.currentComponent);
        }
    }
}
</script>


<style scoped>
.profile-container {
    display: flex;
    width: 100%;
    margin: 0 auto; /* 居中对齐 */
    flex-direction: column;
    height: 100vh;
}

.profile-content {
    width: 60%;
    display: flex;
    flex: 1;
    margin: 0 auto; /* 居中对齐 */
}

.profile-body {
    flex: 1;
    padding: 20px;
}
</style>