<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Login</h2>

      <input type="text" placeholder="Email" v-model="email" />
      <input type="password" placeholder="Password" v-model="password" />

      <button type="submit" class="login-button" @click="login">Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { userRolestore } from "../store/rolestore";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const store = userRolestore();
const router = useRouter();

const email = ref("");
const password = ref("");

async function login() {
  try {
    const response = await axios.post("http://127.0.0.1:8000/auth/login", {
      email: email.value,
      password: password.value,
      role: store.role,
    });

    if (response.status === 200) {
      const user = response.data.user;

      // Save data to store
      store.setUser(user.user_id, user.name);

      // Save login info as a single object in localStorage
      const userData = {
        name: user.name,
        email: email.value,
        role: store.role,
        id: store.userid,
      };
      localStorage.setItem("userData", JSON.stringify(userData));

      // Navigate based on role
      if (store.role === "admin") router.push("/adashboard");
      else if (store.role === "student") router.push("/sdashboard");
      else if (store.role === "faculty") router.push("/fdashboard");

      toast.success("Login Successful!", {
        autoClose: 8000,
        position: "top-right",
        pauseOnHover: true,
        closeOnClick: true,
      });
    }
  } catch (error) {
    console.error("Login failed:", error.response?.data || error.message);
    toast.error("Login failed. Please check your credentials.", {
      autoClose: 5000,
      position: "top-right",
    });
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
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
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
