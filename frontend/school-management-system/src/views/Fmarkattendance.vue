<template>
  <div class="page-container">
    <header class="page-header">
      <h2>Mark Attendance</h2>
      <p class="subtitle">Manage daily attendance for your courses</p>
    </header>

    <div v-if="courses.length === 0" class="loading-state">
      <div class="spinner"></div>
      <p>Loading your courses...</p>
    </div>

    <div v-for="(course, idx) in courses" :key="course" class="course-card">
      <div class="course-header">
        <div class="course-title-group">
          <span class="badge">Course</span>
          <h3>{{ course }}</h3>
        </div>
        <div class="date-control">
          <label>Select Date:</label>
          <input
            type="date"
            v-model="selectedDate[course]"
            class="form-input"
          />
        </div>
      </div>

      <div class="table-responsive">
        <table class="attendance-table">
          <thead>
            <tr>
              <th width="15%">ID</th>
              <th width="30%">Student Name</th>
              <th width="30%">Status</th>
              <th width="25%" class="text-right">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="student in students[idx]" :key="student.user_id">
              <td class="id-cell">#{{ student.user_id }}</td>
              <td class="name-cell">{{ student.name }}</td>
              <td>
                <div class="select-wrapper">
                  <select
                    v-model="attendance[course][student.user_id]"
                    :class="
                      attendance[course][student.user_id] === 'Absent'
                        ? 'status-absent'
                        : 'status-present'
                    "
                  >
                    <option value="Present">Present</option>
                    <option value="Absent">Absent</option>
                  </select>
                </div>
              </td>
              <td class="text-right">
                <button
                  class="btn-primary"
                  @click="markAttendance(course, student.user_id, student.name)"
                >
                  Save
                </button>
              </td>
            </tr>
          </tbody>

          <tfoot
            v-if="attendanceLogs[course] && attendanceLogs[course].length > 0"
          >
            <tr class="log-header-row">
              <td colspan="4">Recent Activity (Today)</td>
            </tr>
            <tr
              v-for="(log, i) in attendanceLogs[course]"
              :key="log.date + log.student_id + i"
              class="log-row"
            >
              <td>#{{ log.student_id }}</td>
              <td>{{ log.name }}</td>
              <td>
                <span :class="['status-pill', log.status.toLowerCase()]">{{
                  log.status
                }}</span>
              </td>
              <td class="text-right date-cell">{{ log.date }}</td>
            </tr>
          </tfoot>
        </table>

        <div
          v-if="!attendanceLogs[course] || attendanceLogs[course].length === 0"
          class="empty-logs"
        >
          No attendance marked for this session yet.
        </div>
      </div>
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
const students = ref([]); // array of arrays; students per course index

const attendance = ref({}); // attendance[course][studentId] => 'Present'|'Absent'
const attendanceLogs = ref({}); // attendanceLogs[course] => array of logs
const selectedDate = ref({}); // selectedDate[course] => 'YYYY-MM-DD'

async function fetchCourses() {
  const userData = JSON.parse(localStorage.getItem("userData"));
  if (!userData || !userData.id) return;
  const userId = userData.id;
  try {
    const resp = await axios.get(
      `${apiConfig.baseURL}/faculty/${userId}/courses`
    );
    courses.value = resp.data;
  } catch (err) {
    console.error("Failed to load courses", err);
  }
}

async function getstudents() {
  const userData = JSON.parse(localStorage.getItem("userData"));
  if (!userData || !userData.id) return;
  const userId = userData.id;
  try {
    students.value = [];
    // initialize maps
    for (const course of courses.value) {
      const resp = await axios.get(
        `${apiConfig.baseURL}/faculty/${userId}/students/${course}`
      );
      students.value.push(resp.data);

      attendance.value[course] = {};
      attendanceLogs.value[course] = [];
      selectedDate.value[course] = formatDateISO();

      // default attendance selection to Present for each student
      for (const s of resp.data) {
        attendance.value[course][s.user_id] = "Present";
      }
    }
  } catch (err) {
    console.error("Failed loading students", err);
  }
}

