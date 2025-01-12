import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../store/userStore';

// Components
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import Login from '../pages/Login.vue';
import Profile from '../pages/Profile.vue';
import UsersList from '../pages/UsersList.vue';
import Signup from '../pages/Signup.vue';

const base = import.meta.env.MODE === 'development' ? import.meta.env.BASE_URL : '';

const routes = [
  { path: '/', name: 'Main Page', component: MainPage },
  { path: '/other/', name: 'Other Page', component: OtherPage },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: '/users',
    name: 'UsersList',
    component: UsersList,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(base),
  routes,
});

router.beforeEach((to, _, next) => {
  const userStore = useUserStore();
  const isAuthenticated = localStorage.getItem('authToken');

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    if (isAuthenticated && !userStore.user) {
      // Fetch user details if authenticated but user is not set
      userStore.fetchUser().then(() => next()).catch(() => next({ name: 'Login' }));
    } else {
      next();
    }
  }
});

export default router;
