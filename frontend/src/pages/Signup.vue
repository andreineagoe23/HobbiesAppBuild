<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="submitSignup" class="signup-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input id="username" v-model="form.username" type="text" placeholder="Enter your username" required />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" v-model="form.email" type="email" placeholder="Enter your email" required />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="form.password" type="password" placeholder="Enter your password" required />
      </div>

      <div class="form-group">
        <label for="name">Full Name</label>
        <input id="name" v-model="form.name" type="text" placeholder="Enter your full name" required />
      </div>

      <div class="form-group">
        <label for="date_of_birth">Date of Birth</label>
        <input id="date_of_birth" v-model="form.date_of_birth" type="date" required />
      </div>

      <div class="form-group">
        <label for="hobbies">Hobbies</label>
        <div class="hobbies-list">
          <label v-for="hobby in hobbies" :key="hobby.id" class="hobby-checkbox">
            <input
              type="checkbox"
              :value="hobby.id"
              v-model="selectedHobbies"
            />
            {{ hobby.name }}
          </label>
        </div>
      </div>

      <button type="submit" class="signup-button">Sign Up</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/userStore';
import { Hobby } from '../types/Hobby';

export default defineComponent({
  setup() {
    const router = useRouter();
    const userStore = useUserStore();

    const form = ref({
      username: '',
      email: '',
      password: '',
      name: '',
      date_of_birth: '',
    });

    const hobbies = ref<Hobby[]>([]);
    const selectedHobbies = ref<number[]>([]);

    const fetchHobbies = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/hobbies/');
        if (!response.ok) {
          throw new Error(`Failed to fetch hobbies: ${response.status} ${response.statusText}`);
        }
        hobbies.value = await response.json();
      } catch (error: unknown) {
        console.error('Error fetching hobbies:', (error as Error).message);
      }
    };

    const submitSignup = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ...form.value,
            hobbies: selectedHobbies.value,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`Signup failed: ${errorData.error || response.statusText}`);
        }

        const data = await response.json();
        userStore.setToken(data.token);
        userStore.setUser(data.user);

        alert('Signup successful! Redirecting...');
        router.push('/protected-route'); // Replace with your actual route
      } catch (error: unknown) {
        console.error('Error signing up:', (error as Error).message);
        alert((error as Error).message);
      }
    };

    onMounted(fetchHobbies);

    return {
      form,
      hobbies,
      selectedHobbies,
      submitSignup,
    };
  },
});
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="date"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.hobbies-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hobby-checkbox {
  display: flex;
  align-items: center;
  gap: 5px;
}

.signup-button {
  background-color: #0066cc;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.signup-button:hover {
  background-color: #005bb5;
}
</style>
