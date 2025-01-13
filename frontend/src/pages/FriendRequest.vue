<template>
  <div>
    <h2>Friend Requests</h2>

    <!-- Pending Requests Section -->
    <div>
      <h3>Pending Friend Requests</h3>
      <div v-if="loadingRequests">Loading pending requests...</div>
      <ul v-else-if="pendingRequests.length > 0">
        <li v-for="request in pendingRequests" :key="request.id">
          <p><strong>{{ request.from_user.name }}</strong> wants to be your friend!</p>
          <button @click="acceptFriendRequest(request.id)">Accept</button>
        </li>
      </ul>
      <p v-else>No pending friend requests.</p>
    </div>

    <!-- Send Requests Section -->
    <div>
      <h3>Send Friend Requests</h3>
      <div v-if="loadingUsers">Loading users...</div>
      <ul v-else-if="users.length > 0">
        <li v-for="user in users" :key="user.id">
          <p><strong>{{ user.name }}</strong> ({{ user.email }})</p>
          <button
            @click="sendFriendRequest(user.id)"
            :disabled="sentRequests.includes(user.id)"
          >
            {{ sentRequests.includes(user.id) ? "Request Sent" : "Send Friend Request" }}
          </button>
        </li>
      </ul>
      <p v-else>No users available to send friend requests.</p>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { User } from "@/types/User";
import { FriendRequest } from "@/types/FriendRequest";
import { useUserStore } from "@/store/userStore";

export default defineComponent({
  name: "FriendRequest",
  setup() {
    const users = ref<User[]>([]); // Users available for friend requests
    const sentRequests = ref<number[]>([]); // Track sent requests
    const pendingRequests = ref<FriendRequest[]>([]); // Pending friend requests
    const loadingUsers = ref(false); // Loading state for users
    const loadingRequests = ref(false); // Loading state for pending requests

    const userStore = useUserStore();
    const apiBaseUrl = "http://localhost:8000";

    const fetchUsers = async () => {
      loadingUsers.value = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/eligible-for-friend-requests/`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        const data = await response.json();
        users.value = data.results;
      } catch {
        console.error("Error fetching eligible users.");
      } finally {
        loadingUsers.value = false;
      }
    };

    const fetchPendingRequests = async () => {
      loadingRequests.value = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/friend-requests/`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        const data = await response.json();
        pendingRequests.value = data.requests;
      } catch {
        console.error("Error fetching pending requests.");
      } finally {
        loadingRequests.value = false;
      }
    };

    const sendFriendRequest = async (userId: number) => {
      try {
        const response = await fetch(`${apiBaseUrl}/api/friend-requests/send/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${userStore.token}`,
          },
          body: JSON.stringify({ to_user_id: userId }),
        });
        if (!response.ok) throw new Error("Failed to send friend request.");
        sentRequests.value.push(userId);
      } catch {
        console.error("Error sending friend request.");
      }
    };

    const acceptFriendRequest = async (requestId: number) => {
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
        fetchPendingRequests(); // Refresh pending requests after accepting
      } catch {
        console.error("Error accepting friend request.");
      }
    };

    onMounted(() => {
      fetchUsers();
      fetchPendingRequests();
    });

    return {
      users,
      sentRequests,
      pendingRequests,
      loadingUsers,
      loadingRequests,
      sendFriendRequest,
      acceptFriendRequest,
    };
  },
});
</script>
