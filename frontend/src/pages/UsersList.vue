<template>
    <div>
      <!-- similar users list -->
      <h1>Similar Users</h1>
        <p>Here are some users similar to you:</p>
      <ul>
        <li v-for="user in similarUsers" :key="user.user_id">
          <span>{{ user.username }} - Similarity Score: {{ user.similarity_score }}</span>
          <!-- similarity score rn here to test if correct users are displayed -->
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default { 
    data() {
      return {
        similarUsers: [] // array of similar users
      };
    },
    mounted() {
      this.fetchSimilarUsers(); // fetch similar users when the component is mounted
    },
    methods: {
      async fetchSimilarUsers() {
        try {
          const response = await fetch('/api/similar-users'); // fetch similar users from the API from the URL
          console.log(response.data);
          const data = await response.json(); // parse the JSON response
          this.similarUsers = data.similar_users; // assign the similar users to the data
        } catch (error) {
          console.error("There was an error fetching the similar users:", error);
        }
      }
    }
  };
  </script>
  