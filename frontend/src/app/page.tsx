import Link from 'next/link';
import { Sparkles, Users, Scroll } from 'lucide-react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-mystery-dark text-white p-24 relative overflow-hidden">
      <div className="z-10 text-center max-w-2xl">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
          AI Cluedo Maker
        </h1>
        <p className="text-xl text-gray-300 mb-10">
          Generate immersive live-action mystery games in minutes.
          Upload participants, choose a theme, and let AI craft the intrigue.
        </p>

        <Link
          href="/create"
          className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 px-8 rounded-full text-xl transition-all shadow-lg hover:shadow-purple-500/50 flex items-center justify-center gap-2 mx-auto w-fit"
        >
          <Sparkles className="w-6 h-6" />
          Create New Event
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 z-10">
        <div className="bg-slate-800/50 p-6 rounded-xl backdrop-blur-sm border border-slate-700">
          <Users className="w-10 h-10 text-purple-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Smart Casting</h3>
          <p className="text-slate-400">AI assigns roles and factions based on your group dynamics.</p>
        </div>
        <div className="bg-slate-800/50 p-6 rounded-xl backdrop-blur-sm border border-slate-700">
          <Scroll className="w-10 h-10 text-pink-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Complete Dossiers</h3>
          <p className="text-slate-400">Generate public and secret character sheets with one click.</p>
        </div>
        <div className="bg-slate-800/50 p-6 rounded-xl backdrop-blur-sm border border-slate-700">
          <Sparkles className="w-10 h-10 text-blue-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Visuals Included</h3>
          <p className="text-slate-400">Beautiful AI-generated character portraits and item cards.</p>
        </div>
      </div>
    </main>
  )
}
