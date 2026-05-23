export default function About() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-10">
      <div className="glass rounded-2xl p-8">
        <h1 className="text-4xl font-black">About WebSense RAG</h1>
        <p className="mt-5 text-white/70">
          WebSense RAG is an AI-powered safety and responsibility assistant inspired by Spidey Sense and the idea that power should be used carefully.
          It combines retrieval augmented generation, local risk classification, evidence display, and action checklists to help users make safer decisions.
        </p>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {['RAG evidence', 'Risk intelligence', 'Responsible action'].map((item) => (
            <div key={item} className="rounded-2xl border border-white/10 bg-white/5 p-5 font-bold">{item}</div>
          ))}
        </div>
      </div>
    </main>
  )
}
