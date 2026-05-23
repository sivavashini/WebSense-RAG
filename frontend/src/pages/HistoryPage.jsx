import { useEffect, useState } from 'react'
import { api, reportUrl } from '../api/client.js'

export default function HistoryPage() {
  const [items, setItems] = useState([])

  useEffect(() => {
    api.get('/history').then((res) => setItems(res.data)).catch(() => setItems([]))
  }, [])

  return (
    <main className="mx-auto max-w-6xl px-4 py-10">
      <h1 className="mb-6 text-4xl font-black">Incident History</h1>
      <div className="space-y-4">
        {items.map((item) => (
          <article key={item.id} className="glass rounded-2xl p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="font-bold">Incident #{item.id}</h2>
              <span className="rounded-full bg-webred/15 px-3 py-1 text-sm text-webred">{item.risk_level} · {item.category} · {Math.round(item.confidence * 100)}%</span>
            </div>
            <p className="mt-3 text-white/70">{item.situation}</p>
            <a href={reportUrl(item.id)} className="mt-4 inline-flex text-sm text-webblue">Export PDF</a>
          </article>
        ))}
        {items.length === 0 && <div className="glass rounded-2xl p-8 text-white/50">No incidents yet.</div>}
      </div>
    </main>
  )
}
