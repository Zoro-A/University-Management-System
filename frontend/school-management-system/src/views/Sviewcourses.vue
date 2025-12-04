<template>
  <table border="1" cellpadding="8">
    <thead>
      <tr>
        <th>#</th>
        <th>Course ID</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="(course, index) in enrolled_courses" :key="index">
        <td>{{ index + 1 }}</td>
        <td>{{ course }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const enrolled_courses = ref([]);

async function fetchCourses() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    console.error("User not logged in");
    return;
  }

  const userId = userData.id;

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/student/${userId}/courses`
    );

    // ✅ CORRECT DATA ACCESS
    enrolled_courses.value = response.data.enrolled_courses;

    console.log(enrolled_courses.value);
  } catch (error) {
    console.error("Error fetching courses:", error);
  }
}

onMounted(fetchCourses);
</script>
<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  font-family: "Segoe UI", Arial, sans-serif;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

/* Header */
thead {
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
}

th {
  padding: 14px;
  text-align: left;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

/* Body */
tbody tr {
  transition: background 0.2s ease, transform 0.1s ease;
}

tbody tr:nth-child(even) {
  background-color: #f9fafb;
}

tbody tr:nth-child(odd) {
  background-color: #ffffff;
}

tbody tr:hover {
  background-color: #eef2ff;
  transform: scale(1.01);
}

/* Cells */
td {
  padding: 12px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

/* Index Column */
td:first-child {
  font-weight: 600;
  color: #4f46e5;
}

/* Course Code */
td:last-child {
  font-weight: 500;
  color: #111827;
}

/* Empty State */
tbody tr td[colspan] {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
}

/* Mobile Responsive */
@media (max-width: 600px) {
  th,
  td {
    padding: 10px;
    font-size: 13px;
  }

  tbody tr:hover {
    transform: none;
  }
}
</style>
