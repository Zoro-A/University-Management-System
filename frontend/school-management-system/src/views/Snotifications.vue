<template>
  <div class="notifications-page">
    <h2>Notifications</h2>

    <div v-if="loading" class="loading-message">Loading notifications...</div>
    <div v-else-if="notifications.length === 0" class="empty-message">
      No notifications available.
    </div>

    <div v-else class="notifications-container">
      <div
        v-for="(notification, index) in notifications"
        :key="index"
        class="notification-card"
      >
        <div class="notification-header">
          <div class="sender-info">
            <span class="sender-badge">{{ getSenderName(notification.from) }}</span>
            <span v-if="notification.to === 'all'" class="broadcast-badge">Broadcast</span>
          </div>
          <span class="date-badge">{{ formatDate(notification.date) }}</span>
        </div>
        <div class="notification-message">
          {{ notification.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import apiConfig from "../config/api";

const notifications = ref([]);
const loading = ref(false);

// Get student ID from localStorage
const getStudentId = () => {
  const userData = JSON.parse(localStorage.getItem("userData"));
  return userData?.id || null;
};

// Get sender name (could be faculty ID or "Admin")
const getSenderName = (senderId) => {
  if (!senderId) return "System";
  if (senderId.toLowerCase() === "admin") return "Admin";
  // If it's a faculty ID, you might want to fetch the name
  // For now, just return the ID
  return senderId;
};

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return "No date";
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return dateString;
  }
};

async function fetchNotifications() {
  const studentId = getStudentId();
  if (!studentId) {
    console.error("Student ID not found");
    return;
  }

  loading.value = true;
  try {
    const response = await axios.get(
      `${apiConfig.baseURL}/student/${studentId}/notifications`
    );
    notifications.value = Array.isArray(response.data) ? response.data : [];
    // Sort by date (newest first)
    notifications.value.sort((a, b) => {
      const dateA = new Date(a.date || 0);
      const dateB = new Date(b.date || 0);
      return dateB - dateA;
    });
  } catch (err) {
    console.error("Failed to fetch notifications:", err);
    notifications.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchNotifications();
});
</script>

<style scoped>
.notifications-page {
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

.loading-message,
.empty-message {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-size: 16px;
}

.empty-message {
  color: #999;
  font-style: italic;
}

.notifications-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-left: 4px solid #4a6cf7;
}

.notification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 8px;
}

.sender-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.sender-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
  background: linear-gradient(135deg, #4a6cf7, #7f57ff);
  color: white;
}

.broadcast-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  background-color: #f4b400;
  color: white;
}

.date-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background-color: #e8eaf6;
  color: #5c6bc0;
}

.notification-message {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  padding: 8px 0;
}

/* Responsive */
@media (max-width: 600px) {
  .notifications-page {
    padding: 16px;
  }

  .notification-card {
    padding: 16px;
  }

  .notification-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>


