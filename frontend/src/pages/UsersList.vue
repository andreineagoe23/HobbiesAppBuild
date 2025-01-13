<template>
    <div>
      <h2>Users List</h2>
      <div v-for="user in users" :key="user.id">
        <p>{{ user.name }}</p>
        <button @click="sendFriendRequest(user.id)">Send Friend Request</button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { User } from '../types/User';
  import { useUserStore } from '@/store/userStore';
  
  export default defineComponent({
    setup() {
      const users = ref<User[]>([]);
      const userStore = useUserStore();
      const apiBaseUrl = 'http://localhost:8000';
  
      const fetchUsers = async () => {
        try {
          const response = await fetch(`${apiBaseUrl}/api/users/`, {
            headers: { Authorization: `Token ${userStore.token}` },
          });
          if (!response.ok) throw new Error('Failed to fetch users');
          const data = await response.json();
          users.value = data;
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      };
  
      const sendFriendRequest = async (toUserId: number) => {
        try {
          const response = await fetch(`${apiBaseUrl}/api/friend-requests/send/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Token ${userStore.token}`,
            },
            body: JSON.stringify({ to_user_id: toUserId }),
          });
          if (!response.ok) throw new Error('Failed to send friend request');
          alert('Friend request sent!');
        } catch (error) {
          console.error('Error sending friend request:', error);
        }
      };
  
      onMounted(fetchUsers);
  
      return { users, sendFriendRequest };
    },
  });
  </script>
  