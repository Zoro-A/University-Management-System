<template>
  <div class="role-wrapper">
    <div class="role-content">
      <p class="role-title">Select Your Role</p>

      <div class="login-container">
        <div class="card admin" @click="selectRole('admin')">
          <div class="icon">
            <img src="../assets/images/admin.svg" width="100" height="100" />
          </div>
          <h3>Admin</h3>
          <p>Manage users, system settings and full control.</p>
          <button>Continue as Admin</button>
        </div>

        <div class="card student" @click="selectRole('student')">
          <div class="icon">
            <img src="../assets/images/student.svg" width="100" height="100" />
          </div>
          <h3>Student</h3>
          <p>Access courses, results, attendance and profile.</p>
          <button>Continue as Student</button>
        </div>

        <div class="card faculty" @click="selectRole('faculty')">
          <div class="icon">
            <img src="../assets/images/faculty.svg" width="100" height="100" />
          </div>
          <h3>Faculty</h3>
          <p>Manage classes, assignments and students.</p>
          <button>Continue as Faculty</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { userRolestore } from "../store/rolestore";
import { onMounted } from "vue";

const router = useRouter();
const userStore = userRolestore();

onMounted(() => {
  userStore.resetAll();
});

function selectRole(role) {
  userStore.setRole(role);
  router.push("/login");
}
</script>

<style scoped>
.role-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center; /* ✅ Vertical center */
}

.role-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px; /* ✅ Space between title & cards */
}

.role-title {
  font-weight: 700;
  font-size: 30px;
  text-align: center;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  flex-wrap: wrap;
}

.role-wrapper {
  display: flex;
  justify-content: center;
  height: 100vh;
}
.select-role {
  font-weight: 700;
  font-size: 20px;
  display: flex;
  justify-content: center;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  padding: 20px;
  flex-wrap: wrap;
}
.role-title {
  font-weight: 700;
  font-size: 30px;
  display: flex;
  justify-content: center;
}
.card {
  width: 280px;
  padding: 30px 20px;
  border-radius: 25px;
  background: white;
  text-align: center;
  cursor: pointer;
  transition: 0.3s ease;
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 8px solid transparent;
}

.card:hover {
  transform: translateY(-10px);
}

.icon {
  font-size: 50px;
  margin-bottom: 15px;
}

.card h3 {
  margin-bottom: 10px;
  font-size: 22px;
}

.card p {
  font-size: 14px;
  color: #555;
  margin-bottom: 20px;
}

.card button {
  padding: 10px 18px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  color: white;
  font-weight: bold;
}

/* ROLE COLORS */
.admin {
  border-color: #f4b400;
}
.admin button {
  background: #f4b400;
}

.student {
  border-color: #2ecc71;
}
.student button {
  background: #2ecc71;
}

.faculty {
  border-color: #1da1f2;
}
.faculty button {
  background: #1da1f2;
}

/* ✅ RESPONSIVE */
@media (max-width: 900px) {
  .login-container {
    flex-direction: column;
  }

  .card {
    width: 90%;
  }
}
</style>
