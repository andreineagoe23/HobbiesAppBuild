// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import Login from '../pages/Login.vue';
import Profile from '../pages/Profile.vue';
import UsersList from '../pages/UsersList.vue';
import Signup from '../pages/Signup.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
    { path: '/', name: 'Main Page', component: MainPage },
    { path: '/other/', name: 'Other Page', component: OtherPage },
    { path: '/signup', name: 'Signup', component: Signup }, 
    { path: '/login', name: 'Login', component: Login },
    { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
    { path: '/users', name: 'UsersList', component: UsersList, meta: { requiresAuth: true } },
 ];

  const router = createRouter({
    history: createWebHistory(),
    routes,
  });

  router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('authToken');
    if (to.meta.requiresAuth && !isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  });
  
  export default router;
