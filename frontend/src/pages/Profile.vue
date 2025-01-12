<template>
  <div v-if="editableUser" class="container mt-5">
    <h2>Profile</h2>
    <form @submit.prevent="saveProfile">
      <!-- Name -->
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          id="name"
          class="form-control"
          v-model="editableUser.name"
          placeholder="Enter your name"
          required
        />
      </div>

      <!-- Email -->
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          class="form-control"
          v-model="editableUser.email"
          placeholder="Enter your email"
          required
        />
      </div>

      <!-- Date of Birth -->
      <div class="mb-3">
        <label for="dob" class="form-label">Date of Birth</label>
        <input
          type="date"
          id="dob"
          class="form-control"
          v-model="editableUser.dob"
          required
        />
      </div>

      <!-- Hobbies -->
      <div class="mb-3">
        <label for="hobbies" class="form-label">Select Hobbies</label>
        <div
          v-for="hobby in allHobbies"
          :key="hobby.id"
          class="form-check"
        >
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
      <button type="submit" class="btn btn-primary">Save Changes</button>
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

    // Fetch profile and hobbies
    const fetchProfile = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/profile/", {
      headers: {
        Authorization: `Token ${userStore.token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch profile");
    }

    const data = await response.json();
    editableUser.value = {
      id: data.id,
      name: data.name,
      email: data.email,
      dob: data.date_of_birth,
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

    if (!response.ok) {
      throw new Error("Failed to fetch hobbies");
    }

    allHobbies.value = await response.json();
  } catch (err) {
    console.error("Error fetching hobbies:", err);
  }
};


    // Save profile changes
    const saveProfile = async () => {
  if (!editableUser.value) return;

  const payload = {
    name: editableUser.value.name,
    email: editableUser.value.email,
    date_of_birth: editableUser.value.dob,
    hobbies: selectedHobbies.value.filter((id) => id !== null && id !== undefined), // Remove invalid IDs
  };

  console.log("Payload being sent:", payload);

  try {
    const response = await fetch("http://localhost:8000/api/profile/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${userStore.token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response from backend:", errorData);
      throw new Error("Failed to save profile");
    }

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
