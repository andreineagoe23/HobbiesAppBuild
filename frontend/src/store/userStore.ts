import { defineStore } from "pinia";
import { User } from "@/types/User";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("authToken") || "" as string | null, // Initialize with localStorage token
    user: null as User | null,
  }),
  actions: {
    // Set the token and store it in localStorage
    setToken(newToken: string) {
      this.token = newToken;
      localStorage.setItem("authToken", newToken);
    },

    // Set user data
    setUser(newUser: User) {
      this.user = newUser;
    },

    // Fetch the authenticated user's data
    async fetchUser() {
      if (!this.token) {
        console.warn("Cannot fetch user without a token");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/api/profile/", {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        if (!response.ok) throw new Error("Failed to fetch user data");
        const data = await response.json();
        console.log("Fetched user data:", data); // Debugging log
        this.setUser(data); // Set user in store
      } catch (error) {
        console.error("Error fetching user data:", error);
        this.clearUser();
      }
    },

    // Clear token and user data
    clearUser() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("authToken");
    },
  },
});
