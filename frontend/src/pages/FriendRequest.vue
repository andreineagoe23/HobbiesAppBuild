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
import { defineComponent, reactive, onMounted } from "vue";
import { FriendRequest } from "@/types/FriendRequest";
import { useUserStore } from "@/store/userStore";

export default defineComponent({
  name: "FriendRequest",
  setup() {
    const state = reactive({
      requests: [] as FriendRequest[],
      loading: false,
    });

    const userStore = useUserStore();
    const apiBaseUrl = "http://localhost:8000";

    const fetchRequests = async () => {
      state.loading = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/friend-requests/`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        if (!response.ok) throw new Error("Failed to fetch friend requests.");
        const data = await response.json();
        state.requests = data.requests;
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      } finally {
        state.loading = false;
      }
    };

    const acceptRequest = async (requestId: number) => {
      try {
        const response = await fetch(`${apiBaseUrl}/api/friend-requests/accept/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${userStore.token}`,
          },
          body: JSON.stringify({ request_id: requestId }),
        });
        if (!response.ok) throw new Error("Failed to accept friend request.");
        fetchRequests();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    onMounted(() => {
      fetchRequests();
    });

    return { ...state, fetchRequests, acceptRequest };
  },
});
</script>
