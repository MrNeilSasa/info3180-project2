<script setup>
import {ref, onMounted} from 'vue'
import RegisterForm from '../components/RegisterForm.vue';

let register = ref([])

</script>

<template>
    <div>
        <h1>Register</h1>
        <RegisterForm />
    </div>
</template>

<style>

</style>