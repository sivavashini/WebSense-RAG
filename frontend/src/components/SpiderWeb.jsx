import { motion } from 'framer-motion'

export default function SpiderWeb() {
  return (
    <motion.svg
      viewBox="0 0 500 500"
      className="absolute inset-0 h-full w-full opacity-30"
      initial={{ opacity: 0, rotate: -4 }}
      animate={{ opacity: .35, rotate: 0 }}
      transition={{ duration: 1.4 }}
    >
      <g fill="none" stroke="currentColor" strokeWidth="1" className="text-webblue">
        {[70, 130, 190, 250].map((r) => <circle key={r} cx="250" cy="250" r={r} />)}
        {Array.from({ length: 16 }).map((_, i) => {
          const angle = (Math.PI * 2 * i) / 16
          return <line key={i} x1="250" y1="250" x2={250 + Math.cos(angle) * 250} y2={250 + Math.sin(angle) * 250} />
        })}
      </g>
    </motion.svg>
  )
}
