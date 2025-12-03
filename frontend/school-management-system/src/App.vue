<script setup>
import Header from "./components/Header.vue";
import Sidebar from "./components/Sidebar.vue";
import { useRoute } from "vue-router";

const route = useRoute();

// Paths where you don't want the header/sidebar
const noLayoutPaths = ["/", "/login"];
</script>

<template>
  <div class="app">
    <Header v-if="!noLayoutPaths.includes(route.path)" />
    <div class="main-layout">
      <Sidebar v-if="!noLayoutPaths.includes(route.path)" />
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style>
.app {
  display: flex;
  flex-direction: column;
  min-height: 99vh;
}

.main-layout {
  display: flex;
  flex: 1;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #ecf0f1;
  height: fit-content;
}

/* Responsive layout */
@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }

  .content {
    margin-left: 0;
  }
}
</style>
