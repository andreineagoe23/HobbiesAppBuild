import { defineStore } from 'pinia';

interface User {
  id: number;
  name: string;
  email: string;
  dob: string;
  hobbies: string[];
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: '' as string,
  }),
  actions: {
    setUser(user: User) {
      this.user = user;
    },
    setToken(token: string) {
      this.token = token;
    },
  },
});
