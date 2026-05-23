export default function EvidenceCards({ evidence = [] }) {
  return (
    <div className="glass rounded-2xl p-5">
      <h3 className="mb-4 font-bold">Retrieved Evidence</h3>
      <div className="space-y-3">
        {evidence.length === 0 && <p className="text-sm text-white/50">Upload documents to power grounded retrieval.</p>}
        {evidence.map((item, index) => (
          <div key={`${item.source}-${item.chunk}-${index}`} className="rounded-xl border border-white/10 bg-black/20 p-3">
            <div className="mb-2 flex justify-between text-xs text-webblue">
              <span>{item.source} · chunk {item.chunk}</span>
              <span>score {Number(item.score).toFixed(3)}</span>
            </div>
            <p className="line-clamp-4 text-sm text-white/70">{item.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
