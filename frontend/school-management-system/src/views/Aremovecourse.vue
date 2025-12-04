<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Remove Course (Admin)</h2>

      <input v-model="course.course_id" placeholder="Course ID" />

      <button class="submit-btn" @click="submitCourse">Remove Course</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios"
import { ref } from "vue"
import { userRolestore } from '../store/rolestore'

const store = userRolestore()

const course = ref({
  course_id: ""
})

async function submitCourse() {
  if (!store.userid) {
    alert("Admin ID missing. Please login first.")
    return
  }

  if (!course.value.course_id.trim()) {
    alert("Please enter a valid Course ID")
    return
  }

  const payload = {
    admin_id: store.userid,
    course_id: course.value.course_id
  }

  console.log("Sending:", payload)

  try {
    await axios.post("http://127.0.0.1:8001/admin/courses/remove", payload)
    alert("✅ Course Removed Successfully!")
    course.value.course_id = ''
  } catch (err) {
    console.error("Backend error:", err.response?.data || err)
    alert("❌ Backend rejected request. Check console for details.")
  }
}
</script>

<style scoped>
/* Center the page */
.page-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  background: #f0f2f5;
  font-family: Arial, sans-serif;
}

/* Form card */
.form-card {
  background-color: #fff;
  padding: 30px 25px;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Heading */
.form-card h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #2c3e50;
}

/* Input */
.form-card input {
  padding: 10px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  outline: none;
  width: 100%;
  box-sizing: border-box;
}

/* Input focus effect */
.form-card input:focus {
  border-color: #e74c3c; /* red for removal */
}

/* Submit button */
.submit-btn {
  padding: 12px;
  background-color: #e74c3c; /* red for remove */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  margin-top: 10px;
  transition: 0.3s ease;
}

.submit-btn:hover {
  background-color: #c0392b;
}
</style>
