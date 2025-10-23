/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'premier': {
          50: '#e6f2ff',
          100: '#cce5ff',
          500: '#045af9',
          600: '#0350e0',
          700: '#0246c7',
        },
        'dark': '#161614',
      },
      fontFamily: {
        'sans': ['Nunito', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
