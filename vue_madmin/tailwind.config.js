/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  corePlugins: {
    preflight: false
  },
  theme: {
    extend: {
    },
  },
  plugins: [],
}
