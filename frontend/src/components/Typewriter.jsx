import { useEffect, useState } from 'react'

export default function Typewriter({ text }) {
  const [visible, setVisible] = useState('')
  useEffect(() => {
    let i = 0
    const timer = setInterval(() => {
      setVisible(text.slice(0, i + 1))
      i += 1
      if (i >= text.length) clearInterval(timer)
    }, 42)
    return () => clearInterval(timer)
  }, [text])
  return <span>{visible}<span className="text-webblue">|</span></span>
}
