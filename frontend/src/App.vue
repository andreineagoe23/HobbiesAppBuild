<template>
    <div id="app">
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/signup">Sign Up</router-link>
        <router-link to="/profile">Profile</router-link>
        <router-link to="/users">Users</router-link>
        <button v-if="isAuthenticated" @click="logout">Logout</button>
      </nav>
      <main>
        <router-view></router-view>
      </main>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useUserStore } from '@/store/userStore';
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
  
      // Check if the user is authenticated
      const isAuthenticated = !!userStore.token;
  
      // Logout function
      const logout = () => {
        userStore.$reset(); // Clear the store
        localStorage.removeItem('authToken'); // Clear token from storage
        window.location.href = '/'; // Redirect to login
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
  