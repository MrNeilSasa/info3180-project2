

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
          <img alt="camera logo" class="logo" src="@/assets/camera.svg" width="30" height="30" />
           Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/myProfile">My Profile</RouterLink>
            </li>
            
          </ul>
        </div>
      </div>
    </nav>
  </header>
  

</template>

<script setup>
import { RouterLink } from "vue-router";

</script>

<style>
/* Add any component specific styles here */
@import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

.navbar{
  background-color: rgb(11, 126, 192);
  }

.navbar-brand{
  font-family:'Lobster', cursive;
  
} 

.navbar-nav {
  display: flex;
  align-items: center;
}

.navbar-nav ul {
  justify-self: right;
  justify-content: right;
  align-items: right;
  align-self: right;
}

</style>
