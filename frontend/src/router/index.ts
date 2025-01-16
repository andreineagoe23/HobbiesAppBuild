import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../store/userStore";

// Components
import MainPage from "../pages/MainPage.vue";
import Login from "../pages/Login.vue";
import Profile from "../pages/Profile.vue";
import UsersList from "../pages/UsersList.vue";
import Signup from "../pages/Signup.vue";

const base = import.meta.env.MODE === "development" ? import.meta.env.BASE_URL : "";

// Define routes
const routes = [
  { path: "/", name: "MainPage", component: MainPage },
  { path: "/signup", name: "Signup", component: Signup },
  { path: "/login", name: "Login", component: Login },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: "/users",
    name: "UsersList",
    component: UsersList,
    meta: { requiresAuth: true },
  },
];

// Create router instance
const router = createRouter({
  history: createWebHistory(base),
  routes,
});

// Navigation guard
router.beforeEach(async (to, _, next) => {
  const userStore = useUserStore();
  const token = localStorage.getItem("authToken");

  if (to.meta.requiresAuth && !token) {
    console.warn("Access denied. Redirecting to login.");
    return next({ name: "Login" });
  }

  if (token && !userStore.token) {
    try {
      console.log("Token exists but userStore is empty. Fetching user data...");
      userStore.setToken(token); // Set token in store
      await userStore.fetchUser(); // Fetch user data
      return next();
    } catch (error) {
      console.error("Error fetching user data during navigation:", error);
      userStore.clearUser(); // Clear invalid token
      return next({ name: "Login" });
    }
  }

  next(); // Allow navigation
});

export default router;
