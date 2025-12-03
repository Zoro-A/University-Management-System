<template>
  <div class="dashboard-container">
    <h1>Admin Dashboard</h1>
    <p>Welcome, {{ userStore.username }}!</p>

    <div class="cards-container">
      <router-link
        v-for="card in cards"
        :key="card.title"
        :to="card.link"
        class="dashboard-card"
      >
        {{ card.title }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { userRolestore } from "../store/rolestore";
import { ref } from "vue";

const userStore = userRolestore();

// Define dashboard cards
const cards = ref([
  { title: "ADD COURSE", link: "/Aaddcourse" },
  { title: "REMOVE USER", link: "/Aremoveuser" },
  { title: "REMOVE COURSE", link: "/Aremovecourse" },
  { title: "VIEW COURSES", link: "/Aviewcourses" },
  { title: "ADD STUDENT", link: "/Aaddstudent" },
  { title: "ADD FACULTY", link: "/Aaddfaculty" },
  { title: "LIST USERS", link: "/Alistusers" },
  { title: "GENERATE TIMETABLE", link: "/Ageneratetimetable" },
]);
</script>

<style scoped>
/* Container */
.dashboard-container {
  padding: 40px;
  text-align: center;
  font-family: Arial, sans-serif;
  background: #f0f2f5;
  min-height: auto;
  overflow-y: hidden;
}

/* Heading */
.dashboard-container h1 {
  margin-bottom: 10px;
  color: #2c3e50;
}

/* Subheading */
.dashboard-container p {
  margin-bottom: 30px;
  font-size: 18px;
  color: #555;
}

/* Cards grid */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

/* Individual card */
.dashboard-card {
  background-color: #3498db;
  color: white;
  padding: 25px 15px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: bold;
  font-size: 16px;
  transition: 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* Hover effect */
.dashboard-card:hover {
  background-color: #2980b9;
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}
</style>
