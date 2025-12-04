<template>
  <div class="dashboard-container">
    <h1>Student Dashboard</h1>
    <p>Welcome to the student dashboard!</p>

    <div class="card-grid">
      <router-link to="/timetable" class="card">Timetable</router-link>
      <router-link to="/transcript" class="card">Transcript</router-link>
      <router-link to="/Sadddropcourse" class="card"
        >Add/Drop Course</router-link
      >
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { userRolestore } from "../store/rolestore";

const userStore = userRolestore();
const router = useRouter();

// Accessing store state
console.log("Role:", userStore.role);
console.log("Username:", userStore.username);
console.log("UserID:", userStore.userid);
</script>
<style scoped>
.dashboard-container {
  text-align: center;
  padding: 40px;
  background: #f5f7fb;
  height: 100vh;
}

h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #333;
}

p {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.card {
  background: white;
  padding: 80px;
  border-radius: 12px;
  text-decoration: none;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: 0.2s ease;
  border: 1px solid #e5e5e5;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  background: #eef4ff;
  border-color: #b5c7ff;
}
</style>
