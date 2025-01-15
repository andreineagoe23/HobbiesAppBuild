<template>
  <div>
    <!-- display friends -->
    <div>
      <h2>Your Friends</h2>
      <div v-if="loadingFriends">Loading your friends...</div>
      <ul v-else-if="friends.length > 0">
        <li v-for="friend in friends" :key="friend.id">
          <strong>{{ friend.name }}</strong> ({{ friend.email }})
        </li>
      </ul>
      <p v-else>No friends found.</p>
    </div>
    <h2>Friend Requests</h2>

    <!-- display pending frined requests. -->
    <div>
      <h3>Pending Friend Requests</h3>
      <div v-if="loadingRequests">Loading pending requests...</div>
      <ul v-else-if="pendingRequests.length > 0">
        <li v-for="request in pendingRequests" :key="request.id">
          <p>
            <strong>{{ request.from_user.name }}</strong> wants to be your friend!
          </p>
          <button @click="acceptFriendRequest(request.id)">Accept</button>
        </li>
      </ul>
      <p v-else>No pending friend requests.</p>
    </div>

    <!-- send friend reqeusts. -->
    <div>
      <h3>Send Friend Requests</h3>
      <div v-if="loadingUsers || loadingFriends">Loading users...</div>
      <ul v-else-if="users.length > 0">
        <li v-for="user in users" :key="user.id">
          <p>
            <strong>{{ user.name }}</strong> ({{ user.email }})
          </p>

          <div v-if="friendIds.includes(user.id)">
            <em>Already friends</em>
          </div>
          <div v-else-if="pendingRequestsFromUserIds.includes(user.id)">
            <em>They have sent you a friend request</em>
          </div>
          <div v-else-if="sentRequests.includes(user.id)">
            <em>Request Sent</em>
          </div>
          <div v-else>
            <button @click="sendFriendRequest(user.id)">
              Send Friend Request
            </button>
          </div>
        </li>
      </ul>
      <p v-else>No users available to send friend requests.</p>
    </div>

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

    const friendIds = computed<number[]>(() => {
      return friends.value.map((f) => f.id);
    });

    const pendingRequestsFromUserIds = computed<number[]>(() =>
      pendingRequests.value.map((req) => req.from_user.id)
    );

    /**
     * get users to send friend requests to.
     */
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

    /**
     * get incoming friend reqeusts.
     */
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

    /**
     * get existing friends.
     */
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

    /**
     * Send friend requests.
     */
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
        if (!response.ok) {
          throw new Error("Failed to send friend request.");
        }
        sentRequests.value.push(userId);
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    };

    /**
     * accept friend request using id
     */
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
        if (!response.ok) {
          throw new Error("Failed to accept friend request.");
        }
        // refresh after accepting
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
