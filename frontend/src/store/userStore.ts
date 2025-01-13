import { defineStore } from 'pinia';
import { User } from '../types/User';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null, // Current authenticated user
    token: '' as string,       // Authentication token
  }),
  actions: {
    /**
     * Sets the authenticated user.
     * @param user - The user object
     */
    setUser(user: User) {
      this.user = user;
    },

    /**
     * Clears the user and token (logout functionality).
     */
    clearUser() {
      this.user = null;
      this.token = '';
      localStorage.removeItem('authToken'); // Clear token from local storage
    },

    /**
     * Sets the authentication token.
     * @param token - The token string
     */
    setToken(token: string) {
      this.token = token;
      localStorage.setItem('authToken', token); // Save token in local storage
    },

    /**
     * Fetches the current user using the stored token.
     */
    async fetchUser() {
      const token = localStorage.getItem("authToken");
if (!token) {
    console.error("No token found!");
    return;
}

  
      try {
          const response = await fetch("http://localhost:8000/api/profile/", {
              method: "GET",
              headers: {
                  "Authorization": `Token ${token}`,
                  "Content-Type": "application/json",
              },
          });
  
          if (response.status === 401) {
              console.error("Unauthorized: Invalid token");
              throw new Error("Unauthorized access");
          }
  
          const userData = await response.json();
          this.setUser(userData);
          console.log("Fetched user data:", userData);
      } catch (err) {
          console.error("Failed to fetch user data", err);
      }
  }
   
    ,
  },
});
