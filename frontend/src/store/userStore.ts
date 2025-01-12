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
      try {
        const response = await fetch('http://localhost:8000/api/profile/', {
          headers: {
            Authorization: `Bearer ${this.token}`, // Assuming token-based auth
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }

        const data = await response.json();
        this.setUser(data);
      } catch (error) {
        console.error('Error fetching user:', error);
        this.clearUser(); // Logout the user on error
      }
    },
  },
});
