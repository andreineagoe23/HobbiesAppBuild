<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email:</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          required
        />
      </div>
      <div>
        <label for="password">Password:</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <button type="submit">Login</button>
    </form>
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useUserStore } from '../store/userStore';

export default defineComponent({
  name: 'Login',
  setup() {
    const email = ref('');
    const password = ref('');
    const errorMessage = ref<string | null>(null);
    const userStore = useUserStore();

    const login = async () => {
      errorMessage.value = null; // Clear previous error messages
      try {
        const response = await fetch('http://localhost:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email.value,
            password: password.value,
          }),
        });

        if (!response.ok) {
          // Handle non-200 responses
          const errorText = await response.text();
          console.error('Server error:', errorText);
          throw new Error(`Login failed: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Login successful:', data);

        // Map the backend response to the User interface
        userStore.setUser({
          id: data.user.id,
          email: data.user.email,
          name: data.user.name,
          dob: data.user.dob,
          hobbies: data.user.hobbies,
        });

        // Redirect to the main page or wherever appropriate
        window.location.href = '/';
      } catch (error: any) {
        console.error('Login error:', error.message);
        errorMessage.value = error.message || 'An error occurred during login.';
      }
    };

    return {
      email,
      password,
      errorMessage,
      login,
    };
  },
});
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.error {
  color: red;
  margin-top: 10px;
}
button {
  margin-top: 10px;
}
</style>
