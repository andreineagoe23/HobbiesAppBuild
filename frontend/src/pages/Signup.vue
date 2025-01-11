<template>
    <div class="signup">
      <h1>Signup</h1>
      <form @submit.prevent="signup">
        <div>
          <label for="name">Name:</label>
          <input v-model="name" id="name" type="text" placeholder="Your name" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="email" id="email" type="email" placeholder="Your email" required />
        </div>
        <div>
          <label for="dob">Date of Birth:</label>
          <input v-model="dob" id="dob" type="date" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="password" id="password" type="password" placeholder="Your password" required />
        </div>
        <div>
          <label for="hobbies">Hobbies:</label>
          <div>
            <ul>
              <li v-for="(hobby, index) in hobbies" :key="index">
                {{ hobby }}
                <button type="button" @click="removeHobby(index)">Remove</button>
              </li>
            </ul>
            <input v-model="newHobby" type="text" placeholder="Add a new hobby" />
            <button type="button" @click="addHobby">Add Hobby</button>
          </div>
        </div>
        <button type="submit">Signup</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    setup() {
      const name = ref('');
      const email = ref('');
      const dob = ref('');
      const password = ref('');
      const hobbies = ref<string[]>([]);
      const newHobby = ref('');
  
      // Add a hobby to the list
      const addHobby = () => {
        if (newHobby.value && !hobbies.value.includes(newHobby.value)) {
          hobbies.value.push(newHobby.value);
          newHobby.value = '';
        }
      };
  
      // Remove a hobby from the list
      const removeHobby = (index: number) => {
        hobbies.value.splice(index, 1);
      };
  
      // Signup function
      const signup = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/signup/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        date_of_birth: dob.value,
        password: password.value,
        hobbies: hobbies.value,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert(`Signup failed: ${errorData.message || 'Unknown error'}`);
      return;
    }

    const data = await response.json();
    alert('Signup successful! You can now login.');
    window.location.href = '/';
  } catch (error) {
    console.error('Error during signup:', error);
    alert('An error occurred during signup. Please try again.');
  }
};
  
      return {
        name,
        email,
        dob,
        password,
        hobbies,
        newHobby,
        addHobby,
        removeHobby,
        signup,
      };
    },
  });
  </script>
  
  <style scoped>
  .signup {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  form div {
    margin-bottom: 15px;
  }
  
  form label {
    font-weight: bold;
  }
  
  form input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
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
  