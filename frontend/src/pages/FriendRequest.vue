<template>
    <div>
      <h2>Friend Requests</h2>
      <div v-if="loading">Loading requests...</div>
      <div v-else>
        <div v-for="request in requests" :key="request.id">
          <p>{{ request.from_user.name }} wants to be your friend!</p>
          <button @click="acceptRequest(request.id)">Accept</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { FriendRequest } from '@/types/FriendRequest';
  import { useUserStore } from '@/store/userStore';
  
  export default defineComponent({
    setup() {
      const requests = ref<FriendRequest[]>([]);
      const loading = ref(false);
      const userStore = useUserStore();
      const apiBaseUrl = 'http://localhost:8000';
  
      const fetchRequests = async () => {
        loading.value = true;
        try {
          const response = await fetch(`${apiBaseUrl}/api/friend-requests/`, {
            headers: { Authorization: `Token ${userStore.token}` },
          });
          if (!response.ok) throw new Error('Failed to fetch requests');
          const data = await response.json();
          requests.value = data.requests;
        } catch (error) {
          console.error('Error fetching friend requests:', error);
        } finally {
          loading.value = false;
        }
      };
  
      const acceptRequest = async (requestId: number) => {
        try {
          const response = await fetch(`${apiBaseUrl}/api/friend-requests/accept/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Token ${userStore.token}`,
            },
            body: JSON.stringify({ request_id: requestId }),
          });
          if (!response.ok) throw new Error('Failed to accept request');
          fetchRequests();
        } catch (error) {
          console.error('Error accepting friend request:', error);
        }
      };
  
      onMounted(fetchRequests);
  
      return { requests, acceptRequest, loading };
    },
  });
  </script>
  