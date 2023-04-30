<script setup>
import {ref, onMounted} from 'vue'
import PostForm from '../components/PostForm.vue';

let post = ref([])
</script>

<template>
    <div>
        <h1>Post</h1>
        <PostForm />
    </div>
</template>

<style>

</style>


