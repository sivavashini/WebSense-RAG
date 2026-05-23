import { useEffect, useState } from 'react'

export function useWebSocket() {
  const [event, setEvent] = useState(null)

  useEffect(() => {
    const url = (import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws')
    const ws = new WebSocket(url)
    ws.onmessage = (message) => setEvent(JSON.parse(message.data))
    return () => ws.close()
  }, [])

  return event
}
