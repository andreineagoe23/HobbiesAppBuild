<template>
  <div class="users-list-container">
    <h1 class="title">Users List</h1>

    <!-- Filter Section -->
    <section class="filter-section">
      <h2 class="section-title">Filter Users</h2>
      <div class="filter-controls">
        <label class="filter-label">
          Min Age:
          <input type="number" v-model="minAge" class="filter-input" placeholder="Enter minimum age" />
        </label>
        <label class="filter-label">
          Max Age:
          <input type="number" v-model="maxAge" class="filter-input" placeholder="Enter maximum age" />
        </label>
        <button @click="fetchUsers" class="action-button">Apply Filters</button>
      </div>
    </section>

    <!-- Users List -->
    <section class="users-list">
      <h2 class="section-title">Users</h2>
      <ul>
        <li v-for="user in users" :key="user.id" class="user-item">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Date of Birth:</strong> {{ user.date_of_birth }}</p>
          <p>
            <strong>Hobbies:</strong>
            <span v-if="user.hobbies.length">
              <span v-for="(hobby, index) in user.hobbies" :key="hobby.id">
                {{ hobby.name }}<span v-if="index < user.hobbies.length - 1">, </span>
              </span>
            </span>
            <span v-else>No hobbies listed</span>
          </p>
          <p><strong>Age:</strong> {{ calculateAge(user.date_of_birth) }} years old</p>
        </li>
      </ul>
    </section>

    <!-- Pagination Controls -->
    <section class="pagination-controls">
      <button :disabled="currentPage === 1" @click="changePage(-1)" class="pagination-button">Previous</button>
      <button :disabled="currentPage === totalPages" @click="changePage(1)" class="pagination-button">Next</button>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from "vue";
import { User } from "@/types/User";
import "@/styles/usersList.css";
import { useUserStore } from "@/store/userStore";

export default defineComponent({
  name: "UsersList",
  setup() {
    const users = reactive<User[]>([]);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);
    const currentPage = ref(1);
    const totalPages = ref(1);

    const userStore = useUserStore();
    const apiBaseUrl = "http://localhost:8000";

    const fetchUsers = async () => {
      const params = new URLSearchParams();
      if (minAge.value !== null) params.append("min_age", minAge.value.toString());
      if (maxAge.value !== null) params.append("max_age", maxAge.value.toString());
      params.append("page", currentPage.value.toString());

      try {
        const response = await fetch(`${apiBaseUrl}/api/users/?${params}`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        if (!response.ok) throw new Error("Failed to fetch users.");
        const data = await response.json();
        users.splice(0, users.length, ...data.results);
        totalPages.value = data.total_pages;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    const changePage = (delta: number) => {
      currentPage.value += delta;
      fetchUsers();
    };

    const calculateAge = (dob: string): number => {
      const birthDate = new Date(dob);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      if (
        today.getMonth() < birthDate.getMonth() ||
        (today.getMonth() === birthDate.getMonth() && today.getDate() < birthDate.getDate())
      ) {
        age--;
      }
      return age;
    };

    onMounted(() => {
      fetchUsers();
    });

    return {
      users,
      minAge,
      maxAge,
      currentPage,
      totalPages,
      fetchUsers,
      changePage,
      calculateAge,
    };
  },
});
</script>

<style scoped>
.users-list-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.title {
  color: #42b983;
  text-align: center;
  margin-bottom: 20px;
}

.section-title {
  color: #2c3e50;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.filter-controls {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 20px;
}

.filter-label {
  display: flex;
  flex-direction: column;
  font-weight: bold;
  color: #2c3e50;
}

.filter-input {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.filter-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5);
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

.users-list ul {
  list-style: none;
  padding: 0;
}

.user-item {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-item p {
  margin: 5px 0;
}

.pagination-controls {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.pagination-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-button:hover:not(:disabled) {
  background-color: #36a572;
}
</style>
