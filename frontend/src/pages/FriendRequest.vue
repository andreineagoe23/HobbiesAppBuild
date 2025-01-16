<template>
  <div class="friend-request-container">
    <!-- Friends Section -->
    <section class="friends-section">
      <h2>Your Friends</h2>
      <div v-if="loadingFriends" class="loading-message">Loading your friends...</div>
      <ul v-else-if="friends.length > 0">
        <li v-for="friend in friends" :key="friend.id" class="friend-item">
          <strong>{{ friend.name }}</strong> ({{ friend.email }})
        </li>
      </ul>
      <p v-else class="no-content-message">No friends found.</p>
    </section>

    <!-- Pending Friend Requests Section -->
    <section class="pending-requests-section">
      <h2>Friend Requests</h2>
      <h3>Pending Friend Requests</h3>
      <div v-if="loadingRequests" class="loading-message">Loading pending requests...</div>
      <ul v-else-if="pendingRequests.length > 0">
        <li v-for="request in pendingRequests" :key="request.id" class="pending-request-item">
          <p>
            <strong>{{ request.from_user.name }}</strong> wants to be your friend!
          </p>
          <button @click="acceptFriendRequest(request.id)" class="action-button">
            Accept
          </button>
        </li>
      </ul>
      <p v-else class="no-content-message">No pending friend requests.</p>
    </section>

    <!-- Send Friend Requests Section -->
    <section class="send-requests-section">
      <h3>Send Friend Requests</h3>
      <div v-if="loadingUsers || loadingFriends" class="loading-message">Loading users...</div>
      <ul v-else-if="users.length > 0">
        <li v-for="user in users" :key="user.id" class="user-item">
          <p>
            <strong>{{ user.name }}</strong> ({{ user.email }})
          </p>
          <div>
            <em v-if="friendIds.includes(user.id)">Already friends</em>
            <em v-else-if="pendingRequestsFromUserIds.includes(user.id)">They have sent you a friend request</em>
            <em v-else-if="sentRequests.includes(user.id)">Request Sent</em>
            <button v-else @click="sendFriendRequest(user.id)" class="action-button">
              Send Friend Request
            </button>
          </div>
        </li>
      </ul>
      <p v-else class="no-content-message">No users available to send friend requests.</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import type { User } from "@/types/User";
import type { FriendRequest } from "@/types/FriendRequest";
import { useUserStore } from "@/store/userStore";

export default defineComponent({
  name: "FriendRequest",
  setup() {
    const users = ref<User[]>([]);
    const friends = ref<User[]>([]);
    const sentRequests = ref<number[]>([]);
    const pendingRequests = ref<FriendRequest[]>([]);

    const loadingUsers = ref(false);
    const loadingRequests = ref(false);
    const loadingFriends = ref(false);

    const userStore = useUserStore();
    const apiBaseUrl = "http://localhost:8000";

    const friendIds = computed(() => friends.value.map((f) => f.id));
    const pendingRequestsFromUserIds = computed(() =>
      pendingRequests.value.map((req) => req.from_user.id)
    );

    const fetchUsers = async () => {
      loadingUsers.value = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/eligible-for-friend-requests/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        const data = await response.json();
        users.value = data.results || [];
      } catch (error) {
        console.error("Error fetching eligible users:", error);
      } finally {
        loadingUsers.value = false;
      }
    };

    const fetchPendingRequests = async () => {
      loadingRequests.value = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/friend-requests/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        const data = await response.json();
        pendingRequests.value = data.requests || [];
      } catch (error) {
        console.error("Error fetching pending requests:", error);
      } finally {
        loadingRequests.value = false;
      }
    };

    const fetchFriends = async () => {
      loadingFriends.value = true;
      try {
        const response = await fetch(`${apiBaseUrl}/api/friends/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        const data = await response.json();
        friends.value = data?.friends || [];
      } catch (error) {
        console.error("Error fetching friends:", error);
      } finally {
        loadingFriends.value = false;
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
      } catch (error) {
        console.error("Error sending friend request:", error);
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
        await fetchPendingRequests();
        await fetchFriends();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    onMounted(() => {
      fetchUsers();
      fetchPendingRequests();
      fetchFriends();
    });

    return {
      users,
      friends,
      sentRequests,
      pendingRequests,
      loadingUsers,
      loadingRequests,
      loadingFriends,
      friendIds,
      pendingRequestsFromUserIds,
      sendFriendRequest,
      acceptFriendRequest,
    };
  },
});
</script>

<style scoped>
.friend-request-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

h2, h3 {
  color: #42b983;
  margin-bottom: 15px;
  text-align: center;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background: white;
  margin-bottom: 10px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.action-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.action-button:hover {
  background-color: #36a572;
}

.loading-message, .no-content-message {
  text-align: center;
  color: #999;
  font-style: italic;
}
</style>
