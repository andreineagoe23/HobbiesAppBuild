<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/signup" v-if="!isAuthenticated">Sign Up</router-link>
      <router-link to="/login" v-if="!isAuthenticated">Login</router-link>
      <router-link to="/profile" v-if="isAuthenticated">Profile</router-link>
      <router-link to="/users" v-if="isAuthenticated">Users</router-link>
      <button v-if="isAuthenticated" @click="logout">Logout</button>
    </nav>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useUserStore } from "@/store/userStore";

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    // Reactive property for authentication status
    const isAuthenticated = computed(() => !!userStore.token);

    // Logout function
    const logout = () => {
      userStore.clearUser(); // Clear the user store
      localStorage.removeItem("authToken"); // Remove token from local storage
      window.location.href = "/"; // Redirect to home
    };

    return {
      isAuthenticated,
      logout,
    };
  },
});
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

nav a {
  text-decoration: none;
  color: #42b983;
}

nav a:hover {
  text-decoration: underline;
}

main {
  padding: 20px;
}
</style>
