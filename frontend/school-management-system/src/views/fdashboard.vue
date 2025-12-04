<template>
  <div class="faculty-dashboard">

    <h2 class="title">Faculty Dashboard</h2>
    <p class="subtitle">
      Welcome to the faculty dashboard. Use the options below to manage your courses.
    </p>

    <div class="card-container">
      <router-link to="/Fassigngrades" class="dashboard-card">
        <h3>Assign Grades</h3>
        <p>Grade students for your assigned courses.</p>
      </router-link>

      <router-link to="/Fviewtimetable" class="dashboard-card">
        <h3>View Timetable</h3>
        <p>Check your scheduled classes.</p>
      </router-link>

      <router-link to="/Fmarkattendance" class="dashboard-card">
        <h3>Mark Attendance</h3>
        <p>Record daily attendance for students in your courses.</p>
      </router-link>

      <router-link to="/FsendNotifications" class="dashboard-card">
        <h3>Send Notifications</h3>
        <p>Communicate updates to students.</p>
      </router-link>
    </div>

  </div>
</template>

<script setup>
import router from '@/router';
</script>

<style scoped>
.faculty-dashboard {
  padding: 24px;
  text-align: center;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 15px;
  color: #555;
  margin-bottom: 24px;
}

/* Card Grid */
.card-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

/* Individual Card */
.dashboard-card {
  width: 240px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  text-decoration: none;
  color: #222;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transition: 0.25s;
  text-align: left;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}

/* Card Title */
.dashboard-card h3 {
  margin-bottom: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #0066cc;
}

/* Card Description */
.dashboard-card p {
  font-size: 14px;
  color: #555;
}
</style>
