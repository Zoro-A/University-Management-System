<template>
  <div class="container">
    <h2>Enroll / Drop Courses (Student Admin View)</h2>

    <!-- Courses Table -->
    <section class="courses">
      <h3>Available Courses</h3>
      <div v-if="loading" class="loading-message">Loading courses...</div>
      <div v-else-if="allCourses.length === 0" class="empty-message">
        No courses available.
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Credits</th>
            <th>Prerequisites</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in allCourses" :key="c.course_id" :class="{ 'enrolled-row': isEnrolled(c.course_id) }">
            <td>{{ c.course_id }}</td>
            <td>{{ c.course_name || "-" }}</td>
            <td>{{ c.credits ?? "-" }}</td>
            <td>{{ c.prerequisite || c.prerequisites || "-" }}</td>
            <td>
              <span v-if="isEnrolled(c.course_id)" class="enrolled-badge">Already Enrolled</span>
              <span v-else class="not-enrolled-badge">Not Enrolled</span>
            </td>
            <td class="actions-btns">
              <button 
                @click="enrollCourse(c.course_id)" 
                :disabled="isEnrolled(c.course_id)"
                :class="{ 'disabled-btn': isEnrolled(c.course_id) }"
              >
                Enroll
              </button>
              <button 
                v-if="isEnrolled(c.course_id)"
                @click="dropCourse(c.course_id)"
                class="drop-btn"
              >
                Drop
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import apiConfig from "../config/api";

const ADMIN_ID = "A1";
const allCourses = ref([]);
const enrolledCourses = ref([]);
const loading = ref(false);

const statusMsg = ref("");

// Get student ID from localStorage
const getStudentId = () => {
  const userData = JSON.parse(localStorage.getItem("userData"));
  return userData?.id || null;
};

// Check if a course is enrolled
const isEnrolled = (courseId) => {
  return enrolledCourses.value.includes(courseId);
};

async function fetchEnrolledCourses() {
  const studentId = getStudentId();
  if (!studentId) {
    console.error("Student ID not found");
    return;
  }

  try {
    const response = await axios.get(
      `${apiConfig.baseURL}/student/${studentId}/courses`
    );
    enrolledCourses.value = response.data.enrolled_courses || [];
  } catch (err) {
    console.error("Failed to fetch enrolled courses:", err);
    enrolledCourses.value = [];
  }
}

async function fetchCourses() {
  loading.value = true;
  try {
    const res = await axios.get(
      `${apiConfig.baseURL}/admin/${encodeURIComponent(ADMIN_ID)}/courses`
    );
    allCourses.value = Array.isArray(res.data) ? res.data : [];
  } catch (err) {
    console.error("Failed to fetch courses:", err);
    allCourses.value = [];
  } finally {
    loading.value = false;
  }
}

async function enrollCourse(courseId) {
  const studentId = getStudentId();
  if (!studentId) {
    statusMsg.value = "Student ID is required. Please login again.";
    toast.error("Student ID not found. Please login again.", {
      autoClose: 3000,
      position: "top-right",
    });
    return;
  }
  statusMsg.value = "Sending enrollment request...";

  try {
    await axios.post(apiConfig.url("student/enroll"), {
      student_id: studentId,
      course_id: courseId,
    });
    statusMsg.value = `✅ Enrolled in ${courseId}`;
    toast.success("Course Enrolled Successfully!", {
      autoClose: 3000,
      position: "top-right",
      pauseOnHover: true,
      closeOnClick: true,
    });
    // Refresh enrolled courses list to update the filtered view
    await fetchEnrolledCourses();
  } catch (error) {
    toast.error("Failed to enroll. " + (error.response?.data?.detail || "Please try again."), {
      autoClose: 3000,
      position: "top-right",
      pauseOnHover: true,
      closeOnClick: true,
    });
    statusMsg.value = `❌ Failed to enroll in ${courseId}`;
  }
}

async function dropCourse(courseId) {
  const studentId = getStudentId();
  if (!studentId) {
    statusMsg.value = "Student ID is required. Please login again.";
    toast.error("Student ID not found. Please login again.", {
      autoClose: 3000,
      position: "top-right",
    });
    return;
  }

  statusMsg.value = "Sending drop request...";

  try {
    await axios.post(apiConfig.url("student/drop"), {
      student_id: studentId,
      course_id: courseId,
    });
    statusMsg.value = `✅ Dropped ${courseId}`;
    toast.success("Course Dropped Successfully!", {
      autoClose: 3000,
      position: "top-right",
      pauseOnHover: true,
      closeOnClick: true,
    });
    // Refresh enrolled courses list to update the filtered view
    await fetchEnrolledCourses();
  } catch (error) {
    toast.error("Failed to drop course. " + (error.response?.data?.detail || "Please try again."), {
      autoClose: 3000,
      position: "top-right",
      pauseOnHover: true,
      closeOnClick: true,
    });
    statusMsg.value = `❌ Failed to drop ${courseId}`;
  }
}

onMounted(async () => {
  await Promise.all([fetchCourses(), fetchEnrolledCourses()]);
});
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

th,
td {
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

/* Enroll button */
.actions-btns button:first-child {
  background: #2ecc71;
  color: white;
  box-shadow: 0 2px 6px rgba(46, 204, 113, 0.4);
}
.actions-btns button:first-child:hover:not(.disabled-btn) {
  background: #27ae60;
}

/* Disabled enroll button */
.actions-btns .disabled-btn {
  background: #bdc3c7;
  color: #7f8c8d;
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}

.actions-btns .disabled-btn:hover {
  background: #bdc3c7;
}

/* Drop button */
.actions-btns .drop-btn {
  background: #e74c3c;
  color: white;
  box-shadow: 0 2px 6px rgba(231, 76, 60, 0.4);
  margin-left: 8px;
}
.actions-btns .drop-btn:hover {
  background: #c0392b;
}

/* Enrolled row styling */
.enrolled-row {
  background-color: #f0f8f0 !important;
}

.enrolled-row:hover {
  background-color: #e8f5e8 !important;
}

/* Status badges */
.enrolled-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  background-color: #2ecc71;
  color: white;
}

.not-enrolled-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  background-color: #95a5a6;
  color: white;
}

/* Loading and empty states */
.loading-message,
.empty-message {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-size: 16px;
}

.empty-message {
  color: #999;
  font-style: italic;
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
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  font-size: 15px;
  animation: slideUp 0.35s ease;
}

/* Animation for notification */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
