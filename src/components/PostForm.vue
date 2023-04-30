<script setup>
import { ref, onMounted, toRefs } from 'vue';
let csrf_token = ref("");

let successMessage = ref("");
let errorMessage = ref([]);

let postPic = ref(null);
let user_id = ref(null);

const state = toRefs({ postPic, csrf_token, successMessage, errorMessage });

function getCsrfToken(){
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
}

function getUserId(){
   const token = localStorage.getItem('token');
   const decodedToken = JSON.parse(atob(token.split('.')[1]));
   user_id.value = decodedToken.sub;
}

onMounted(() => {
    getCsrfToken();
    getUserId();
});

function createPost()  {
    let form = document.querySelector("#newPost");
    let formData = new FormData(form)

    const post_photo = state.postPic.value.files[0];
    const caption = formData.get('caption');

    let errors = [];

    if (!caption || caption.trim() === '') {
        errors.push('Error in Caption field - This field is required.');
    }

    if (!post_photo) {
        errors.push("Error in Photo field - A Photo is required in this field.");
    } else {
        const fileType = post_photo.type;
        if (!(fileType === "image/jpeg" || fileType === "image/png")) {
            errors.push("Photo must be a JPG or PNG image.");
        }
    }

    if (errors.length > 0) {
        errorMessage.value = errors;
        return;
    }

    console.log(Array.from(formData.entries()));

    fetch("/api/v1/users/${user_id.value}/posts", {
        method: 'POST',
        body: formData,
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrf_token.value,
            'Authorization': `Bearer ${localStorage.getItem('token')}`
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
        successMessage.value = "Post successfully created!";
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



}
</script>

<style scoped>

</style>

<template>
<form @submit.prevent="createPost" id="newPost" method="post" class = "form">
    <div class="alert alert-success" v-if="successMessage">{{ successMessage }}</div>

    <div v-if="errorMessage.length">
      <div class="alert alert-danger" v-for="(error, index) in errorMessage" :key="index">
        {{ error }}
      </div>
    </div>
    <div class="form-group mb-3">
        <label for="post_photo" class="form-label">Photo</label>
        <input type="file" name="post_photo" class="form-control" ref="postPic">
    </div>
    <div class="form-group mb-3">
        <label for="caption" class="form-label">Caption</label>
        <textarea id="caption" name="caption" rows="5" class="form-control"></textarea>
    </div>
    <button type="submit" class="btn btn-success">Submit</button>
</form>

</template>