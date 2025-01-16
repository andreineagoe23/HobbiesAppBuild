<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/signup" v-if="!isAuthenticated">Sign Up</router-link>
      <router-link to="/login" v-if="!isAuthenticated">Login</router-link>
      <router-link to="/profile" v-if="isAuthenticated">Profile</router-link>
      <router-link to="/users" v-if="isAuthenticated">Users</router-link>
      <button v-if="isAuthenticated" class="logout-button" @click="logout">Logout</button>
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

    const isAuthenticated = computed(() => !!userStore.token);

    // logout.
    const logout = () => {
      userStore.clearUser(); 
      localStorage.removeItem("authToken"); 
      window.location.href = "/"; 
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

nav .logout-button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

nav .logout-button:hover {
  background-color: #d9363e; 
}

nav .logout-button:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(255, 77, 79, 0.5); 
}

main {
  padding: 20px;
}
</style>
