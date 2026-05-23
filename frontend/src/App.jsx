import { Moon, Sun, UploadCloud, Shield, History, Info, RadioTower } from 'lucide-react'
import { Link, NavLink, Route, Routes } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Landing from './pages/Landing.jsx'
import Dashboard from './pages/Dashboard.jsx'
import UploadPage from './pages/UploadPage.jsx'
import HistoryPage from './pages/HistoryPage.jsx'
import About from './pages/About.jsx'

const links = [
  ['/', 'Home', Shield],
  ['/dashboard', 'Dashboard', RadioTower],
  ['/upload', 'Upload', UploadCloud],
  ['/history', 'History', History],
  ['/about', 'About', Info],
]

export default function App() {
  const [dark, setDark] = useState(true)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  return (
    <div className="min-h-screen bg-slate-100 text-slate-950 dark:bg-night dark:text-white">
      <div className="fixed inset-0 -z-10 bg-web-grid opacity-50" />
      <nav className="sticky top-0 z-40 border-b border-white/10 bg-night/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="flex items-center gap-3 font-black tracking-wide">
            <span className="grid h-10 w-10 place-items-center rounded-full bg-webred shadow-danger">W</span>
            <span>WebSense RAG</span>
          </Link>
          <div className="hidden items-center gap-2 md:flex">
            {links.map(([to, label, Icon]) => (
              <NavLink key={to} to={to} className={({ isActive }) => `nav-link ${isActive ? 'nav-active' : ''}`}>
                <Icon size={16} /> {label}
              </NavLink>
            ))}
          </div>
          <button onClick={() => setDark(!dark)} className="icon-button" aria-label="Toggle theme">
            {dark ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  )
}
