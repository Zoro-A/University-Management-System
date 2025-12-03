<template>
  <div class="login-container">

    <div class="admin-button">
      <button @click="selectRole('admin')">Admin</button>
    </div>

    <div class="student-button">
      <button @click="selectRole('student')">Student</button>
    </div>

    <div class="faculty-button">
      <button @click="selectRole('faculty')">Faculty</button>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { userRolestore } from '../store/rolestore'
import { onMounted } from 'vue'

const router = useRouter()
const userStore = userRolestore()

onMounted(() => {
  userStore.resetAll()
  console.log("Store reset:", userStore.role, userStore.username, userStore.userid)
})

function selectRole(role) {
  userStore.setRole(role)
  console.log("Selected role:", userStore.role)
  router.push("/login")
}
</script>

<style scoped>
/* Center everything */
.login-container {
  height: 100vh;              /* full screen height */
  display: flex;
  justify-content: center;    /* center horizontally */
  align-items: center;        /* center vertically */
  flex-direction: column;     /* stack buttons vertically */
  gap: 20px;                  /* space between buttons */
}

/* Button styling */
button {
  width: 200px;
  padding: 12px;
  font-size: 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s ease;
}

/* Individual colors */
.admin-button button {
  background-color: #3498db;
  color: white;
}

.student-button button {
  background-color: #2ecc71;
  color: white;
}

.faculty-button button {
  background-color: #f39c12;
  color: white;
}

/* Hover effect */
button:hover {
  transform: scale(1.05);
  opacity: 0.9;
}
</style>
