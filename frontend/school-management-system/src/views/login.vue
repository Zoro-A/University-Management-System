<template>
  <div class="login-page">

    <div class="login-card">
      <h2>Login</h2>

      <input type="text" placeholder="Email" v-model="email" />
      <input type="password" placeholder="Password" v-model="password" />

      <button class="login-button" @click="login">Login</button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { userRolestore } from '../store/rolestore'

const store = userRolestore()
const router = useRouter()

const email = ref('')
const password = ref('')

async function login() {
  try {
    const response = await axios.post("http://127.0.0.1:8000/auth/login", {
      email: email.value,
      password: password.value,
      role: store.role
    })

    console.log("Login success:", response.data)

    if (response.status === 200) {
      store.setUser(response.data.user.user_id, response.data.user.name)
      alert("Login Successful")

      if (store.role === 'admin') router.push('/adashboard')
      else if (store.role === 'student') router.push('/sdashboard')
      else if (store.role === 'faculty') router.push('/fdashboard')
    }

  } catch (error) {
    console.error("Login failed:", error.response?.data || error.message)
    alert("Login failed: " + (error.response?.data?.detail || error.message))
  }
}
</script>

<style scoped>
/* Page setup */
.login-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to right, #dfe9f3, #ffffff);
}

/* Login card */
.login-card {
  width: 320px;
  padding: 25px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Heading */
.login-card h2 {
  text-align: center;
  margin-bottom: 10px;
}

/* Inputs */
.login-card input {
  padding: 10px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  outline: none;
}

/* Focus effect */
.login-card input:focus {
  border-color: #3498db;
}

/* Button */
.login-button {
  padding: 10px;
  font-size: 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s ease;
}

/* Hover */
.login-button:hover {
  background-color: #2980b9;
}
</style>
