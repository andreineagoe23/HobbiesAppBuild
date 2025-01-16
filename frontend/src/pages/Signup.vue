<template>
  <div class="signup-container">
    <h1 class="signup-title">Signup</h1>
    <form @submit.prevent="signup" class="signup-form">
      <div class="form-group">
        <label for="name" class="form-label">Name:</label>
        <input
          id="name"
          v-model="form.name"
          class="form-input"
          type="text"
          placeholder="Enter your name"
          required
        />
      </div>
      <div class="form-group">
        <label for="email" class="form-label">Email:</label>
        <input
          id="email"
          v-model="form.email"
          class="form-input"
          type="email"
          placeholder="Enter your email"
          required
        />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Password:</label>
        <input
          id="password"
          v-model="form.password"
          class="form-input"
          type="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <div class="form-group">
        <label for="dob" class="form-label">Date of Birth:</label>
        <input
          id="dob"
          v-model="form.date_of_birth"
          class="form-input"
          type="date"
          required
        />
      </div>
      <fieldset class="form-group">
        <legend class="form-legend">Select Hobbies:</legend>
        <div v-for="hobby in hobbies" :key="hobby.id" class="checkbox-item">
          <input
            type="checkbox"
            :id="'hobby-' + hobby.id"
            class="form-check-input"
            :value="hobby.id"
            v-model="form.hobbies"
          />
          <label :for="'hobby-' + hobby.id" class="form-check-label">
            {{ hobby.name }}
          </label>
        </div>
      </fieldset>
      <button type="submit" class="action-button">Signup</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted } from "vue";
import { useUserStore } from "@/store/userStore";
import { useRouter } from "vue-router";
import { Hobby } from "@/types/Hobby";

export default defineComponent({
  name: "Signup",
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const form = reactive({
      name: "",
      email: "",
      password: "",
      date_of_birth: "",
      hobbies: [] as number[],
    });

    const hobbies = reactive<Hobby[]>([]);

    const fetchHobbies = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/hobbies/");
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        const data = await response.json();
        hobbies.push(...data);
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    };

    const signup = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/signup/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        });
        if (!response.ok) throw new Error("Signup failed");
        const data = await response.json();
        userStore.setToken(data.token);
        userStore.setUser(data.user);
        router.push("/");
      } catch (error) {
        console.error("Error during signup:", error);
      }
    };

    onMounted(() => {
      fetchHobbies();
    });

    return { form, signup, hobbies };
  },
});
</script>

<style scoped>
.signup-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.signup-title {
  color: #42b983;
  text-align: center;
  margin-bottom: 20px;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
}

.form-input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5);
}

.checkbox-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-check-input {
  margin-right: 10px;
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
