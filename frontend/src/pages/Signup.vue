<template>
  <div class="form-container">
    <h1>Signup</h1>
    <form @submit.prevent="signup" class="form">
      <label>
        Name:
        <input v-model="form.name" required />
      </label>
      <label>
        Email:
        <input v-model="form.email" type="email" required />
      </label>
      <label>
        Password:
        <input v-model="form.password" type="password" required />
      </label>
      <label>
        Date of Birth:
        <input v-model="form.date_of_birth" type="date" required />
      </label>
      <fieldset>
        <legend>Select Hobbies:</legend>
        <div v-for="hobby in hobbies" :key="hobby.id" class="checkbox-item">
          <input
            type="checkbox"
            :value="hobby.id"
            v-model="form.hobbies"
            :id="'hobby-' + hobby.id"
          />
          <label :for="'hobby-' + hobby.id">{{ hobby.name }}</label>
        </div>
      </fieldset>
      <button type="submit" class="button">Signup</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted } from "vue";
import { useUserStore } from "@/store/userStore";
import { useRouter } from "vue-router";
import { Hobby } from "@/types/Hobby";
import "@/styles/signup.css"; // Import the CSS file

export default defineComponent({
  name: "Signup",
  setup() {
    const userStore = useUserStore();
    const router = useRouter(); // Use Vue Router for redirection
    const form = reactive({
      name: "",
      email: "",
      password: "",
      date_of_birth: "",
      hobbies: [] as number[],
    });

    const hobbies = reactive<Hobby[]>([]);

    // Fetch available hobbies
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
        console.log("Signup successful:", data);

        // Redirect to home page
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
