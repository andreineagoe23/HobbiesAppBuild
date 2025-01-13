<template>
<<<<<<< HEAD
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
  
=======
  <div>
    <h1>Users List</h1>

    <!-- Filters -->
    <div class="filters">
      <label for="minAge">Min Age:</label>
      <input type="number" id="minAge" v-model="minAge" placeholder="Enter min age" />

      <label for="maxAge">Max Age:</label>
      <input type="number" id="maxAge" placeholder="Enter max age" v-model="maxAge" />

      <button @click="fetchUsers">Filter</button>
    </div>

    <!-- Users Table -->
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Hobbies</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.date_of_birth }}</td>
          <td>{{ user.hobbies.join(', ') }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination">
      <button @click="previousPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  setup() {
    const users = ref([]);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);
    const currentPage = ref(1);
    const totalPages = ref(1);

    const fetchUsers = async () => {
      try {
        // Build query parameters
        const params = new URLSearchParams();
        if (minAge.value !== null) params.append('min_age', String(minAge.value));
        if (maxAge.value !== null) params.append('max_age', String(maxAge.value));
        params.append('page', String(currentPage.value));

        // Fetch users from the API
        const response = await fetch(`http://localhost:8000/api/users/?${params.toString()}`, {
          method: 'GET',
        });

        if (!response.ok) {
          const errorData = await response.json();
          alert(`Error: ${errorData.error || 'Unable to fetch users.'}`);
          return;
        }

        const data = await response.json();
        users.value = data.users;
        totalPages.value = data.total_pages;
      } catch (error) {
        console.error('Error fetching users:', error);
        alert('An error occurred while fetching users.');
      }
    };

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        fetchUsers();
      }
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
        fetchUsers();
      }
    };

    // Fetch users on component mount
    fetchUsers();

    return {
      users,
      minAge,
      maxAge,
      currentPage,
      totalPages,
      fetchUsers,
      previousPage,
      nextPage,
    };
  },
});
</script>

<style scoped>
.filters {
  margin-bottom: 20px;
}

.filters input {
  margin-right: 10px;
}

.filters button {
  padding: 5px 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

.filters button:hover {
  background-color: #369f6e;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f4f4f4;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
>>>>>>> origin/Chun
