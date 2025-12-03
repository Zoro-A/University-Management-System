<template>
  <aside :class="['sidebar', { open: isOpen }]">
    <button class="toggle-btn" @click="toggleSidebar">☰</button>
    <ul>
      <li
        v-for="item in menuItems"
        :key="item.title"
        @click="navigate(item.link)"
      >
        {{ item.title }}
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

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
    { title: "ADD COURSE", link: "/Aaddcourse" },
    { title: "REMOVE USER", link: "/Aremoveuser" },
    { title: "REMOVE COURSE", link: "/Aremovecourse" },
    { title: "VIEW COURSES", link: "/Aviewcourses" },
    { title: "ADD STUDENT", link: "/Aaddstudent" },
    { title: "ADD FACULTY", link: "/Aaddfaculty" },
    { title: "LIST USERS", link: "/Alistusers" },
    { title: "GENERATE TIMETABLE", link: "/Ageneratetimetable" },
  ];

  const student = [
    { title: "Dashboard", link: "/sdashboard" },
    { title: "My Courses", link: "/scourses" },
    { title: "Assignments", link: "/sassignments" },
  ];

  const faculty = [
    { title: "Dashboard", link: "/fdashboard" },
    { title: "Assign Grades", link: "/Fassigngrades" },
    { title: "View Timetable", link: "/Fviewtimetable" },
    { title: "Send Notifications", link: "/FsendNotifications" },
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

.sidebar li:hover {
  background-color: #925fe2;
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
