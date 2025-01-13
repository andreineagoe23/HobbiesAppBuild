<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>

    <section>
      <h2>Your Friend Requests</h2>
      <FriendRequest />
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import FriendRequest from "@/pages/FriendRequest.vue";

export default defineComponent({
  name: "MainPage",
  components: {
    FriendRequest,
  },
});
</script>
