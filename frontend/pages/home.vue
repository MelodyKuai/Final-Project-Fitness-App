<script setup>
import { ref, onMounted, computed } from 'vue'
import { recordService } from '../services/recordService'
import { exerciseService } from '../services/exerciseService'
import { userService } from '../services/userService'
import { useToast } from "vue-toastification/dist/index.mjs"
import { useRouter } from 'vue-router'

const router = useRouter()
const toast = useToast()
const workoutRecords = ref([])
const showNewWorkoutForm = ref(false)
const showActionMenu = ref(false)
const selectedRecord = ref(null)
const menuPosition = ref({ x: 0, y: 0 })
const loading = ref(false)

const exercises = ref([])
const loadingExercises = ref(false)

const newWorkout = ref({
  name: '',
  duration: '',
  imgUrl: '',
  date: new Date().toISOString().split('T')[0]
})

const showImagePreview = ref(false)
const previewImage = ref({
  url: '',
  name: ''
})

// Fetch exercises
const fetchExercises = async () => {
  try {
    loadingExercises.value = true
    const data = await exerciseService.getExercises(50)
    exercises.value = data
  } catch (err) {
    toast.error(err.message || 'Failed to fetch exercises')
  } finally {
    loadingExercises.value = false
  }
}

// Fetch all records
const fetchRecords = async () => {
  try {
    loading.value = true
    const records = await recordService.getAllRecords()
    workoutRecords.value = records
    console.log('records', workoutRecords.value);
    
  } catch (err) {
    toast.error(err.message || 'Failed to fetch records')
    workoutRecords.value = []
  } finally {
    loading.value = false
  }
}

const handleStartWorkout = () => {
  showNewWorkoutForm.value = true
}

const handleSubmitWorkout = async () => {
  try {
    loading.value = true
    await recordService.createRecord(newWorkout.value)
    await fetchRecords()
    showNewWorkoutForm.value = false
    toast.success('Workout added successfully')
    
    // Reset form
    newWorkout.value = {
      name: '',
      duration: '',
      imgUrl: '',
      date: new Date().toISOString().split('T')[0]
    }
  } catch (err) {
    toast.error(err.message || 'Failed to create workout')
  } finally {
    loading.value = false
  }
}

const handleRecordAction = (record, event) => {
  selectedRecord.value = record
  const rect = event.target.getBoundingClientRect()
  menuPosition.value = {
    x: rect.left,
    y: rect.bottom
  }
  showActionMenu.value = true
}

