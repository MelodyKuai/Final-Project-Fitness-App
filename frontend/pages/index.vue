<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // Redirect to login page when accessing root
  router.push('/login')
})
</script>

<template>
  <div></div>
</template> 