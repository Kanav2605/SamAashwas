/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/**/*.{html,js}",
    "./docs/**/*.{html,md}"
  ],
  theme: {
    extend: {
      colors: {
        paper: "#FFF6E5",
        "paper-2": "#FFEFD0",
        ink: "#231F20",
        tomato: "#FF5A4E",
        mustard: "#FFC93C",
        mint: "#7BDCB5",
        bubblegum: "#FF9EC4",
        lavender: "#B8A6FF",
        peach: "#FFB88A",
        "cream-white": "#FFFDF7",
      },
      fontFamily: {
        display: ["Fredoka", "Bricolage Grotesque", "cursive", "sans-serif"],
        body: ["Nunito", "sans-serif"],
        handwriting: ["Caveat", "cursive"],
      },
      boxShadow: {
        hard: "4px 4px 0 #231F20",
        "hard-sm": "2px 2px 0 #231F20",
        "hard-lg": "6px 6px 0 #231F20",
        "hard-xl": "8px 8px 0 #231F20",
        "hard-pressed": "1px 1px 0 #231F20",
      },
      borderWidth: {
        ink: "2.5px",
        "ink-thick": "3.5px",
      },
      borderRadius: {
        sticker: "20px",
        "sticker-lg": "28px",
      }
    },
  },
  plugins: [],
};
