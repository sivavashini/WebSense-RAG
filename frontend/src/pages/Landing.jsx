import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Activity, FileSearch, ShieldAlert } from 'lucide-react'
import SpiderWeb from '../components/SpiderWeb.jsx'
import Typewriter from '../components/Typewriter.jsx'

export default function Landing() {
  return (
    <main className="relative overflow-hidden">
      <section className="relative mx-auto flex min-h-[calc(100vh-65px)] max-w-7xl items-center px-4 py-16">
        <SpiderWeb />
        <div className="relative z-10 max-w-3xl">
          <motion.p initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-4 text-sm font-bold uppercase tracking-[.35em] text-webblue">
            With great power comes great responsibility
          </motion.p>
          <motion.h1 initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .1 }} className="text-5xl font-black leading-tight md:text-7xl">
            WebSense RAG
          </motion.h1>
          <p className="mt-5 text-2xl text-white/80"><Typewriter text="Your AI-powered responsibility assistant." /></p>
          <p className="mt-5 max-w-2xl text-white/60">
            Describe dangerous, ethical, cyber, emergency, or suspicious situations. WebSense retrieves evidence, classifies risk, and gives calm next actions.
          </p>
          <Link to="/dashboard" className="btn-primary mt-8 inline-flex">Activate SpideySense</Link>
        </div>
        <div className="absolute right-8 top-28 hidden w-80 space-y-4 lg:block">
          {[
            [ShieldAlert, 'Danger pulse', 'High-risk signals trigger cinematic warning states.'],
            [FileSearch, 'Grounded retrieval', 'Evidence cards show the sources behind advice.'],
            [Activity, 'Responsibility engine', 'Advice prioritizes safety, ethics, and escalation.'],
          ].map(([Icon, title, body], i) => (
            <motion.div key={title} initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: .25 + i * .1 }} className="glass animate-float rounded-2xl p-5" style={{ animationDelay: `${i * .7}s` }}>
              <Icon className="mb-3 text-webred" />
              <h3 className="font-bold">{title}</h3>
              <p className="text-sm text-white/60">{body}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </main>
  )
}
