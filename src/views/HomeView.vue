<template>
  <div class="homepage">
    <fieldset class="img-container">
      <img alt="Home page Image" src="@/assets/homepageimage.png" class="h-img" />
    </fieldset>
    <fieldset class="box1">
      <legend class="logo"><img alt="camera logo" class="logo" src="@/assets/camera.svg" width="30" height="30" /> Photogram</legend>
      <p>Share photos of your favourite moments with friends, family and the world.</p> 
      <div class="buttons">
        <button class="btn register" type="submit"><RouterLink class="nav-link"  to="/register">Register</RouterLink></button>
        <button class="btn login" type="submit"><RouterLink class="nav-link"  to="/login">Login</RouterLink></button>
      </div>  
    </fieldset>
  </div>  
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');


.box1 {
  border: 1px solid #ccc;
  padding: 20px;
  width: 400px;
  margin: 10px;
  height: 400px;
  background-color: white;
  border-radius: 5px;
}

.login {
  background-color: rgb(11, 126, 192);
  margin-left: 5px;
  color: white;
}

.register {
  background-color: rgb(150, 247, 4);
  margin-right: 15px;
  color: white;
}

.login:hover {
  background-color: #0b7ec0;
}

.register:hover {
  background-color: #5fdf5f;
}

.buttons {
  display: flex;
  margin-bottom: 50px;
  padding: 5px;
}

.logo-here {
  border-bottom: solid 1px #666;
}

/* Add any component specific styles here */

.logo {
  font-family: 'Lobster', cursive;
  text-align: center;
}

legend {
  border-bottom: solid 1px #666;
}

.homepage {
  display: flex;
  justify-content: center;
}

.img-container {
  display: flex;
  height: 400px;
  align-items: center;
  margin: 10px;

}

.h-img {
  height: 400px;
  border-radius: 5px;
}


</style>
