module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  extend: {
    animation: {
      typewriter:
        "typewriter 4s steps(40) 1s 1 normal both, blink 0.6s step-end infinite",
    },
    keyframes: {
      typewriter: {
        "0%": { width: "0%" },
        "100%": { width: "100%" },
      },
      blink: {
        "0%, 100%": { "border-color": "transparent" },
        "50%": { "border-color": "black" },
      },
    },
  },

  plugins: [],
};
