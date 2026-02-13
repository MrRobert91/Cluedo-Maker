"use client";
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'next/navigation';

export default function Dashboard() {
  const { id } = useParams(); // event id
  const [event, setEvent] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(1000);

  const API_URL = "http://localhost:8000/api/events";

  useEffect(() => {
    if (!id) return;
    const fetchEvent = async () => {
      try {
        const res = await axios.get(`${API_URL}/${id}`);
        setEvent(res.data);
        if (res.data.status === 'ready' || res.data.status === 'error') {
          setRefreshInterval(null); // Stop polling
        }
      } catch (e) {
        console.error(e);
      }
    };

    fetchEvent();
    const timer = refreshInterval ? setInterval(fetchEvent, refreshInterval) : null;
    return () => clearInterval(timer);
  }, [id, refreshInterval]);

  if (!event) return <div className="p-10 text-white">Loading...</div>;

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">{event.name}</h1>
            <p className="text-slate-400">{event.theme} • {event.tone}</p>
          </div>
          <div className={`px-4 py-2 rounded-full capitalize font-bold ${event.status === 'ready' ? 'bg-green-500/20 text-green-400' :
              event.status === 'generating' ? 'bg-yellow-500/20 text-yellow-400 animate-pulse' :
                'bg-slate-700'
            }`}>
            {event.status}
          </div>
        </header>

        {event.status === 'generating' && (
          <div className="text-center py-20">
            <div className="text-2xl mb-4">🔮 Concocting the mystery...</div>
            <p className="text-slate-500">The AI agents are building factions, writing secrets, and planting clues.</p>
          </div>
        )}

        {event.status === 'ready' && (
          <div className="grid gap-6">
            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h2 className="text-xl font-bold mb-4">Downloads</h2>
              <div className="flex gap-4">
                <button className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-bold">
                  📥 Public Packet (Introduction & Bios)
                </button>
                <button className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-bold">
                  🗂️ Organizer Dossier (Secrets & Solutions)
                </button>
              </div>
            </div>

            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
              <h2 className="text-xl font-bold mb-4">Participants & Roles</h2>
              {/* Placeholder for now as the simple endpoint doesn't return full relation tree yet, usually you'd need a separate fetch for participants/characters */}
              <div className="text-slate-400">
                {event.num_participants} players ready. (Detailed character view coming in next implementation block)
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
