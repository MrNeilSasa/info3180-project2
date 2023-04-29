<script setup> 

import { ref, onMounted, toRefs } from 'vue';
let csrf_token = ref("");


let successMessage = ref("");
let errorMessage = ref([]);

let profilePic = ref(null);

const state = toRefs({ profilePic, csrf_token, successMessage, errorMessage });

function getCsrfToken(){
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
}

onMounted(() => {
    getCsrfToken();
});

function createUser()  {
    let form = document.querySelector("#registration");
    let formData = new FormData(form);

    const firstname = formData.get('firstname');
    const lastname = formData.get('lastname');
    const username = formData.get('username');
    const password = formData.get('password');
    const email = formData.get('email');
    const location = formData.get('location');
    const biography = formData.get('biography');
    const profile_photo = state.profilePic.value.files[0];
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    let errors = [];

    if (!firstname || firstname.trim() === '') {
        errors.push('Error in First Name field - This field is required.');
    }

    if (!lastname || lastname.trim() === '') {
        errors.push('Error in Last Name field - This field is required.');
    }

    if (!username || username.trim() === '') {
        errors.push('Error in Username field - This field is required.');
    }

    if (!password || password.trim() === ''){
        errors.push('Error in Password field - This field is required.');
    } else if (!passwordPattern.test(password)) {
        errors.push('Error in Password field - Password must be at least 8 characters long and contain at least one letter and one number.');
    }


    if (!email || email.trim() === '') {
        errors.push('Error in Email field - This field is required.');
    } else if (!emailPattern.test(email)) {
        errors.push('Error in Email field - Please enter a valid email address.');
    }
    if (!location || location.trim() === '') {
        errors.push('Error in Location field - This field is required.');
    }

    if (!biography || biography.trim() === '') {
        errors.push('Error in Biography field - This field is required.');
    }

    if (!profile_photo) {
        errors.push("Error in Poster field - A Photo is required in this field.");
    } else {
        const fileType = profile_photo.type;
        if (!(fileType === "image/jpeg" || fileType === "image/png")) {
            errors.push("Poster must be a JPG or PNG image.");
        }
    }

    if (errors.length > 0) {
        errorMessage.value = errors;
        return;
    }

    console.log(Array.from(formData.entries()));


    fetch("/api/v1/users/register", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token.value,
        }
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw response;
        }
    })
    .then((data) => {
        successMessage.value = "Account successfully created!";
        errorMessage.value = [];
        console.log(data);
    })
    .catch((error) => {
        error.json().then((data) => {
            if (data.errors) {
                errorMessage.value = data.errors;
            } else {
                errorMessage.value = ["An unexpected error occurred."];
            }
            successMessage.value = "";
            console.log(data);
        });
    });

};





</script>



<style scoped>

</style>

<template>
<form @submit.prevent="createUser" id="registration" method="post" class = "form">
    <div class="alert alert-success" v-if="successMessage">{{ successMessage }}</div>

    <div v-if="errorMessage.length">
      <div class="alert alert-danger" v-for="(error, index) in errorMessage" :key="index">
        {{ error }}
      </div>
    </div>
    <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" name="username" class="form-control" />
    </div>
    <div class="form-group mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" name="password" class="form-control" />
    </div>
    <div class="form-group mb-3">
        <label for="firstname" class="form-label">First Name</label>
        <input type="text" name="firstname" class="form-control" />
    </div>
    <div class="form-group mb-3">
        <label for="lastname" class="form-label">Last Name</label>
        <input type="text" name="lastname" class="form-control" />
    </div>

    <div class="form-group mb-3">
        <label for="location" class="form-label">Location</label>
        <input type="text" name="location" class="form-control" />
    </div>
    
    <div class="form-group mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" name="email" class="form-control" />
    </div>
    <div class="form-group mb-3">
        <label for="biography" class="form-label">Biography</label>
        <textarea id="biography" name="biography" rows="5" class="form-control"></textarea>
    </div>
    <div class="form-group mb-3">
        <label for="profile_photo" class="form-label">Photo</label>
        <input type="file" name="profile_photo" class="form-control" ref="profilePic">
    </div>
    <button type="submit" class="btn btn-success">Register</button>

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
    background-color: antiquewhite;
}

h2{
position: absolute;
top: 108px;
left: 475px;

}
button{
    width: 100%;

}

input[type="file"] {
  background-color: #f1f1f1;
  border: 1px solid #ccc;
  color: #333;
  font-size: 16px;
  padding: 10px;
}

</style>