<template>
  <div class="form-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="form">
      <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" v-model="form.email" type="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" v-model="form.password" type="password" required />
      </div>
      <button type="submit" class="action-button">Login</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { useUserStore } from "@/store/userStore";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "Login",
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const form = reactive({
      email: "",
      password: "",
    });

    const login = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        });
        if (!response.ok) throw new Error("Login failed");
        const data = await response.json();
        userStore.setToken(data.token);
        userStore.setUser(data.user);
        router.push("/");
      } catch (error) {
        console.error("error logging in:", error);
      }
    };

    return { form, login };
  },
});
</script>

<style scoped>
.form-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #42b983;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5);
}

.action-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.action-button:hover {
  background-color: #36a572;
}

.action-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