const handleEdit = async () => {
  try {
    loading.value = true
    await recordService.updateRecord(selectedRecord.value.id, selectedRecord.value)
    await fetchRecords()
    showActionMenu.value = false
    toast.success('Workout updated successfully')
  } catch (err) {
    toast.error(err.message || 'Failed to update workout')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (record) => {
  try {
    loading.value = true
    await recordService.deleteRecord(record.id)
    await fetchRecords()
    toast.success('Workout deleted successfully')
  } catch (err) {
    toast.error(err.message || 'Failed to delete workout')
  } finally {
    loading.value = false
  }
}

const handleSelectExercise = (exercise) => {
  newWorkout.value.name = exercise.name
  newWorkout.value.imgUrl = exercise.gifUrl
}

// Close menu when clicking outside
const closeMenu = () => {
  showActionMenu.value = false
}

const handleLogout = async () => {
  try {
    await userService.logout()
    toast.success('Logged out successfully')
    router.push('/login')
  } catch (err) {
    toast.error(err.message || 'Failed to logout')
  }
}

// Fetch data when component mounts
onMounted(() => {
  Promise.all([
    fetchRecords(),
    fetchExercises()
  ])
})

const groupedRecords = computed(() => {
  const groups = {}
  const sortedRecords = [...workoutRecords.value].sort((a, b) => 
    new Date(b.created_time) - new Date(a.created_time)
  )
  
  sortedRecords.forEach(record => {
    const date = new Date(record.created_time).toLocaleDateString()
    if (!groups[date]) {
      groups[date] = []
    }
    groups[date].push(record)
  })
  
  return groups
})

const getMaxDuration = (records) => {
  return Math.max(...records.map(record => Number(record.duration) || 0))
}

const getProgressWidth = (duration, maxDuration) => {
  return `${(duration / maxDuration * 50)}%`
}

// Helper function: Get image source from record
const getImageSrc = (record) => {
  if (!record.imgData) return record.imgUrl // Fallback to imgUrl if imgData not exists
  return record.imgData.startsWith('data:') ? record.imgData : `data:image/gif;base64,${record.imgData}`
}

// Handle image preview click
const handleImageClick = (record) => {
  previewImage.value = {
    url: getImageSrc(record),
    name: record.name
  }
  showImagePreview.value = true
}
</script>

<template>
  <div class="home-container">
    <div class="glass-card main-card">
      <div class="header-actions">
        <button class="btn-primary start-workout" @click="handleStartWorkout" :disabled="loading">
          <va-icon name="fitness_center" />
          Start Today's Workout
        </button>
        <va-menu>
          <template #anchor>
            <button class="avatar-button">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User Avatar" class="avatar-image">
            </button>
          </template>

          <va-menu-item @click="handleLogout" class="logout-item">
            <va-icon name="logout" class="logout-icon" />
            Logout
          </va-menu-item>
        </va-menu>
      </div>

      <div class="records-list">
        <h3 class="text-xl font-semibold mb-4">Recent Workouts</h3>
        <div v-if="loading" class="loading">Loading...</div>
        <template v-else>
          <div v-if="Object.keys(groupedRecords).length === 0" class="no-records">
            No workouts recorded yet
          </div>
          <div v-else class="date-groups">
            <div 
              v-for="(records, date) in groupedRecords" 
              :key="date" 
              class="date-group"
            >
              <div class="date-header">{{ date }}</div>
              <div class="workouts-container">
                <div 
                  v-for="record in records" 
                  :key="record.id" 
                  class="workout-item"
                >
                  <div class="workout-info">
                    <img 
                      :src="getImageSrc(record)" 
                      :alt="record.name" 
                      class="workout-image"
                      @click="handleImageClick(record)"
                    >
                    <span class="workout-name">{{ record.name }}</span>
                  </div>
                  <div class="progress-container">
                    <div 
                      class="progress-bar"
                      :style="{ width: getProgressWidth(record.duration, getMaxDuration(records)) }"
                    ></div>
                    <span class="duration-text">{{ record.duration }} mins</span>
                  </div>
                  <va-menu>
                    <template #anchor>
                      <button class="action-btn">
                        <va-icon name="more_vert" />
                      </button>
                    </template>
                    <va-menu-item @click="handleDelete(record)" class="delete-item">
                      <va-icon name="delete" class="delete-icon" />
                      Delete
                    </va-menu-item>
                  </va-menu>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <va-modal 
      v-model="showNewWorkoutForm" 
      hide-default-header
      hide-default-actions
      class="modal-fullscreen"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">Choose Your Workout</h2>
          <button class="close-button" @click="showNewWorkoutForm = false">
            <va-icon name="close" />
          </button>
        </div>

        <div class="popup-actions">
          <div v-if="loadingExercises" class="loading">Loading exercises...</div>
          <div v-else class="exercise-grid">
            <div 
              v-for="exercise in exercises" 
              :key="exercise.id"
              class="exercise-card"
              :class="{ 'selected': newWorkout.name === exercise.name }"
              @click="handleSelectExercise(exercise)"
            >
              <img :src="exercise.gifUrl" :alt="exercise.name" class="exercise-gif">
              <div class="exercise-name">{{ exercise.name }}</div>
            </div>
          </div>
          
          <div class="form-footer">
            <div class="form-row">
              <va-input
                v-model="newWorkout.duration"
                type="number"
                placeholder="Duration (minutes)"
                class="form-input"
              />
              <va-date-input
                v-model="newWorkout.date"
                class="form-input"
              />
              <button 
                class="btn-primary submit-button" 
                @click="handleSubmitWorkout" 
                :disabled="loading || !newWorkout.name || !newWorkout.duration"
              >
                {{ loading ? 'Saving...' : 'Start Workout' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </va-modal>

    <va-menu v-model="showActionMenu" :position="menuPosition">
      <va-menu-item @click="handleEdit">Edit</va-menu-item>
      <va-menu-item @click="handleDelete">Delete</va-menu-item>
    </va-menu>

    <va-modal
      v-model="showImagePreview"
      hide-default-actions
      class="image-preview-modal"
      :max-width="false"
      :max-height="false"
    >
      <div class="image-preview-content">
        <div class="preview-header">
          <h3>{{ previewImage.name }}</h3>
          <button class="close-button" @click="showImagePreview = false">
            <va-icon name="close" />
          </button>
        </div>
        <div class="preview-body">
          <img :src="previewImage.url" :alt="previewImage.name" class="preview-image">
        </div>
      </div>
    </va-modal>
  </div>
</template>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.main-card {
  margin-bottom: 20px;
}

.start-workout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.records-list {
  max-height: 80vh;
  overflow-y: auto;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 15px;
}

.record-info {
  display: flex;
  gap: 20px;
  align-items: center;
}

.record-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.record-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.record-type {
  font-weight: 500;
}

.record-duration, .record-date {
  font-size: 0.9em;
  color: var(--text-color);
  opacity: 0.8;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color);
}

.modal-fullscreen :deep(.va-modal__dialog) {
  margin: 0 auto;
  height: 90vh;
  max-height: 800px;
  max-width: 90vw;
  width: 800px;
}

.modal-fullscreen :deep(.va-modal__content) {
  padding: 0;
}

.modal-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.6;
  transition: opacity 0.3s;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  opacity: 1;
}

.popup-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
  flex: 1;
  overflow: hidden;
}

.form-footer {
  padding: 16px;
  background: white;
  border-top: 1px solid rgba(0,0,0,0.1);
}

.form-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.form-input {
  flex: 2;
  min-width: 0;
}

.form-input :deep(.va-input-wrapper),
.form-input :deep(.va-date-input__input) {
  margin-bottom: 0;
}

.submit-button {
  flex: 3;
  white-space: nowrap;
  padding: 12px 24px;
}

.workout-modal {
  max-width: 90vw;
  width: 800px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.workout-modal :deep(.va-modal__dialog) {
  margin: 0 auto;
  height: 90vh;
  max-height: 800px;
  display: flex;
  flex-direction: column;
}

.workout-modal :deep(.va-modal__content) {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.exercise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-height: 40vh;
  overflow-y: scroll;
  padding: 16px;
}

.exercise-grid::-webkit-scrollbar {
  width: 8px;
}

.exercise-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.exercise-grid::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.exercise-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.exercise-card {
  border-radius: 8px;
  overflow: hidden;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.exercise-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.exercise-card.selected {
  border-color: var(--primary-color);
}

.exercise-gif {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.exercise-name {
  padding: 12px;
  font-size: 14px;
  text-align: center;
  color: var(--text-color);
}

.loading {
  text-align: center;
  padding: 20px;
  color: var(--text-color);
}

.no-records {
  text-align: center;
  padding: 20px;
  color: var(--text-color);
  font-style: italic;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  height: 48px;
}

.start-workout {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0 24px;
}

.avatar-button {
  width: 48px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border: 2px solid var(--primary-color);
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  background: white;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin: 0;
}

.avatar-button:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.logout-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #dc3545;
  padding: 8px 16px;
  min-width: 120px;
}

.logout-icon {
  font-size: 18px;
}

.date-groups {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.date-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.date-header {
  font-weight: 500;
  color: var(--text-color);
  opacity: 0.8;
  padding: 0 8px;
}

.workouts-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.workout-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.workout-info {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 200px;
  flex-shrink: 0;
}

.workout-image {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.2s;
}

.workout-image:hover {
  transform: scale(1.1);
}

.workout-name {
  font-weight: 500;
  color: var(--text-color);
}

.progress-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding-right: 16px;
}

.progress-bar {
  height: 8px;
  background: var(--primary-color);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.duration-text {
  font-size: 0.9em;
  color: var(--text-color);
  opacity: 0.8;
  white-space: nowrap;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color);
  opacity: 0.6;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 1;
}

.delete-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #dc3545;
  padding: 8px 16px;
  min-width: 120px;
}

.delete-icon {
  font-size: 18px;
}

.image-preview-modal :deep(.va-modal__dialog) {
  max-width: 90vw;
  max-height: 90vh;
  width: auto;
  margin: 0 auto;
}

.image-preview-modal :deep(.va-modal__content) {
  padding: 0;
}

.image-preview-content {
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.preview-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--text-color);
}

.preview-body {
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0,0,0,0.03);
}

.preview-image {
  max-width: 100%;
  max-height: calc(90vh - 120px);
  object-fit: contain;
  border-radius: 8px;
}
</style> 