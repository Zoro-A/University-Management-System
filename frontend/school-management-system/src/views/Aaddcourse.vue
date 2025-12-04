<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Add Course (Admin)</h2>

      <input v-model="course.course_id" placeholder="Course ID" />
      <input v-model="course.name" placeholder="Course Name" />
      <input
        type="number"
        v-model.number="course.credits"
        placeholder="Credits"
      />
      <input v-model="course.prerequisites" placeholder="Prerequisites" />

      <h3>Eligible Faculty</h3>

      <div
        v-for="(faculty, index) in course.eligible_faculty"
        :key="index"
        class="faculty-row"
      >
        <input
          v-model="course.eligible_faculty[index]"
          placeholder="Faculty ID"
        />
        <button class="remove-btn" @click="removeFaculty(index)">❌</button>
      </div>

      <button class="add-btn" @click="addFaculty">+ Add Faculty</button>

      <button class="submit-btn" @click="submitCourse">Submit Course</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { userRolestore } from "../store/rolestore";

const store = userRolestore();

const course = ref({
  course_id: "",
  name: "",
  eligible_faculty: [""],
  credits: 0,
  prerequisites: "",
});

function addFaculty() {
  course.value.eligible_faculty.push("");
}

function removeFaculty(index) {
  course.value.eligible_faculty.splice(index, 1);
}

async function submitCourse() {
  course.value.eligible_faculty = course.value.eligible_faculty.filter(
    (f) => f.trim() !== ""
  );
  course.value.credits = Number(course.value.credits);

  const payload = {
    admin_id: store.userid,
    course_id: course.value.course_id,
    name: course.value.name,
    eligible_faculty: course.value.eligible_faculty,
    credits: course.value.credits,
    prerequisites: course.value.prerequisites,
  };

  console.log("Sending:", payload);

  try {
    await axios.post("http://127.0.0.1:8000/admin/courses/add", payload);
    alert("✅ Course Added Successfully!");
  } catch (err) {
    console.error("Backend error:", err.response?.data || err);
    alert("❌ Backend rejected request. Check console for details.");
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

/* Card / form container */
.form-card {
  background-color: #fff;
  padding: 30px 25px;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
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

/* Input focus effect */
.form-card input:focus {
  border-color: #3498db;
}

/* Faculty row styling */
.faculty-row {
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

/* Add Faculty button */
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
