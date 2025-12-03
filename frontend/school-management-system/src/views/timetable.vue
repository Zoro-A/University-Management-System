<template>
  <div class="page">
    <h1>Time Table</h1>

    <div v-if="loading">Loading timetable...</div>
    <div v-else-if="timetable.length === 0">No timetable available.</div>

    <table v-else class="tt-table">
      <thead>
        <tr>
          <th>Day</th>
          <th>Course ID</th>
          <th>Course Name</th>
          <th>Slot</th>
          <th>Room</th>
          <th>Faculty</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, idx) in timetable" :key="idx">
          <td>{{ item.day }}</td>
          <td>{{ item.course_id }}</td>
          <td>{{ item.course_name || '-' }}</td>
          <td>{{ item.slot || '-' }}</td>
          <td>{{ item.room || '-' }}</td>
          <td>{{ item.faculty_name || item.faculty_id || '-' }}</td>
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
const timetable = ref([])
const loading = ref(false)

async function fetchTimetable() {
  const sid = store.userid
  if (!sid) {
    // no student id in store; keep empty or you can set sample data
    timetable.value = []
    return
  }

  loading.value = true
  try {
    const url = `http://127.0.0.1:8000/student/${encodeURIComponent(sid)}/timetable`
    const res = await axios.get(url)
    timetable.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('Failed to fetch timetable', err.response?.data || err)
    timetable.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTimetable()
})
</script>

<style scoped>
.page {
  padding: 24px;
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
  background: linear-gradient(135deg, #eef2ff, #f8f9ff);
  min-height: 100vh;
}

/* Page Title */
h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  letter-spacing: 0.5px;
}

/* Table Container (Card Style) */
.tt-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

/* Table Header */
.tt-table thead {
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  color: white;
}

.tt-table th {
  padding: 14px;
  font-size: 15px;
  font-weight: 600;
  text-align: left;
}

/* Table Rows */
.tt-table td {
  padding: 12px 14px;
  font-size: 14px;
  border-bottom: 1px solid #f0f2ff;
  vertical-align: middle;
}

/* Slot and room badges */
.badge {
  display: inline-block;
  padding: 6px 8px;
  border-radius: 8px;
  font-size: 12px;
  color: #fff;
  background: #6c7bf3;
  margin-right: 6px;
}
.badge.room { background: #4a90e2 }
.badge.slot { background: #7f57ff }

/* Row striping */
.tt-table tbody tr:nth-child(even) {
  background: #fbfbff;
}

/* Row hover effect */
.tt-table tbody tr:hover {
  background: #f0f6ff;
  transform: translateY(-1px);
  box-shadow: inset 0 0 0 9999px rgba(240, 246, 255, 0.5);
  transition: all 0.18s ease;
}

/* Loading & Empty States */
.status-text {
  font-size: 16px;
  margin-top: 10px;
  color: #3c4b71;
  text-align: center;
  font-weight: 500;
  animation: fadeIn 0.28s ease;
}

/* Smooth Fade Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive adjustments */
@media (max-width: 800px) {
  .tt-table th, .tt-table td { padding: 10px; font-size: 13px }
  .tt-table thead { display: none }
  .tt-table, .tt-table tbody, .tt-table tr, .tt-table td { display: block; width: 100% }
  .tt-table tr { margin-bottom: 12px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04) }
  .tt-table td { text-align: left; padding-left: 14px; position: relative }
  .tt-table td::before { content: attr(data-label); font-weight: 600; display: block; color:#6b7280; margin-bottom:6px }
}
</style>