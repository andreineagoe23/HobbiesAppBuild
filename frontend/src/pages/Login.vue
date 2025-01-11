<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'; // Import ref from 'vue'
import { useUserStore } from '@/store/userStore';

export default defineComponent({
  setup() {
    const userStore = useUserStore(); // Access the Pinia store
    const email = ref(''); // Define a reactive email variable
    const password = ref(''); // Define a reactive password variable

    const login = async () => {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email.value, password: password.value }),
        });
        const data = await response.json();
        if (response.ok) {
          userStore.setToken(data.token);
          userStore.setUser(data.user);
          alert('Login successful!');
          window.location.href = '/profile'; // Redirect to profile page
        } else {
          alert('Login failed: ' + data.message);
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    };

    return {
      email,
      password,
      login,
    };
  },
});
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
}

input {
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369f6e;
}
</style>
