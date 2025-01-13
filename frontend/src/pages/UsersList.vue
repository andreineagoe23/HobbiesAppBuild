<template>
  <div class="users-list-container">
    <h1>Users List</h1>

    <!-- Filter Section -->
    <section class="filter-section">
      <h2>Filter Users</h2>
      <div class="filter-controls">
        <label>
          Min Age:
          <input type="number" v-model="minAge" placeholder="Enter minimum age" />
        </label>
        <label>
          Max Age:
          <input type="number" v-model="maxAge" placeholder="Enter maximum age" />
        </label>
        <button @click="fetchUsers" class="filter-button">Apply Filters</button>
      </div>
    </section>

    <!-- Users List -->
    <section class="users-list">
      <h2>Users</h2>
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
        console.log("Fetching users with params:", params.toString());
        const response = await fetch(`${apiBaseUrl}/api/users/?${params}`, {
          headers: { Authorization: `Token ${userStore.token}` },
        });
        if (!response.ok) throw new Error("Failed to fetch users.");
        const data = await response.json();
        console.log("Fetched users:", data);

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
