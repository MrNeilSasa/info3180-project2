<script setup>
import {ref, onMounted} from 'vue'
import LoginForm from '../components/LoginForm.vue';

let login = ref([])

</script>

<template>
    <div>
        <h1>Login</h1>
        <LoginForm />
    </div>
</template>

<style>
h1{
    position: absolute;
    left: 35%;
    font-size: 30px;
}
</style>