<template>
  <div style="padding: 20px">
    <h2>Assign Grades</h2>

    <div v-if="courses.length === 0">
      <p>Loading courses...</p>
    </div>

    <!-- COURSE TABLES -->
    <div
      v-for="(course, index) in courses"
      :key="course"
      style="margin-bottom: 40px"
    >
      <h3>Course: {{ course }}</h3>

      <table border="1" cellpadding="8" cellspacing="0" width="100%">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Name</th>
            <th>Marks</th>
            <th>Grade</th>
            <th>Submit</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="student in students[index]" :key="student.user_id">
            <td>{{ student.user_id }}</td>
            <td>{{ student.name }}</td>

            <!-- MARKS -->
            <td>
              <input
                type="number"
                min="0"
                max="100"
                v-model="marks[course][student.user_id]"
                @input="calculateGrade(course, student.user_id)"
              />
            </td>

            <!-- GRADE -->
            <td>
              {{ grades[course][student.user_id] }}
            </td>

            <!-- SUBMIT -->
            <td>
              <button @click="submitGrade(course, student.user_id)">
                Save
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { userRolestore } from "../store/rolestore";
import apiConfig from "../config/api";

const store = userRolestore();

const courses = ref([]);
const students = ref([]);

const marks = ref({});
const grades = ref({});

async function fetchCourses() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;

  try {
    const response = await axios.get(
      `${apiConfig.baseURL}/faculty/${userId}/courses`
    );
    courses.value = response.data;
  } catch (err) {
    console.error("Failed to load courses", err);
  }
}

async function getstudents() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;
  try {
    students.value = [];

    for (const course of courses.value) {
      const response = await axios.get(
        `${apiConfig.baseURL}/faculty/${userId}/students/${course}`
      );
      console.log(response?.data, "check response data");
      students.value.push(response.data);

      // Initialize per course grade maps
      marks.value[course] = {};
      grades.value[course] = {};
    }
  } catch (err) {
    console.error("Failed loading students", err);
  }
}

/* -----------------------------------
   AUTO GRADE CALCULATION
----------------------------------- */
function calculateGrade(course_id, student_id) {
  const score = marks.value[course_id][student_id];

  if (score === undefined || score === "") {
    grades.value[course_id][student_id] = "";
    return;
  }

  if (score >= 85) grades.value[course_id][student_id] = "A";
  else if (score >= 70) grades.value[course_id][student_id] = "B";
  else if (score >= 60) grades.value[course_id][student_id] = "C";
  else if (score >= 50) grades.value[course_id][student_id] = "D";
  else grades.value[course_id][student_id] = "F";
}

/* -----------------------------------
   POST GRADE TO BACKEND
----------------------------------- */
async function submitGrade(course_id, student_id) {
  const grade = grades.value[course_id][student_id];

  const payload = {
    faculty_id: store.userid,
    student_id: student_id,
    course_id: course_id,
    grade: grade,
  };

  try {
    const response = await axios.post(
      apiConfig.url("faculty/assign-grade"),
      payload
    );

    if (response.status === 200) {
      alert(`Grade saved for ${student_id} in ${course_id}`);
    }
  } catch (err) {
    console.error(err);
    alert("Failed to assign grade");
  }
}

/* -----------------------------------
   LOAD DATA
----------------------------------- */
onMounted(async () => {
  await fetchCourses();
  await getstudents();
});
</script>

<style scoped>
/* Page layout */
/* Page background */
div {
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
  background: linear-gradient(to right, #eef2f3, #ffffff);
  min-height: 100vh;
}

/* Main heading */
h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 26px;
}

/* Course title */
h3 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 12px 18px;
  border-radius: 8px;
  font-size: 18px;
  letter-spacing: 0.5px;
}

/* Table container */
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

/* Header */
thead {
  background: #2c3e50;
  color: #ecf0f1;
}

th {
  padding: 12px;
  text-transform: uppercase;
  font-size: 13px;
  letter-spacing: 0.8px;
}

/* Cells */
td {
  padding: 10px;
  text-align: center;
  font-size: 14px;
  border-bottom: 1px solid #eee;
}

/* Zebra stripes */
tbody tr:nth-child(odd) {
  background-color: #f8faff;
}

tbody tr:nth-child(even) {
  background-color: #ffffff;
}

/* Hover highlight */
tbody tr:hover {
  background: #eaf2ff;
  transition: 0.25s;
}

/* Inputs */
input[type="number"] {
  width: 70px;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #bbb;
  outline: none;
  text-align: center;
  font-size: 14px;
}

input:focus {
  border-color: #667eea;
  box-shadow: 0 0 6px rgba(102, 126, 234, 0.4);
}

/* Button */
button {
  background: linear-gradient(to right, #36d1dc, #5b86e5);
  border: none;
  border-radius: 8px;
  color: white;
  padding: 7px 14px;
  cursor: pointer;
  font-size: 13px;
  transition: 0.3s;
  font-weight: bold;
}

button:hover {
  transform: scale(1.05);
  background: linear-gradient(to right, #5b86e5, #36d1dc);
}

/* Grade Coloring */
td {
  font-weight: 500;
}

/* Use Vue dynamic class to color grades */
td::after {
  font-weight: bold;
  letter-spacing: 1px;
}

/* Grade colors via text detection */
/* Since Vue renders text, we style via attribute selector hack */

/* A Grade */
td:has(> span.grade-A),
td:contains("A") {
  color: #2ecc71;
}

/* B Grade */
td:contains("B") {
  color: #27ae60;
}

/* C Grade */
td:contains("C") {
  color: #f39c12;
}

/* D Grade */
td:contains("D") {
  color: #e67e22;
}

/* F Grade */
td:contains("F") {
  color: #e74c3c;
  font-weight: bold;
}

/* Default empty grade */
td:empty {
  color: #aaa;
}

/* Loading text */
p {
  text-align: center;
  color: #7f8c8d;
  font-size: 15px;
}
</style>
