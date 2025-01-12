<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="signup">
      <input type="text" v-model="username" placeholder="Username" required />
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async signup() {
      try {
        const response = await fetch("http://localhost:8000/api/signup/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.errorMessage = errorData.error || "Signup failed.";
          return;
        }

        const data = await response.json();
        this.successMessage = data.message;
        this.errorMessage = "";
      } catch (error) {
        console.error("Error during signup:", error);
        this.errorMessage = "An unexpected error occurred. Please try again.";
      }
    },
  },
});
</script>
