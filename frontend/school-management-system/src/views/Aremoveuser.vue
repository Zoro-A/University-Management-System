<template>
  <div class="page-container">
    <div class="form-card">
      <h2>Remove User (Admin)</h2>

      <input v-model="user.user_id" placeholder="User ID to remove" />

      <button class="submit-btn" @click="submitRemove">Submit</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { userRolestore } from "../store/rolestore";

const store = userRolestore();

const user = ref({
  user_id: "",
});

async function submitRemove() {
  const payload = {
    admin_id: store.userid,
    user_id: user.value.user_id,
  };

  console.log("Sending remove-user payload:", payload);

  try {
    await axios.post("http://127.0.0.1:8000/admin/faculty/add", payload);
    alert("✅ Request sent successfully");
    user.value.user_id = "";
  } catch (err) {
    console.error("Remove user error:", err.response?.data || err);
    alert("❌ Failed to send request — check console for details");
  }
}
</script>

<style scoped>
/* Center the page */
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
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
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

/* Input */
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
  border-color: #e74c3c; /* red for remove */
}

/* Submit button */
.submit-btn {
  padding: 12px;
  background-color: #e74c3c; /* red for remove */
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
  background-color: #c0392b;
}
</style>
