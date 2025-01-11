<template>
    <div class="profile">
      <h1>User Profile</h1>
      <form @submit.prevent="saveProfile">
        <div>
          <label for="name">Name:</label>
          <input v-model="editableUser.name" id="name" type="text" placeholder="Your name" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="editableUser.email" id="email" type="email" placeholder="Your email" required />
        </div>
        <div>
          <label for="dob">Date of Birth:</label>
          <input v-model="editableUser.dob" id="dob" type="date" required />
        </div>
        <div>
          <label for="hobbies">Hobbies:</label>
          <div>
            <ul>
              <li v-for="(hobby, index) in editableUser.hobbies" :key="index">
                {{ hobby }}
                <button type="button" @click="removeHobby(index)">Remove</button>
              </li>
            </ul>
            <input v-model="newHobby" type="text" placeholder="Add a new hobby" />
            <button type="button" @click="addHobby">Add Hobby</button>
          </div>
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="editableUser.password" id="password" type="password" placeholder="New password" />
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { useUserStore } from '@/store/userStore';
  import { User } from '@/types/User';
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const editableUser = ref<User | null>(null);
      const newHobby = ref('');
  
      // Fetch user details on mount
      onMounted(async () => {
        if (userStore.user) {
          editableUser.value = { ...userStore.user }; // Make a copy for editing
        } else {
          const response = await fetch('/api/profile', {
            headers: { Authorization: `Bearer ${userStore.token}` },
          });
          const data = await response.json();
          userStore.setUser(data);
          editableUser.value = { ...data };
        }
      });
  
      // Add a new hobby to the list
      const addHobby = () => {
        if (newHobby.value && editableUser.value) {
          editableUser.value.hobbies.push(newHobby.value);
          newHobby.value = '';
        }
      };
  
      // Remove a hobby from the list
      const removeHobby = (index: number) => {
        if (editableUser.value) {
          editableUser.value.hobbies.splice(index, 1);
        }
      };
  
      // Save the profile changes
      const saveProfile = async () => {
        if (!editableUser.value) return;
  
        const response = await fetch('/api/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${userStore.token}`,
          },
          body: JSON.stringify(editableUser.value),
        });
  
        if (response.ok) {
          const updatedUser = await response.json();
          userStore.setUser(updatedUser); // Update the global store
          alert('Profile updated successfully!');
        } else {
          alert('Failed to update profile.');
        }
      };
  
      return {
        editableUser,
        newHobby,
        addHobby,
        removeHobby,
        saveProfile,
      };
    },
  });
  </script>
  
  <style scoped>
  .profile {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  .profile form div {
    margin-bottom: 15px;
  }
  .profile form label {
    display: block;
    font-weight: bold;
  }
  .profile form input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    box-sizing: border-box;
  }
  </style>
  