<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Add Student (Admin)</h2>

      <input v-model="student.user_id" placeholder="Student User ID" />
      <input v-model="student.name" placeholder="Full Name" />
      <input v-model="student.email" placeholder="Email" />
      <input type="password" v-model="student.password" placeholder="Password" />

      <button class="submit-btn" @click="submitStudent">Submit Student</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { userRolestore } from '../store/rolestore'

const store = userRolestore()

const student = ref({
  user_id: '',
  name: '',
  email: '',
  password: ''
})

async function submitStudent() {
  const payload = {
    admin_id: store.userid,
    user_id: student.value.user_id,
    name: student.value.name,
    email: student.value.email,
    password: student.value.password
  }

  console.log('Sending student payload:', payload)

  try {
    await axios.post('http://127.0.0.1:8000/admin/student/add', payload)
    alert('✅ Student added successfully')
    student.value.user_id = ''
    student.value.name = ''
    student.value.email = ''
    student.value.password = ''
  } catch (err) {
    console.error('Add student error:', err.response?.data || err)
    alert('❌ Failed to add student — check console for details')
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
