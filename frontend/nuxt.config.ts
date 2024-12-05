// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  
  modules: [
    '@vuestic/nuxt'
  ],

  vuestic: {
    config: {
      // Vuestic config here
    }
  },

  compatibilityDate: '2024-11-01',
  devtools: { enabled: true }
})
