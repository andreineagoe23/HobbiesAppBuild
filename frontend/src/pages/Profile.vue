<template>
  <div v-if="editableUser">
    <h2>Profile</h2>
    <p>Name: {{ editableUser.name }}</p>
    <p>Email: {{ editableUser.email }}</p>
    <p>Date of Birth: {{ editableUser.dob }}</p>
    <ul>
      <!-- Use hobby.id as the key and hobby.name for display -->
      <li v-for="hobby in editableUser.hobbies" :key="hobby.id">
        {{ hobby.name }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { User } from '@/types/User';
import { Hobby } from '@/types/Hobby';

export default defineComponent({
  data() {
    return {
      editableUser: null as User | null,
    };
  },
  mounted() {
    this.editableUser = {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@example.com',
      dob: '1990-01-01',
      hobbies: [
        { id: 1, name: 'Reading' },
        { id: 2, name: 'Traveling' },
      ] as Hobby[],
    };
  },
});
</script>
