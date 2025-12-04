<template>
  <div class="transcript-page">
    <h2>Transcript</h2>

    <div v-if="loading">Loading transcript...</div>
    <div v-else-if="!hasEntries">No transcript available.</div>

    <div v-else>
      <div
        v-for="(courses, year) in transcript"
        :key="year"
        class="year-section"
      >
        <h3>{{ year }}</h3>

        <table class="transcript-table">
          <thead>
            <tr>
              <th>Course</th>
              <th>Grade</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="c in courses" :key="c.course">
              <td>{{ c.course }}</td>
              <td>{{ c.grade }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { userRolestore } from "../store/rolestore";

const transcript = ref({});
const loading = ref(false);
const store = userRolestore();

const hasEntries = computed(() => {
  return Object.keys(transcript.value || {}).length > 0;
});

async function fetchTranscript() {
  const sid = store.userid;

  if (!sid) {
    transcript.value = {
      2022: [
        { course: "CS100", grade: "A" },
        { course: "CS101", grade: "B+" },
      ],
      2023: [{ course: "CS201", grade: "A-" }],
      Unknown: [{ course: "CSE101", grade: "D" }],
    };
    return;
  }

  loading.value = true;

  try {
    const url = `http://127.0.0.1:8000/student/${encodeURIComponent(
      sid
    )}/transcript`;
    const res = await axios.get(url);

    transcript.value = res?.data ?? {};
  } catch (err) {
    console.error("Failed to fetch transcript", err.response?.data || err);
    transcript.value = {};
  } finally {
    loading.value = false;
  }
}

onMounted(fetchTranscript);
</script>

<style scoped>
.transcript-page {
  padding: 24px;
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
  background: linear-gradient(135deg, #eef2ff, #f8f9ff);
  min-height: 100vh;
}

h2 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 25px;
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.year-section {
  margin-bottom: 32px;
  padding: 20px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  border-left: 6px solid #4a6cf7;
  transition: transform 0.2s ease;
}

.year-section:hover {
  transform: translateY(-3px);
}

.year-section h3 {
  margin-bottom: 16px;
  color: #4a6cf7;
  font-size: 22px;
  font-weight: 600;
}

.transcript-table {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
  border-radius: 10px;
}

.transcript-table thead {
  background: linear-gradient(90deg, #4a6cf7, #7f57ff);
  color: white;
}

.transcript-table th,
.transcript-table td {
  padding: 12px 10px;
  border-bottom: 1px solid #e6e6e6;
  font-size: 15px;
}

.transcript-table tr:nth-child(even) {
  background: #f8f9ff;
}

.transcript-table tr:hover {
  background: #eef2ff;
  transition: 0.2s ease;
}
</style>
