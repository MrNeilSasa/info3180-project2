<script setup>
import { ref, onMounted, toRefs } from 'vue';

let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref([]);
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
  let form = document.querySelector("#loginForm");
  let formData = new FormData(form);

  const errors = [];

  if (!formData.get('username') || formData.get('username').trim() === '') {
    errors.push('Error in Username field - This field is required.');
  }

  if (!formData.get('password') || formData.get('password').trim() === '') {
    errors.push('Error in Password field - This field is required.');
  }

  if (errors.length > 0) {
    errorMessage.value = errors;
    return;
  }

  formSubmitted.value = true;

  const jsonData = Object.fromEntries(formData.entries());

  fetch('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify(jsonData),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw response;
      }
    })
    .then((data) => {
      if (data.token) {
        successMessage.value = data.message;
        // You can store the token in localStorage or use it as needed
        localStorage.setItem('token', data.token);
        console.log(data.token);
        window.location.href = '/about';
      } else {
        errorMessage.value = [data.message];
      }
    })
    .catch((error) => {
      error.json().then((data) => {
        if (data.errors) {
          errorMessage.value = data.errors;
        } else {
          errorMessage.value = ["Invalid Credentials."];
        }
        successMessage.value = "";
        console.log(data);
      });
    });
}

</script>

<template>
  <form @submit.prevent="loginUser" id="loginForm" method="post" class="form">
    <div v-if="errorMessage.length">
      <div class="alert alert-danger" v-for="(error, index) in errorMessage" :key="index">
        {{ error }}
      </div>
    </div>

    <div class="form-group mb-3">
      <label for="username" class="form-label">Username</label>
      <input type="text" name="username" v-model="username" class="form-control" />
    </div>

    <div class="form-group mb-3">
      <label for="password" class="form-label">Password</label>
      <input type="password" name="password" v-model="password" class="form-control" />
    </div>

    <button type="submit" class="btn btn-success">Login</button>

    <p v-if="formSubmitted && successMessage" class="alert alert-success">{{ successMessage }}</p>
  </form>
</template>


<style>
.form{
position: absolute;
top: 150px;
left: 475px;
border: 1px solid #ccc;
padding: 20px;
width: 500px;
margin: 0 auto;
background-color: white;
border-radius: 5px;
}

body{
    background-color: rgb(201, 197, 191);
}

h2{
position: absolute;
top: 108px;
left: 475px;

}
button{
    width: 100%;

}
</style>