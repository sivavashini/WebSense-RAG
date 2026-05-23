import { useEffect, useState } from 'react'

export function useWebSocket() {
  const [event, setEvent] = useState(null)

  useEffect(() => {
    // Vercel deployment: WebSocket URL follows the same /api prefix as the backend service.
    // If the serverless host does not support WebSockets, the UI simply continues without live events.
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url = import.meta.env.VITE_WS_URL || `${protocol}//${window.location.host}/api/ws`
    const ws = new WebSocket(url)
    ws.onmessage = (message) => setEvent(JSON.parse(message.data))
    ws.onerror = () => setEvent(null)
    return () => ws.close()
  }, [])

  return event
}
