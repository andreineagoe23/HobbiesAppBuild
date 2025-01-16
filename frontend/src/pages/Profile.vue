<template>
  <div v-if="editableUser" class="profile-container">
    <h2 class="profile-title">Profile</h2>
    <form @submit.prevent="saveProfile" class="profile-form">
      <!-- Name -->
      <div class="form-group">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          id="name"
          class="form-input"
          v-model="editableUser.name"
          placeholder="Enter your name"
          required
        />
      </div>

      <!-- Email -->
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          class="form-input"
          v-model="editableUser.email"
          placeholder="Enter your email"
          required
        />
      </div>

      <!-- Date of Birth -->
      <div class="form-group">
        <label for="date_of_birth" class="form-label">Date of Birth</label>
        <input
          type="date"
          id="date_of_birth"
          class="form-input"
          v-model="editableUser.date_of_birth"
          required
        />
      </div>

      <!-- Hobbies -->
      <div class="form-group">
        <label for="hobbies" class="form-label">Select Hobbies</label>
        <div v-for="hobby in allHobbies" :key="hobby.id" class="form-check">
          <input
            type="checkbox"
            :id="`hobby-${hobby.id}`"
            class="form-check-input"
            :value="hobby.id"
            v-model="selectedHobbies"
          />
          <label :for="`hobby-${hobby.id}`" class="form-check-label">
            {{ hobby.name }}
          </label>
        </div>
      </div>

      <!-- Save Button -->
      <button type="submit" class="action-button">Save Changes</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useUserStore } from "@/store/userStore";
import { Hobby } from "@/types/Hobby";
import { User } from "@/types/User";

export default defineComponent({
  name: "Profile",
  setup() {
    const userStore = useUserStore();
    const editableUser = ref<User | null>(null);
    const allHobbies = ref<Hobby[]>([]);
    const selectedHobbies = ref<number[]>([]);

    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/profile/", {
          headers: {
            Authorization: `Token ${userStore.token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Failed to fetch profile");
        const data = await response.json();
        editableUser.value = {
          id: data.id,
          name: data.name,
          email: data.email,
          date_of_birth: data.date_of_birth,
          hobbies: data.hobbies,
        };
        selectedHobbies.value = data.hobbies.map((hobby: Hobby) => hobby.id);
      } catch (err) {
        console.error("Error fetching profile:", err);
      }
    };

    const fetchHobbies = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/hobbies/", {
          headers: {
            Authorization: `Token ${userStore.token}`,
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        allHobbies.value = await response.json();
      } catch (err) {
        console.error("Error fetching hobbies:", err);
      }
    };

    const saveProfile = async () => {
      if (!editableUser.value) return;

      const payload = {
        name: editableUser.value.name,
        email: editableUser.value.email,
        date_of_birth: editableUser.value.date_of_birth,
        hobbies: selectedHobbies.value,
      };

      try {
        const response = await fetch("http://localhost:8000/api/profile/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${userStore.token}`,
          },
          body: JSON.stringify(payload),
        });
        if (!response.ok) throw new Error("Failed to save profile");
        alert("Profile updated successfully!");
      } catch (err) {
        console.error("Error saving profile:", err);
        alert("An error occurred while updating the profile.");
      }
    };

    onMounted(() => {
      fetchProfile();
      fetchHobbies();
    });

    return {
      editableUser,
      allHobbies,
      selectedHobbies,
      saveProfile,
    };
  },
});
</script>

<style scoped>
.profile-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-title {
  color: #42b983;
  text-align: center;
  margin-bottom: 20px;
}

.profile-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
}

.form-input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.5);
}

.form-check {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-check-input {
  margin-right: 10px;
}

.action-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.action-button:hover {
  background-color: #36a572;
}

.action-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
