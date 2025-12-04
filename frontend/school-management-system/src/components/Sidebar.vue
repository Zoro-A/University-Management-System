<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <button class="toggle-btn" @click="toggleSidebar">☰</button>

    <ul class="sidebar-items">
      <li
        v-for="item in menuItems"
        :key="item.title"
        @click="navigate(item.link)"
      >
        <img
          :src="item.img"
          class="sidebar-icon"
          alt="icon"
          width="20"
          height="20"
        />

        {{ item.title }}
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import addCourse from "@/assets/images/addCourse.svg";
import removeUser from "@/assets/images/removeUser.svg";
import removeCourse from "@/assets/images/removeCourse.svg";
import viewCourse from "@/assets/images/viewCourse.svg";
import addUser from "@/assets/images/addUser.svg";
import listUsers from "@/assets/images/listUsers.svg";
import generateTimeTable from "@/assets/images/generateTimeTable.svg";
import dashboard from "@/assets/images/dashboard.svg";
import transcript from "@/assets/images/transcript.svg";
import myCourses from "@/assets/images/myCourses.svg";
import assignGrades from "@/assets/images/assignGrades.svg";
import notification from "@/assets/images/notifications.svg";

const router = useRouter();
const isOpen = ref(true);
const role = ref(""); // role from localStorage

onMounted(() => {
  const userData = JSON.parse(localStorage.getItem("userData"));
  if (userData && userData.role) role.value = userData.role;
});

// Role-based menus
const menuItems = computed(() => {
  const admin = [
    { title: "Dashboard", link: "/adashboard", img: dashboard },
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
  ];

  const student = [
    {
      title: "Dashboard",
      link: "/sdashboard",
      img: dashboard,
    },
    { title: "My Courses", link: "/scourses", img: myCourses },
    { title: "Transcript", link: "/transcript", img: transcript },
    { title: "Add or drop course", link: "/Sadddropcourse", img: removeCourse },
  ];

  const faculty = [
    { title: "Dashboard", link: "/fdashboard", img: dashboard },
    { title: "Assign Grades", link: "/Fassigngrades", img: assignGrades },
    {
      title: "View Timetable",
      link: "/Fviewtimetable",
      img: generateTimeTable,
    },
    {
      title: "Send Notifications",
      link: "/FsendNotifications",
      img: notification,
    },
  ];

  if (role.value === "admin") return admin;
  if (role.value === "student") return student;
  if (role.value === "faculty") return faculty;
  return [];
});

function toggleSidebar() {
  isOpen.value = !isOpen.value;
}

function navigate(path) {
  router.push(path);
}
</script>

<style scoped>
.sidebar-icon {
  margin-top: 35px;
  margin-right: 10px;
}
.sidebar {
  width: 280px;
  background-image: linear-gradient(to bottom right, #a277e6, #6326c5);
  color: white;
  padding: 20px;
  box-sizing: border-box;
  transition: all 0.3s;
}
.sidebar li {
  margin-top: 10px;
  padding: 10px 0;
  cursor: pointer;
  margin-bottom: 20px; /* Add this line to increase spacing */
}

.sidebar li:last-child {
  margin-bottom: 0; /* Optional: remove margin from the last item */
}

.sidebar.closed {
  width: 60px;
}

.sidebar .toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px 0;
  cursor: pointer;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -220px;
    top: 0;
    z-index: 1000;
  }

  .sidebar.open {
    left: 0;
  }
}
</style>
