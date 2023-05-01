<script setup>
import { ref, onMounted } from "vue";

let posts = ref([]);

function fetchPosts() {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('token'),
  };

  fetch('api/v1/posts', { headers })
    .then((response) => response.json())
    .then((data) => {
      posts.value = data.posts;
    });
}

onMounted(() => {
  fetchPosts();
});

</script>

<template>
  <div class="explore container">
    <div class="row">
      <div class="col-md-8">
        <div class="row">
          <div v-for="post in posts" :key="post.id" class="col-md-6 mb-4">
            <div class="card">
              <img :src="post.photo" class="card-img-top" alt="post image">
              <div class="card-body">
                <h5 class="card-title">{{ post.caption }}</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <button class="btn btn-primary btn-block">New Post</button>
      </div>
    </div>
  </div>
</template>

<style>
</style>
