/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        warehouse: {
          bg: '#0f1117',
          panel: '#1a1a2e',
        }
      }
    },
  },
  plugins: [],
}
