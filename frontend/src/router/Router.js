import { createRouter, createWebHistory } from 'vue-router'

// 关键字: let 和 const。
// let 声明的变量只在 let 命令所在的代码块内有效。
// const 声明一个只读的常量，一旦声明，常量的值就不能改变。
// new的作用是通过构造函数来创建一个实例对象。

// 创建router 对路由进行管理，它是由构造函数 new vueRouter() 创建，接受routes 参数
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
      // component是指组件  import引用login.vue地址
      component: ()=>import('../views/Login.vue')
    },
    // {
    //   path: '/admin_home',  // 路径
    //   name: 'admin_home',  //名字
    //   meta: {         
    //     title: '管理主页' 
    //   },
    //   component: ()=>import('../views/Admin.vue')
    // },
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
  ]
})

// 导出router这个方法函数，便于其他模块引用
export default router
