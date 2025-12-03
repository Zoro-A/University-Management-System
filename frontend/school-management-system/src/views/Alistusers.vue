<template>
  <div class="users-container">
    <h1>All Users</h1>

    <div v-for="(group, role) in users" :key="role" class="role-section">

      <h2>{{ role.toUpperCase() }}</h2>

      <table :class="['users-table', role]">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Password</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="user in group" :key="user.user_id">
            <td>{{ user.user_id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.password }}</td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { userRolestore } from '../store/rolestore'

const store = userRolestore()
const users = ref({})

async function fetchUsers() {
  if (!store.userid) {
    console.error("Admin ID missing")
    return
  }

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/admin/${store.userid}/users`
    )
    users.value = response.data
  } catch (error) {
    console.error("Failed to fetch users:", error.response?.data || error)
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.users-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.role-section {
  margin-bottom: 40px;
}

/* Shared table styling */
.users-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.users-table th, .users-table td {
  padding: 12px;
  text-align: left;
  border: none;
}

/* Header styles per role */
.users-table.admin thead {
  background-color: #3498db;
  color: white;
}

.users-table.student thead {
  background-color: #2ecc71;
  color: white;
}

.users-table.faculty thead {
  background-color: #f39c12;
  color: white;
}

/* Striped rows for contrast */
.users-table.admin tbody tr:nth-child(odd) {
  background-color: #eaf2fb;
}
.users-table.admin tbody tr:nth-child(even) {
  background-color: #ffffff;
}

.users-table.student tbody tr:nth-child(odd) {
  background-color: #e9f9f1;
}
.users-table.student tbody tr:nth-child(even) {
  background-color: #ffffff;
}

.users-table.faculty tbody tr:nth-child(odd) {
  background-color: #fff5e6;
}
.users-table.faculty tbody tr:nth-child(even) {
  background-color: #ffffff;
}

/* Hover effect for all tables */
.users-table tbody tr:hover {
  background-color: #dbe9f7;
}
</style>
