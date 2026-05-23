export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        webred: '#ff1744',
        webblue: '#00d9ff',
        night: '#060814',
      },
      boxShadow: {
        neon: '0 0 24px rgba(0, 217, 255, .28), 0 0 36px rgba(255, 23, 68, .22)',
        danger: '0 0 36px rgba(255, 23, 68, .55)',
      },
      animation: {
        pulseDanger: 'pulseDanger 1.2s ease-in-out infinite',
        float: 'float 6s ease-in-out infinite',
      },
      keyframes: {
        pulseDanger: {
          '0%, 100%': { boxShadow: '0 0 0 rgba(255,23,68,0)' },
          '50%': { boxShadow: '0 0 44px rgba(255,23,68,.72)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-14px)' },
        },
      },
    },
  },
  plugins: [],
}
