<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Add Faculty (Admin)</h2>

      <input v-model="faculty.faculty_id" placeholder="Faculty ID" />
      <input v-model="faculty.faculty_name" placeholder="Full Name" />
      <input v-model="faculty.email" placeholder="Email" />
      <input type="password" v-model="faculty.password" placeholder="Password" />

      <h3>Eligible Courses</h3>

      <div v-for="(course, index) in faculty.eligible_courses" :key="index" class="course-row">
        <input v-model="faculty.eligible_courses[index]" placeholder="Course ID" />
        <button class="remove-btn" @click="removeCourse(index)">❌</button>
      </div>

      <button class="add-btn" @click="addCourse">+ Add Course</button>
      <button class="submit-btn" @click="submitFaculty">Submit Faculty</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { userRolestore } from '../store/rolestore'
import { ref } from 'vue'

const store = userRolestore()

const faculty = ref({
  faculty_id: "",
  faculty_name: "",
  email: "",
  password: "",
  eligible_courses: [""]
})

function addCourse() {
  faculty.value.eligible_courses.push("")
}

function removeCourse(index) {
  faculty.value.eligible_courses.splice(index, 1)
}

async function submitFaculty() {
  if (!store.userid) {
    alert("Admin ID missing! Please login again.")
    return
  }

  const payload = {
    admin_id: store.userid,
    user_id: faculty.value.faculty_id,
    name: faculty.value.faculty_name,
    email: faculty.value.email,
    password: faculty.value.password,
    courses: faculty.value.eligible_courses.filter(c => c.trim() !== "")
  }

  console.log("Sending faculty payload:", payload)

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/admin/faculty/add',
      payload
    )

    console.log("Response:", response.data)
    alert("✅ Faculty added successfully")

  } catch (err) {
    console.error("Add faculty error:", err.response?.data || err)
    alert("❌ Failed to add faculty — check console for details")
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

/* Form card container */
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

/* Inputs */
.form-card input {
  padding: 10px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  outline: none;
  width: 100%;
  box-sizing: border-box;
}

/* Focus effect */
.form-card input:focus {
  border-color: #3498db;
}

/* Eligible course row */
.course-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* Remove button */
.remove-btn {
  padding: 8px 12px;
  background-color: #e74c3c;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: 0.2s ease;
}

.remove-btn:hover {
  background-color: #c0392b;
}

/* Add course button */
.add-btn {
  padding: 10px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s ease;
}

.add-btn:hover {
  background-color: #27ae60;
}

/* Submit button */
.submit-btn {
  padding: 12px;
  background-color: #3498db;
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
  background-color: #2980b9;
}
</style>
