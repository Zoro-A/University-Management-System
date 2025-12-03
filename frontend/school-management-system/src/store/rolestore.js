import { defineStore } from 'pinia'
import { ref } from 'vue'

export const userRolestore = defineStore("userRolestore", () => {

  // --- STATE ---
  const role = ref("")
  const username = ref("")
  const userid = ref("")

  // --- ACTIONS ---
  function setRole(newRole) {
    role.value = newRole
  }

  function setUser(id, name) {
    userid.value = id
    username.value = name
  }

  function resetAll() {
    role.value = ""
    username.value = ""
    userid.value = ""
  }

  // --- RETURN EVERYTHING ---
  return {
    role,
    username,
    userid,
    setRole,
    setUser,
    resetAll
  }
})
