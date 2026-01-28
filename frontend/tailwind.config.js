/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Tajawal', 'sans-serif'],
      },
      colors: {
        'brand': '#6CAD85',
        'page-bg': '#F4F6F8',
        'pill-bg': '#F0F2F4',
        'bubble-user': '#6CAD85',
        'bubble-bot': '#EEF0F2',
      },
      borderRadius: {
        'card': '48px',
        'bubble': '28px',
      },
    },
  },
  plugins: [],
}
