<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Generate Timetable (Admin)</h2>

      <div v-for="(r, idx) in rooms" :key="idx" class="room-row">
        <input v-model="rooms[idx]" placeholder="Room name" />
        <button class="remove-btn" @click="removeRoom(idx)">❌</button>
      </div>

      <button class="add-btn" @click="addRoom">+ Add Room</button>
      <button class="submit-btn" @click="submitGenerate">Generate Timetable</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { userRolestore } from '../store/rolestore'

const store = userRolestore()

const rooms = ref([''])

function addRoom() {
  rooms.value.push('')
}

function removeRoom(index) {
  rooms.value.splice(index, 1)
}

async function submitGenerate() {
  const cleaned = rooms.value.map(r => String(r).trim()).filter(r => r !== '')
  const payload = { admin_id: store.userid, rooms: cleaned }

  console.log('Sending generate timetable payload:', payload)

  try {
    await axios.post('http://127.0.0.1:8001/admin/timetable/generate', payload)
    alert('✅ Timetable generation request sent')
    rooms.value = ['']
  } catch (err) {
    console.error('Generate timetable error:', err.response?.data || err)
    alert('❌ Failed to send request — check console for details')
  }
}
</script>

<style scoped>
/* Center page */
.page-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 40px 20px;
  background: #f0f2f5;
  font-family: Arial, sans-serif;
}

/* Card container */
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

/* Room row */
.room-row {
  display: flex;
  gap: 10px;
  align-items: center;
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

/* Input focus */
.form-card input:focus {
  border-color: #3498db;
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

/* Add Room button */
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

/* Generate Timetable button */
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
