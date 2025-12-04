<template>
  <div class="container">
    <h2>Enroll / Drop Courses (Student Admin View)</h2>

    <!-- Courses Table -->
    <section class="courses">
      <h3>Available Courses (from admin {{ ADMIN_ID }})</h3>
      <table>
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Credits</th>
            <th>Prerequisites</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in courses" :key="c.course_id">
            <td>{{ c.course_id }}</td>
            <td>{{ c.course_name || '-' }}</td>
            <td>{{ c.credits ?? '-' }}</td>
            <td>{{ c.prerequisite || c.prerequisites || '-' }}</td>
            <td class="actions-btns">
              <button @click="enrollCourse(c.course_id)">Add</button>
              <button @click="dropCourse(c.course_id)">Drop</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Professional Notification Block -->
    <div v-if="statusMsg" class="status-box">
      {{ statusMsg }}
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const ADMIN_ID = 'A1'
const courses = ref([])

const statusMsg = ref('')
const STUDENT_ID = ref('S1')

async function fetchCourses() {
  try {
    const res = await axios.get(`http://127.0.0.1:8001/admin/${encodeURIComponent(ADMIN_ID)}/courses`)
    courses.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    courses.value = []
  }
}

async function enrollCourse(courseId) {
  if (!STUDENT_ID.value) {
    statusMsg.value = 'Student ID is required'
    return
  }
  statusMsg.value = 'Sending enrollment request...'

  try {
    await axios.post('http://127.0.0.1:8001/student/enroll', {
      student_id: STUDENT_ID.value,
      course_id: courseId
    })
    statusMsg.value = `✅ ${STUDENT_ID.value} enrolled in ${courseId}`
  } catch {
    statusMsg.value = `❌ Failed to enroll in ${courseId}`
  }
}

async function dropCourse(courseId) {
  if (!STUDENT_ID.value) return (statusMsg.value = 'Student ID is required')

  statusMsg.value = 'Sending drop request...'

  try {
    await axios.post('http://127.0.0.1:8001/student/drop', {
      student_id: STUDENT_ID.value,
      course_id: courseId
    })
    statusMsg.value = `✅ ${STUDENT_ID.value} dropped ${courseId}`
  } catch {
    statusMsg.value = `❌ Failed to drop ${courseId}`
  }
}

onMounted(fetchCourses)
</script>

<style scoped>
/* Main container */
.container {
  padding: 24px;
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
  background: linear-gradient(135deg, #eef2ff, #f8f9ff);
  min-height: 100vh;
}

/* Page heading */
h2 {
  text-align: center;
  font-size: 26px;
  margin-bottom: 20px;
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

/* Course Section Card */
section {
  margin-top: 16px;
  background: white;
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

/* Subheading */
h3 {
  margin-bottom: 12px;
  font-size: 20px;
  color: #4a6cf7;
  font-weight: 600;
}

/* Table styling */
table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 8px;
}

thead {
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  color: white;
}

th, td {
  padding: 12px;
  text-align: left;
  font-size: 15px;
  border-bottom: 1px solid #eee;
}

tbody tr:nth-child(even) {
  background: #f5f7ff;
}

tbody tr:hover {
  background: #eef2ff;
  transition: 0.2s ease;
}

/* Buttons */
.actions-btns button {
  margin-right: 8px;
  padding: 7px 12px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
}

/* Add button */
.actions-btns button:first-child {
  background: #2ecc71;
  color: white;
  box-shadow: 0 2px 6px rgba(46, 204, 113, 0.4);
}
.actions-btns button:first-child:hover {
  background: #27ae60;
}

/* Drop button */
.actions-btns button:last-child {
  background: #e74c3c;
  color: white;
  box-shadow: 0 2px 6px rgba(231, 76, 60, 0.4);
}
.actions-btns button:last-child:hover {
  background: #c0392b;
}

/* PROFESSIONAL STATUS BOX */
.status-box {
  margin-top: 20px;
  padding: 16px 20px;
  border-radius: 10px;
  font-weight: 600;
  background: #e6eeff;
  color: #2c3e70;
  border-left: 6px solid #4a6cf7;
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
  font-size: 15px;
  animation: slideUp 0.35s ease;
}

/* Animation for notification */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
