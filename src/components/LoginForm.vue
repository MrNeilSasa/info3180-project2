<script setup>
import { ref, onMounted, toRefs } from 'vue';

let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref("");
let formSubmitted = ref(false);

const state = toRefs({ csrf_token, successMessage, errorMessage });
let username = ref("");
let password = ref("");

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

onMounted(() => {
  getCsrfToken();
});

function loginUser() {
  formSubmitted.value = true;
  fetch('http://localhost:8080/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.token) {
        successMessage.value = data.message;
        // You can store the token in localStorage or use it as needed
        localStorage.setItem('token', data.token);
      } else {
        errorMessage.value = data.message;
      }
    });
}
</script>

<template>
  <form @submit.prevent="loginUser" id="loginForm" method="post">
    <h2>Login</h2>

    <div class="mb-3">
      <label for="username" class="form-label">Username</label>
      <input v-model="username" type="text" class="form-control" id="username" placeholder="Enter User Name">
    </div>

    <div class="mb-3">
      <label for="password" class="form-label">Password</label>
      <input v-model="password" type="password" class="form-control" id="password" placeholder="Enter Password">
    </div>

    <p v-if="formSubmitted && successMessage" class="alert alert-success">{{ successMessage }}</p>
    <p v-if="formSubmitted && errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
    
    <button class="btn btn-success" type="submit">Login</button>
  </form>
</template>
