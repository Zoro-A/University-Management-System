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
        <img
          :src="card.img"
          class="card-icon"
          alt="icon"
          width="20"
          height="20"
        />
        {{ card.title }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { userRolestore } from "../store/rolestore";
import { ref } from "vue";
import addCourse from "@/assets/images/addCourse.svg";
import removeUser from "@/assets/images/removeUser.svg";
import removeCourse from "@/assets/images/removeCourse.svg";
import viewCourse from "@/assets/images/viewCourse.svg";
import addUser from "@/assets/images/addUser.svg";
import listUsers from "@/assets/images/listUsers.svg";
import generateTimeTable from "@/assets/images/generateTimeTable.svg";

const userStore = userRolestore();

const cards = ref([
  { title: "ADD COURSE", link: "/Aaddcourse", img: addCourse },
  { title: "REMOVE USER", link: "/Aremoveuser", img: removeUser },
  { title: "REMOVE COURSE", link: "/Aremovecourse", img: removeCourse },
  { title: "VIEW COURSES", link: "/Aviewcourses", img: viewCourse },
  { title: "ADD STUDENT", link: "/Aaddstudent", img: addUser },
  { title: "ADD FACULTY", link: "/Aaddfaculty", img: addUser },
  { title: "LIST USERS", link: "/Alistusers", img: listUsers },
  {
    title: "GENERATE TIMETABLE",
    link: "/Ageneratetimetable",
    img: generateTimeTable,
  },
]);
</script>

<style scoped>
/* Container */
.dashboard-container {
  padding: 40px;
  text-align: center;
  font-family: Arial, sans-serif;
  background: #f0f2f5;
  min-height: 100vh;
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
.card-icon {
  margin-right: 15px;
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
  white-space: nowrap;
}

/* Hover effect */
.dashboard-card:hover {
  background-color: #2980b9;
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}
</style>
