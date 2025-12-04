<template>
  <div class="page-center">
    <div class="profile-box">
      <h2>Update Profile</h2>

      <input type="email" placeholder="Email" v-model="email" />
      <input type="text" placeholder="Username" v-model="username" />
      <input type="password" placeholder="Password" v-model="password" />

      <button class="update-button" @click="updateProfile">
        Update Profile
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { userRolestore } from "../store/rolestore";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const router = useRouter();
const userStore = userRolestore();

const username = ref("");
const email = ref("");
const password = ref("");

async function updateProfile() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;
  try {
    if (!userId) {
      alert("Error: No user ID found. Please login again.");
      router.push("/login");
      return;
    }

    // Correct request
    const response = await axios.put(
      "http://127.0.0.1:8000/student/update-profile",
      {
        student_id: userId,
        name: username.value,
        email: email.value,
        password: password.value,
      }
    );
    toast.success("Profile Updated Successfully!", {
      autoClose: 3000,
      position: "top-right",
      pauseOnHover: true,
      closeOnClick: true,
    });
  } catch (error) {
    console.error("updation failed:", error.response?.data || error.message);
  }
}
</script>
<style scoped>
/* Full page center */
.page-center {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eef3f9; /* Soft background like your login page */
  font-family: "Segoe UI", Tahoma, sans-serif;
}

/* White card box */
.profile-box {
  width: 360px;
  padding: 32px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Header */
.profile-box h2 {
  text-align: center;
  margin-bottom: 8px;
  font-size: 22px;
  font-weight: 700;
  color: #222;
}

/* Inputs */
.profile-box input {
  height: 42px;
  padding: 0 12px;
  border: 1px solid #cfd6e1;
  border-radius: 6px;
  font-size: 15px;
  transition: 0.2s;
}

.profile-box input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
  outline: none;
}

/* Button */
.update-button {
  height: 44px;
  background: #2196f3;
  color: white;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: 0.2s;
}

.update-button:hover {
  background: #1976d2;
}
</style>
