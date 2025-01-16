<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>
    <FriendRequest />
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
  setup() {
    console.log("MainPage component loaded"); // Debugging log
  },
});
</script>
