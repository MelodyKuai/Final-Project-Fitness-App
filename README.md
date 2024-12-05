# Final-Project-Fitness-App
Link to presentation video:
# Workout Tracker

A modern web application for tracking your daily workouts and discovering new exercises. Built with Vue.js and ExerciseDB API.

## Features

### 🏋️‍♂️ Exercise Library
- Browse through a comprehensive collection of exercises
- Detailed picture for each exercise:
  - Target muscle groups and body parts
  - Required equipment

### 📝 Workout Tracking
- Record your daily workouts with duration
- View workout history organized by date
- Track progress with visual duration indicators
- Quick access to exercise picture

### 👤 User Management
- Secure user authentication
- Personal workout history
- Easy registration and login

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm (v7 or higher)
- Backend server running on `http://localhost:5000`

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Application will be available at:
http://localhost:3000
```
### API Configuration
The application requires:
- Backend API running on `http://localhost:5000`
- ExerciseDB API key for exercise data

## Tech Stack

- **Frontend**: Vue.js 3 with Composition API
- **UI Components**: Vuestic UI
- **API Integration**: ExerciseDB API
- **State Management**: Vue Reactivity
- **Notifications**: Vue Toastification
- **Authentication**: Session-based with HTTP-only cookies

## Usage

1. **Register/Login**: Create an account or login to access your personal workout tracker
2. **Browse Exercises**: Explore the exercise library with detailed instructions
3. **Record Workout**: Click "Start Today's Workout" to:
   - Select an exercise
   - Set duration
   - Save to your history
4. **View History**: See your workout history organized by date
5. **Track Progress**: Monitor your workout frequency and duration


# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.
npx nuxi@latest init my-app 

## Setup

!!!Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