function formatDateISO(d = new Date()) {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

async function markAttendance(course_id, student_id, student_name) {
  const status = attendance.value[course_id][student_id] || "Present";
  const date = selectedDate.value[course_id] || formatDateISO();

  if (Array.isArray(attendanceLogs.value[course_id])) {
    const exists = attendanceLogs.value[course_id].some(
      (l) => l.student_id === student_id && l.date === date
    );
    if (exists) {
      alert("Attendance already marked for this student on the selected date.");
      return;
    }
  }
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    console.error("User not logged in");
    return;
  }

  const userId = userData.id;

  const payload = {
    faculty_id: userId,
    student_id: student_id,
    course_id: course_id,
    date: date,
    status: status,
  };

  try {
    const resp = await axios.post(
      apiConfig.url("faculty/mark-attendance"),
      payload
    );
    if (resp.status === 200 || resp.status === 201) {
      // append to logs for this course — new entries appear as last rows (tfoot)
      attendanceLogs.value[course_id].push({
        student_id: student_id,
        name: student_name,
        status: status,
        date: payload.date,
      });
    }
  } catch (err) {
    console.error("Failed to mark attendance", err);
    alert("Failed to mark attendance");
  }
}

onMounted(async () => {
  await fetchCourses();
  await getstudents();
});
</script>
<style scoped>
/* --- Layout & Typography --- */
.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    sans-serif;
  color: #1f2937;
  background-color: #f9fafb;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.subtitle {
  color: #6b7280;
  margin-top: 8px;
}

/* --- Course Card --- */
.course-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  margin-bottom: 40px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.course-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  flex-wrap: wrap;
  gap: 15px;
}

.course-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.course-title-group h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
}

.badge {
  background-color: #e0e7ff;
  color: #4338ca;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* --- Controls --- */
.date-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-control label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #374151;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* --- Table Styles --- */
.table-responsive {
  overflow-x: auto;
}

.attendance-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.attendance-table th {
  background-color: #f9fafb;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.attendance-table td {
  padding: 16px 24px;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
  font-size: 0.95rem;
}

.attendance-table tbody tr:hover {
  background-color: #f9fafb;
}

/* --- Columns --- */
.id-cell {
  color: #9ca3af;
  font-family: monospace;
}

.name-cell {
  font-weight: 500;
  color: #111827;
}

.text-right {
  text-align: right;
}

/* --- Inputs & Buttons inside Table --- */
select {
  padding: 8px 32px 8px 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background-color: white;
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  width: 100%;
  max-width: 140px;
}

select:focus {
  outline: none;
  border-color: #6366f1;
}

/* Color coding for select */
.status-present {
  color: #059669; /* Green text */
  border-color: #a7f3d0;
  background-color: #ecfdf5;
}

.status-absent {
  color: #dc2626; /* Red text */
  border-color: #fecaca;
  background-color: #fef2f2;
}

.btn-primary {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
}

.btn-primary:active {
  transform: translateY(0);
}

/* --- Footer / Logs --- */
tfoot {
  background-color: #f8fafc;
  border-top: 2px solid #e2e8f0;
}

.log-header-row td {
  padding: 10px 24px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #64748b;
  letter-spacing: 0.05em;
  background: #f1f5f9;
}

.log-row td {
  padding: 12px 24px;
  font-size: 0.85rem;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
}

.status-pill {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-pill.present {
  background-color: #d1fae5;
  color: #065f46;
}

.status-pill.absent {
  background-color: #fee2e2;
  color: #991b1b;
}

.date-cell {
  font-variant-numeric: tabular-nums;
}

.empty-logs {
  padding: 15px;
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
  font-style: italic;
  background-color: #f9fafb;
}

/* --- Loading --- */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #6b7280;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4f46e5;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .course-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .date-control {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
