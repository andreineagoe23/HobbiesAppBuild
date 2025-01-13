<template>
  <div>
    <h1>Main Page</h1>
    <UsersList />
    <FriendRequests />
  </div>
</template>

<script lang="ts">
import UsersList from './UsersList.vue';
import FriendRequests from './FriendRequest.vue';

export default {
  components: {
    UsersList,
    FriendRequests,
  },
};
</script>
