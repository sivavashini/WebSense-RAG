const colors = {
  LOW: '#22c55e',
  MEDIUM: '#eab308',
  HIGH: '#f97316',
  CRITICAL: '#ff1744',
}

const values = { LOW: 25, MEDIUM: 50, HIGH: 75, CRITICAL: 96 }

export default function RiskMeter({ risk }) {
  const level = risk?.risk_level || 'LOW'
  const value = values[level] || 25
  const color = colors[level] || colors.LOW
  const dash = `${value * 2.64} 264`

  return (
    <div className={`glass rounded-2xl p-5 ${['HIGH', 'CRITICAL'].includes(level) ? 'animate-pulseDanger' : ''}`}>
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-bold">SpideySense Risk Meter</h3>
        <span className="rounded-full px-3 py-1 text-xs font-black" style={{ backgroundColor: `${color}22`, color }}>{level}</span>
      </div>
      <div className="relative mx-auto h-52 w-52">
        <svg className="-rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" stroke="rgba(255,255,255,.12)" strokeWidth="9" fill="none" />
          <circle cx="50" cy="50" r="42" stroke={color} strokeWidth="9" strokeLinecap="round" fill="none" strokeDasharray={dash} className="transition-all duration-700" />
        </svg>
        <div className="absolute inset-0 grid place-items-center text-center">
          <div>
            <div className="text-4xl font-black" style={{ color }}>{Math.round((risk?.confidence || .58) * 100)}%</div>
            <div className="text-sm text-white/50">{risk?.category || 'Awaiting signal'}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
