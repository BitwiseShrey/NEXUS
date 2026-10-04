/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nexus: {
          950: '#070A12',
          900: '#0B0F19',
          850: '#101626',
          800: '#161F36',
          700: '#23304E',
          accent: '#3B82F6',
          emerald: '#10B981',
          amber: '#F59E0B',
          rose: '#EF4444',
          cyan: '#06B6D4',
          purple: '#8B5CF6'
        }
      }
    },
  },
  plugins: [],
}
