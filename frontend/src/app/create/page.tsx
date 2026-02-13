"use client";
import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function CreateEvent() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: 'Mystery Night',
    theme: 'Victorian Steampunk',
    tone: 'mystery',
    participants: [] // Will hold strings
  });
  const [tempParticipant, setTempParticipant] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Use absolute URL correctly
  const API_URL = "http://localhost:8000/api/events";

  const handleCreate = async () => {
    setIsLoading(true);
    try {
      // 1. Create Event
      const res = await axios.post(`${API_URL}/`, {
        name: formData.name,
        theme: formData.theme,
        tone: formData.tone
      });
      const eventId = res.data.id;

      // 2. Add Participants
      if (formData.participants.length > 0) {
        await axios.post(`${API_URL}/${eventId}/participants`,
          formData.participants.map(p => ({ name: p }))
        );
      }

      // 3. Trigger Generation
      await axios.post(`${API_URL}/${eventId}/generate`);

      // Redirect to dashboard
      router.push(`/events/${eventId}/dashboard`);
    } catch (e) {
      alert("Error creating event: " + e);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-10 flex flex-col items-center">
      <div className="w-full max-w-2xl bg-slate-800 p-8 rounded-2xl shadow-xl">
        <div className="mb-8 flex justify-between items-center border-b border-slate-700 pb-4">
          <h2 className="text-2xl font-bold">Step {step} of 2</h2>
        </div>

        {step === 1 && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Event Name</label>
              <input
                className="w-full bg-slate-700 rounded p-3 text-white border border-slate-600 focus:border-purple-500 outline-none"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Theme</label>
              <input
                className="w-full bg-slate-700 rounded p-3 text-white border border-slate-600 focus:border-purple-500 outline-none"
                value={formData.theme}
                onChange={e => setFormData({ ...formData, theme: e.target.value })}
                placeholder="e.g. 1920s Mafia, Cyberpunk, Harry Potter..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Tone</label>
              <select
                className="w-full bg-slate-700 rounded p-3 text-white border border-slate-600 focus:border-purple-500 outline-none"
                value={formData.tone}
                onChange={e => setFormData({ ...formData, tone: e.target.value })}
              >
                <option value="mystery">Serious Mystery</option>
                <option value="humor">Absurd/Humorous</option>
                <option value="horror">Dark Horror</option>
              </select>
            </div>
            <button
              onClick={() => setStep(2)}
              className="w-full bg-purple-600 py-3 rounded-lg font-bold mt-4 hover:bg-purple-700"
            >
              Next: Participants
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Add Participants</label>
              <div className="flex gap-2">
                <input
                  className="flex-1 bg-slate-700 rounded p-3 text-white border border-slate-600"
                  value={tempParticipant}
                  onChange={e => setTempParticipant(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && (setFormData(p => ({ ...p, participants: [...p.participants, tempParticipant] })), setTempParticipant(''))}
                  placeholder="Player Name"
                />
                <button
                  onClick={() => {
                    if (tempParticipant) {
                      setFormData(p => ({ ...p, participants: [...p.participants, tempParticipant] }));
                      setTempParticipant('');
                    }
                  }}
                  className="bg-blue-600 px-4 rounded"
                >
                  Add
                </button>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              {formData.participants.map((p, i) => (
                <span key={i} className="bg-slate-600 px-3 py-1 rounded-full text-sm flex items-center gap-2">
                  {p}
                  <button onClick={() => setFormData(d => ({ ...d, participants: d.participants.filter(x => x !== p) }))}>×</button>
                </span>
              ))}
              {formData.participants.length === 0 && <span className="text-slate-500 text-sm">No participants yet.</span>}
            </div>

            <button
              onClick={handleCreate}
              disabled={isLoading || formData.participants.length < 2}
              className="w-full bg-green-600 py-3 rounded-lg font-bold mt-8 hover:bg-green-700 disabled:opacity-50"
            >
              {isLoading ? "Generating Magic..." : "Create & Generate Game"}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
