import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { Mic, Send, Volume2 } from 'lucide-react'
import { api, reportUrl } from '../api/client.js'
import EvidenceCards from '../components/EvidenceCards.jsx'
import RiskMeter from '../components/RiskMeter.jsx'
import { useWebSocket } from '../hooks/useWebSocket.js'

const categories = [
  'Pet Safety',
  'Lost & Found',
  'Public Help',
  'Cyber Threat',
  'Physical Threat',
  'Medical Emergency',
  'Ethical Concern',
  'Suspicious Activity',
  'Harassment',
  'Theft',
]

export default function Dashboard() {
  const [message, setMessage] = useState('')
  const [chat, setChat] = useState([])
  const [latest, setLatest] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [pulse, setPulse] = useState(false)
  const wsEvent = useWebSocket()
  const endRef = useRef(null)

  useEffect(() => {
    api.get('/history?limit=8').then((res) => setHistory(res.data)).catch(() => {})
  }, [latest])

  useEffect(() => {
    if (latest && ['HIGH', 'CRITICAL'].includes(latest.risk.risk_level)) {
      setPulse(true)
      setTimeout(() => setPulse(false), 2300)
    }
  }, [latest])

  useEffect(() => endRef.current?.scrollIntoView({ behavior: 'smooth' }), [chat, loading])

  const submit = async () => {
    if (!message.trim()) return
    const text = message.trim()
    setMessage('')
    setChat((items) => [...items, { role: 'user', text }])
    setLoading(true)
    try {
      const res = await api.post('/chat', { message: text, top_k: 4 })
      setLatest(res.data)
      setChat((items) => [...items, { role: 'ai', text: res.data.ai_response }])
    } catch (error) {
      setChat((items) => [...items, { role: 'ai', text: error.response?.data?.detail || 'WebSense signal failed. Check the backend.' }])
    } finally {
      setLoading(false)
    }
  }

  const voice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return
    const recog = new SpeechRecognition()
    recog.onresult = (event) => setMessage(event.results[0][0].transcript)
    recog.start()
  }

  return (
    <main className={pulse ? 'risk-pulse' : ''}>
      <div className="mx-auto grid max-w-7xl gap-4 px-4 py-6 lg:grid-cols-[260px_1fr_340px]">
        <aside className="space-y-4">
          <div className="glass rounded-2xl p-4">
            <h3 className="mb-3 font-bold">Previous Incidents</h3>
            <div className="space-y-2">
              {history.map((item) => <div key={item.id} className="rounded-xl bg-white/5 p-3 text-sm text-white/70">{item.risk_level} · {item.category}</div>)}
            </div>
          </div>
          <div className="glass rounded-2xl p-4">
            <h3 className="mb-3 font-bold">Risk Categories</h3>
            <div className="flex flex-wrap gap-2">
              {categories.map((cat) => <span key={cat} className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/70">{cat}</span>)}
            </div>
          </div>
        </aside>

        <section className="glass flex min-h-[78vh] flex-col rounded-2xl">
          <div className="border-b border-white/10 p-4">
            <h2 className="text-xl font-black">AI Chat Dashboard</h2>
            <p className="text-sm text-white/50">Describe the situation. WebSense will retrieve, classify, and advise.</p>
          </div>
          <div className="flex-1 space-y-4 overflow-y-auto p-4">
            {chat.length === 0 && <div className="rounded-2xl border border-dashed border-white/20 p-8 text-center text-white/50">Awaiting responsibility signal.</div>}
            {chat.map((item, index) => (
              <motion.div key={index} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className={`max-w-[85%] whitespace-pre-wrap rounded-2xl p-4 ${item.role === 'user' ? 'ml-auto bg-webblue/20' : 'bg-white/10'}`}>
                {item.text}
              </motion.div>
            ))}
            {loading && <div className="rounded-2xl bg-white/10 p-4 text-webblue">WebSense AI is tracing the evidence...</div>}
            <div ref={endRef} />
          </div>
          <div className="flex gap-2 border-t border-white/10 p-4">
            <button className="icon-button" onClick={voice} aria-label="Voice input"><Mic size={18} /></button>
            <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && submit()} className="input" placeholder="Example: I got a suspicious email asking for my OTP..." />
            <button className="icon-button" onClick={submit} aria-label="Send"><Send size={18} /></button>
          </div>
        </section>

        <aside className="space-y-4">
          <RiskMeter risk={latest?.risk} />
          <div className="glass rounded-2xl p-5">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-bold">Action Checklist</h3>
              <Volume2 size={18} className="text-webred" />
            </div>
            <div className="space-y-2">
              {(latest?.actions || ['Upload knowledge, describe a situation, and activate WebSense.']).map((action) => (
                <label key={action} className="flex gap-3 rounded-xl bg-white/5 p-3 text-sm text-white/70"><input type="checkbox" /> {action}</label>
              ))}
            </div>
            {latest?.incident_id && <a className="mt-4 inline-flex text-sm text-webblue" href={reportUrl(latest.incident_id)}>Export incident report PDF</a>}
          </div>
          <EvidenceCards evidence={latest?.evidence || []} />
          {wsEvent && <div className="rounded-xl border border-webblue/30 bg-webblue/10 p-3 text-xs text-webblue">Live: {wsEvent.type}</div>}
        </aside>
      </div>
    </main>
  )
}
