<template>
    <div class="container">
      <div class="card my-4">
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <img :src="userInfo.profile_photo" class="rounded-circle" :alt="userInfo.username" />
            </div>
            <div class="col-md-8">
              <h5 class="card-title">{{ userInfo.username }}</h5>
              <p class="card-text">{{ userInfo.bio }}</p>
            </div>
          </div>
        </div>
      </div>
  
      <div class="row">
        <div v-for="post in posts" :key="post.id" class="col-md-6 mb-4">
            <img :src="post.photo" class="card-img-top" alt="post image">

        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  let posts = ref([]);
  let userInfo = ref({});
  
  function getUserId() {
    const token = localStorage.getItem('token');
    const decodedToken = JSON.parse(atob(token.split('.')[1]));
    return decodedToken.sub;
  }
  
  function fetchUserInfo() {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + localStorage.getItem('token'),
    };
  
    fetch('/api/v1/users/' + getUserId().value, { headers })
      .then((response) => response.json())
      .then((data) => {
        userInfo.value = data.user;
      });
  }
  
  function fetchPosts() {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + localStorage.getItem('token'),
    };
  
    fetch('api/v1/posts?user_id=' + getUserId(), { headers })
      .then((response) => response.json())
      .then((data) => {
        posts.value = data.posts;
      });
  }
  
  onMounted(() => {
    fetchPosts();
    fetchUserInfo();
  });
  </script>
  
  <style scoped>
  .card {
    border: none;
  }
  
  .card-body {
    padding: 0;
  }
  
  .card-img-top {
    object-fit: cover;
    height: 250px;
  }
  </style>
  