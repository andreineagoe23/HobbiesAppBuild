<template>
  <div class="form-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="form">
      <label>
        Email:
        <input v-model="form.email" type="email" required />
      </label>
      <label>
        Password:
        <input v-model="form.password" type="password" required />
      </label>
      <button type="submit" class="button">Login</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { useUserStore } from "@/store/userStore";
import { useRouter } from "vue-router";
import "@/styles/login.css"; // Import the CSS file

export default defineComponent({
  name: "Login",
  setup() {
    const userStore = useUserStore();
    const router = useRouter(); // Use Vue Router for redirection
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
        console.log("Login successful:", data);

        // Redirect to home page
        router.push("/");
      } catch (error) {
        console.error("Error during login:", error);
      }
    };

    return { form, login };
  },
});
</script>
