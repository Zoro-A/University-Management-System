<template>
  <div style="padding: 20px">
    <h2>Send Notifications (Faculty)</h2>

    <div v-if="courses.length === 0">
      <p>Loading courses...</p>
    </div>

    <div style="margin-top: 12px">
      <label>Select Course:</label>
      <select v-model="selectedCourse">
        <option value="">-- Select course --</option>
        <option v-for="c in courses" :key="c" :value="c">{{ c }}</option>
      </select>
      <button
        @click="loadStudentsForCourse"
        :disabled="!selectedCourse"
        style="margin-left: 8px"
      >
        Load Students
      </button>
    </div>

    <div v-if="loadingStudents" style="margin-top: 10px">
      Loading students...
    </div>

    <div v-if="currentStudents.length" style="margin-top: 14px">
      <h3>Students for {{ selectedCourse }}</h3>

      <label
        ><input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
        Select All</label
      >

      <div
        style="
          max-height: 260px;
          overflow: auto;
          border: 1px solid #eee;
          padding: 8px;
          margin-top: 8px;
          background: #fafafa;
        "
      >
        <div
          v-for="s in currentStudents"
          :key="s.user_id"
          style="display: flex; align-items: center; gap: 12px; padding: 6px 0"
        >
          <input
            type="checkbox"
            :value="s.user_id"
            v-model="selectedRecipients"
          />
          <div>
            <div>
              <strong>{{ s.user_id }}</strong>
            </div>
            <div style="font-size: 13px; color: #555">
              {{ s.name }} — {{ s.email }}
            </div>
          </div>
        </div>
      </div>

      <div style="margin-top: 10px">
        <textarea
          v-model="message"
          rows="4"
          style="width: 100%"
          placeholder="Enter notification message"
        ></textarea>
      </div>

      <div style="margin-top: 8px; display: flex; gap: 8px">
        <button
          @click="sendToSelected"
          :disabled="!message || selectedRecipients.length === 0"
        >
          Send to Selected
        </button>
        <button @click="sendToAll" :disabled="!message">Send to All</button>
      </div>

      <div v-if="result" style="margin-top: 8px">{{ result }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import axios from "axios";
import { userRolestore } from "../store/rolestore";

const store = userRolestore();

const courses = ref([]);
const studentsByCourse = reactive({});
const selectedCourse = ref("");
const loadingStudents = ref(false);

const selectAll = ref(false);
const selectedRecipients = ref([]);
const message = ref("");
const result = ref("");

const currentStudents = computed(() => {
  return selectedCourse.value &&
    Array.isArray(studentsByCourse[selectedCourse.value])
    ? studentsByCourse[selectedCourse.value]
    : [];
});

async function fetchCourses() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;
  try {
    const res = await axios.get(
      `http://127.0.0.1:8001/faculty/${encodeURIComponent(userId)}/courses`
    );
    courses.value = Array.isArray(res.data) ? res.data : [];
  } catch (err) {
    console.error("Failed to load courses", err);
    courses.value = [];
  }
}

/* Extracted getstudents logic: fetch students per course and store in studentsByCourse */
async function loadAllStudents() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;
  try {
    for (const course of courses.value) {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8001/faculty/${encodeURIComponent(
            userId
          )}/students/${encodeURIComponent(course)}`
        );
        studentsByCourse[course] = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.error("Failed loading students for", course, err);
        studentsByCourse[course] = [];
      }
    }
  } catch (err) {
    console.error("Error in loadAllStudents", err);
  }
}

async function loadStudentsForCourse() {
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!userData || !userData.id) {
    return;
  }

  const userId = userData.id;
  if (!selectedCourse.value) return;
  loadingStudents.value = true;
  try {
    // if already loaded, just use from map
    if (!studentsByCourse[selectedCourse.value]) {
      const res = await axios.get(
        `http://127.0.0.1:8001/faculty/${encodeURIComponent(
          userId
        )}/students/${encodeURIComponent(selectedCourse.value)}`
      );
      studentsByCourse[selectedCourse.value] = Array.isArray(res.data)
        ? res.data
        : [];
    }
    // reset selections
    selectedRecipients.value = [];
    selectAll.value = false;
    result.value = "";
  } catch (err) {
    console.error("Failed loading students for course", err);
    studentsByCourse[selectedCourse.value] = [];
  } finally {
    loadingStudents.value = false;
  }
}

function toggleSelectAll() {
  if (selectAll.value)
    selectedRecipients.value = currentStudents.value.map((s) => s.user_id);
  else selectedRecipients.value = [];
}

async function sendToSelected() {
  if (!message.value || selectedRecipients.value.length === 0) return;
  result.value = "Sending...";
  try {
    const fid = store.userid;
    const tasks = selectedRecipients.value.map((id) => {
      const payload = { faculty_id: fid, target: id, message: message.value };
      return axios.post("http://127.0.0.1:8001/faculty/notify", payload);
    });
    const settled = await Promise.allSettled(tasks);
    const failed = settled.filter((s) => s.status === "rejected");
    result.value =
      failed.length === 0
        ? "Notifications sent successfully."
        : `${settled.length - failed.length} sent, ${failed.length} failed.`;
  } catch (err) {
    console.error("Send selected error", err);
    result.value = "Failed to send notifications.";
  }
}

async function sendToAll() {
  if (!message.value) return;
  result.value = "Sending to all...";
  try {
    const fid = store.userid;
    const payload = { faculty_id: fid, target: "all", message: message.value };
    await axios.post("http://127.0.0.1:8001/faculty/notify", payload);
    result.value = "Notification sent to all.";
  } catch (err) {
    console.error("Send to all error", err);
    result.value = "Failed to send to all.";
  }
}

onMounted(async () => {
  await fetchCourses();
  // optionally pre-load students for faster selection
  // await loadAllStudents()
});
</script>

<style scoped>
/* PAGE */
div {
  font-family: "Segoe UI", Tahoma, Arial, sans-serif;
}

h2 {
  font-size: 22px;
  margin-bottom: 12px;
  color: #2c3e50;
}

h3 {
  margin-top: 12px;
  margin-bottom: 8px;
  color: #34495e;
}

/* COURSE SELECT AREA */
label {
  font-weight: 500;
}

select {
  padding: 6px 10px;
  margin-left: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  outline: none;
  background-color: white;
}

select:focus {
  border-color: #3498db;
}

/* STUDENT LIST BOX */
div[style*="max-height"] {
  border-radius: 6px;
  background-color: #f9f9f9;
}

/* STUDENT ROW */
div[style*="display:flex"] {
  padding: 6px 8px;
  border-bottom: 1px solid #eee;
}

div[style*="display:flex"]:hover {
  background-color: #eef6ff;
}

/* CHECKBOX */
input[type="checkbox"] {
  transform: scale(1.1);
  cursor: pointer;
}

/* MESSAGE BOX */
textarea {
  border-radius: 6px;
  padding: 8px;
  border: 1px solid #ccc;
  resize: none;
}

textarea:focus {
  outline: none;
  border-color: #3498db;
}

/* BUTTONS */
button {
  border: none;
  border-radius: 5px;
  padding: 6px 14px;
  background-color: #3498db;
  color: white;
  font-weight: 500;
  transition: 0.2s ease;
}

button:hover {
  background-color: #2980b9;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* RESULT MESSAGE */
div[v-if="result"] {
  margin-top: 10px;
  font-weight: 500;
}

/* LOADING TEXT */
p {
  color: #888;
}
</style>
