import { createRouter, createWebHistory } from 'vue-router'
const router = createRouter({
    history: createWebHistory(''),
    routes: [
    //默认转到登录页
    {
        path:'/',
        redirect:'/login'
    },
    {
      path: '/login',  // 路径
      name: 'login',  //名字
      meta: {         
        title: '登录页' 
      },
      component: ()=>import('../views/Login.vue')
    },
    {
      path: '/admin_home',  // 路径
      name: 'admin_home',  //名字
      meta: {         
        title: '管理主页' 
      },
      component: ()=>import('../views/Admin.vue')
    },
    {
      path: '/home',  // 路径
      name: 'home',  //名字
      meta: {         
        title: '主页' 
      },
      component: ()=>import('../views/Home.vue')
    },
    {
      path: '/register',  // 路径
      name: 'register',  //名字
      meta: {         
        title: '注册页' 
      },
      component: ()=>import('../views/Register.vue')
    },
    {
      path: '/post_edit',  // 路径
      name: 'post_edit',  //名字
      meta: {         
        title: '帖子编辑页' 
      },
      component: ()=>import('../views/Post_edit.vue')
    },
    {
      path: '/post',   
      name: 'DetailPage',
      meta: {         
            title: '帖子编辑页' 
          },
      component: ()=>import('../views/Post_detail.vue')
    },
  ]
})

// 导出router这个方法函数，便于其他模块引用
export default router
