<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header text-center bg-primary text-white">
            <h2>Sign Up</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitSignup">
              <!-- Username -->
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  id="username"
                  class="form-control"
                  v-model="formData.username"
                  placeholder="Enter your username"
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
                  v-model="formData.email"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <!-- Password -->
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  id="password"
                  class="form-control"
                  v-model="formData.password"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <!-- Full Name -->
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input
                  type="text"
                  id="name"
                  class="form-control"
                  v-model="formData.name"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <!-- Date of Birth -->
              <div class="mb-3">
                <label for="date_of_birth" class="form-label">Date of Birth</label>
                <input
                  type="date"
                  id="date_of_birth"
                  class="form-control"
                  v-model="formData.date_of_birth"
                  required
                />
              </div>

              <!-- Hobbies -->
              <div class="mb-3">
                <label for="hobbies" class="form-label">Select Hobbies</label>
                <div class="form-check" v-for="hobby in hobbies" :key="hobby.id">
                  <input
                    type="checkbox"
                    :id="`hobby-${hobby.id}`"
                    class="form-check-input"
                    :value="hobby.id"
                    v-model="formData.hobbies"
                  />
                  <label :for="`hobby-${hobby.id}`" class="form-check-label">
                    {{ hobby.name }}
                  </label>
                </div>
              </div>

              <!-- Submit Button -->
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Sign Up</button>
              </div>
            </form>
          </div>
          <div class="card-footer text-muted text-center">
            Already have an account? <a href="/login">Login</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { Hobby } from "@/types/Hobby";

export default defineComponent({
  name: "Signup",
  setup() {
    const formData = ref({
      username: "",
      email: "",
      password: "",
      name: "",
      date_of_birth: "",
      hobbies: [] as number[],
    });

    const hobbies = ref<Hobby[]>([]);
    const error = ref<string | null>(null);

    onMounted(async () => {
      try {
        const response = await fetch("http://localhost:8000/api/hobbies/");
        if (!response.ok) {
          throw new Error(
            `Failed to fetch hobbies: ${response.status} ${response.statusText}`
          );
        }

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          hobbies.value = await response.json();
        } else {
          throw new Error("Received non-JSON response");
        }
      } catch (err) {
        console.error("Error fetching hobbies:", err);
        error.value = "Failed to load hobbies. Please try again later.";
      }
    });

    const submitSignup = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/signup/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData.value),
    });

    if (!response.ok) {
      const errorData = await response.json();
      alert(errorData.error || "Signup failed");
    } else {
      alert("Signup successful! Redirecting...");
      window.location.href = "/";
    }
  } catch (err) {
    console.error("Error during signup:", err);
    alert("An unexpected error occurred. Please try again later.");
  }
};


    return {
      formData,
      hobbies,
      error,
      submitSignup,
    };
  },
});
</script>
