import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { createPinia } from 'pinia';



const app = createApp(App);

// Create a Pinia instance
const pinia = createPinia();

// Use Pinia and Vue Router in the app
app.use(pinia);
app.use(router);

// Mount the app to the DOM
app.mount('#app');