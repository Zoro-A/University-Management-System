<template>
  <header class="header">
    <div class="logo"></div>
    <div class="avatar-container" @click="toggleDropdown">
      <img src="https://i.pravatar.cc/40" alt="User Avatar" class="avatar" />
      <div v-if="dropdownOpen" class="dropdown">
        <ul>
          <li @click="goToProfile">Profile</li>
          <li @click="logout">Logout</li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { userRolestore } from "../store/rolestore";

const dropdownOpen = ref(false);
const router = useRouter();
const store = userRolestore();

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value;
}

function goToProfile() {
  dropdownOpen.value = false;
  router.push("/update");
}

function logout() {
  dropdownOpen.value = false;

  // Remove user data from localStorage
  localStorage.removeItem("userData");
  
  // Reset the store
  store.resetAll();

  // Navigate to role selection page
  router.replace("/");
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: linear-gradient(to left, #a277e6, #6326c5);
  color: white;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
}

.avatar-container {
  position: relative;
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.dropdown {
  position: absolute;
  right: 0;
  top: 50px;
  background-color: white;
  color: black;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  width: 120px;
}

.dropdown ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown li {
  padding: 10px;
  cursor: pointer;
}

.dropdown li:hover {
  background-color: #f0f0f0;
}
</style>
