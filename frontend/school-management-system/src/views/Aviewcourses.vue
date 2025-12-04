<template>
  <div class="table-container">
    <h2>Courses List</h2>
    <table class="courses-table">
      <thead>
        <tr>
          <th>Course ID</th>
          <th>Course Name</th>
          <th>Credits</th>
          <th>Prerequisites</th>
          <th>Eligible Faculty</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.course_id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.course_name }}</td>
          <td>{{ course.credits }}</td>
          <td>{{ course.prerequisite || course.prerequisites || '-' }}</td>
          <td>{{ course.eligible_faculty.length ? course.eligible_faculty.join(', ') : '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { userRolestore } from '../store/rolestore'

const store = userRolestore()
const courses = ref([])

async function fetchCourses() {
  if (!store.userid) {
    console.error("Admin ID missing")
    return
  }

  try {
    const res = await axios.get(`http://127.0.0.1:8001/admin/${store.userid}/courses`)
    courses.value = res.data
  } catch (err) {
    console.error("Error fetching courses:", err.response?.data || err)
  }
}

onMounted(fetchCourses)
</script>

<style scoped>
.table-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

/* Table styling */
.courses-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-radius: 8px;
  overflow: hidden;
}

/* Header */
.courses-table thead {
  background-color: #3498db;
  color: white;
}

.courses-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
}

/* Body rows */
.courses-table tbody tr {
  transition: background-color 0.2s ease;
}

/* Alternating row colors for contrast */
.courses-table tbody tr:nth-child(odd) {
  background-color: #f8f9fa;
}
.courses-table tbody tr:nth-child(even) {
  background-color: #ffffff;
}

/* Hover effect */
.courses-table tbody tr:hover {
  background-color: #e1f0ff;
}

/* Cells */
.courses-table td {
  padding: 12px;
  border: none;
}
</style>
