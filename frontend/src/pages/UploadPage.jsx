import { useState } from 'react'
import { UploadCloud } from 'lucide-react'
import { api } from '../api/client.js'
import { useWebSocket } from '../hooks/useWebSocket.js'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const event = useWebSocket()

  const upload = async () => {
    if (!file) return
    setError('')
    setResult(null)
    const form = new FormData()
    form.append('file', file)
    try {
      const res = await api.post('/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => setProgress(Math.round((e.loaded * 100) / e.total)),
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    }
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <h1 className="mb-6 text-4xl font-black">Knowledge Upload</h1>
      <div
        onDrop={(e) => { e.preventDefault(); setFile(e.dataTransfer.files[0]) }}
        onDragOver={(e) => e.preventDefault()}
        className="glass grid min-h-80 place-items-center rounded-2xl border-dashed p-8 text-center"
      >
        <div>
          <UploadCloud className="mx-auto mb-4 text-webblue" size={54} />
          <p className="text-xl font-bold">Drag PDF, TXT, or DOCX here</p>
          <p className="mt-2 text-white/50">Documents are parsed, chunked, embedded, and stored in FAISS.</p>
          <input className="mt-6" type="file" accept=".pdf,.txt,.docx" onChange={(e) => setFile(e.target.files[0])} />
          {file && <p className="mt-4 text-webblue">{file.name} · {(file.size / 1024 / 1024).toFixed(2)} MB</p>}
          <button onClick={upload} className="btn-primary mt-5">Index Document</button>
        </div>
      </div>
      <div className="mt-6 h-3 overflow-hidden rounded-full bg-white/10"><div className="h-full bg-webblue transition-all" style={{ width: `${progress}%` }} /></div>
      {result && <div className="glass mt-6 rounded-2xl p-5">Indexed {result.filename}: {result.chunks} chunks stored in {result.vector_store}.</div>}
      {error && <div className="mt-6 rounded-2xl border border-webred bg-webred/10 p-5 text-webred">{error}</div>}
      {event && <div className="mt-4 text-sm text-webblue">Live indexing status: {event.type}</div>}
    </main>
  )
}
