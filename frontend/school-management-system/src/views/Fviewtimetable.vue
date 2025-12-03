<template>
  <div class="page">
    <h2>Faculty Timetable</h2>

    <div v-if="loading">Loading timetable...</div>
    <div v-else-if="!timetable.length">No timetable available.</div>

    <table v-else>
      <thead>
        <tr>
          <th>Course ID</th>
          <th>Course Name</th>
          <th>Day</th>
          <th>Slot</th>
          <th>Room</th>
          <th>Faculty</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in timetable" :key="idx">
          <td>{{ row.course_id }}</td>
          <td>{{ row.course_name || '-' }}</td>
          <td>{{ row.day }}</td>
          <td>{{ row.slot }}</td>
          <td>{{ row.room }}</td>
          <td>{{ row.faculty_name || row.faculty_id || '-' }}</td>
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
  const fid = store.userid
  if (!fid) {
    console.warn('Faculty id missing in store')
    timetable.value = []
    return
  }

  loading.value = true
  try {
    const url = `http://127.0.0.1:8000/faculty/${encodeURIComponent(fid)}/timetable`
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
/* Page background */
.page {
  min-height: 100vh;
  padding: 25px;
  background: linear-gradient(to right, #eef2f3, #ffffff);
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
}

/* Page Heading */
h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 26px;
  font-weight: bold;
}

/* Status Messages */
.page div {
  text-align: center;
  font-size: 15px;
  color: #7f8c8d;
  margin-top: 20px;
}

/* Table container */
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 15px;
  box-shadow: 0 8px 14px rgba(0, 0, 0, 0.08);
}

/* Table Header */
thead {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

th {
  padding: 12px;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.7px;
}

/* Table Body Cells */
td {
  padding: 10px;
  font-size: 14px;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
}

/* Zebra Stripes */
tbody tr:nth-child(odd) {
  background: #f8faff;
}
tbody tr:nth-child(even) {
  background: #ffffff;
}

/* Hover Effect */
tbody tr:hover {
  background: #ecf3ff;
  transition: 0.25s;
  cursor: pointer;
}

/* Column Alignment */
td:nth-child(2) { font-weight: 500; }

/* Room Badge Style */
td:nth-child(5) {
  background: #f4f6f8;
  font-weight: bold;
  text-align: center;
}

/* Slot column */
td:nth-child(4) {
  color: #5b86e5;
  font-weight: 500;
}

/* Day column */
td:nth-child(3) {
  color: #764ba2;
  font-weight: 600;
}

/* Faculty column */
td:nth-child(6) {
  color: #34495e;
  font-weight: 500;
}

/* Empty state */
.page div {
  padding: 10px;
}

</style>
