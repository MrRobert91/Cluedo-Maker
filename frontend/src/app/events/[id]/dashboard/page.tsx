'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import axios from 'axios';

interface Project {
  id: number;
  name: string;
  theme: string;
  tone: string;
  num_participants: number;
  status: string;
}

export default function DashboardPage() {
  const params = useParams();
  const router = useRouter();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Use env variable or fallback
  const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";
  const BASE_API_URL = rawApiUrl.replace(/\/events\/?$/, "");

  useEffect(() => {
    if (!params.id) return;

    const fetchProject = async () => {
      try {
        // Note: We need to implement GET /api/projects/{id} in backend
        const response = await axios.get(`${BASE_API_URL}/projects/${params.id}`);
        setProject(response.data);
      } catch (err: any) {
        console.error(err);
        setError('Failed to load project details.');
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [params.id, BASE_API_URL]);

  if (loading) return <div className="text-white text-center mt-20">Loading project...</div>;
  if (error) return <div className="text-red-400 text-center mt-20">{error}</div>;
  if (!project) return <div className="text-white text-center mt-20">Project not found</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
          {project.name}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h2 className="text-xl font-semibold mb-4 text-purple-300">Project Details</h2>
            <div className="space-y-2 text-gray-300">
              <p><span className="font-medium text-gray-500">Status:</span> {project.status}</p>
              <p><span className="font-medium text-gray-500">Participants:</span> {project.num_participants}</p>
              <p><span className="font-medium text-gray-500">Theme:</span> {project.theme}</p>
              <p><span className="font-medium text-gray-500">Tone:</span> {project.tone}</p>
            </div>
          </div>

          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col justify-center items-center">
            <h2 className="text-xl font-semibold mb-4 text-pink-300">Configuration</h2>
            <p className="text-gray-400 text-center mb-6">
              Configure factions and other settings before generating the game.
            </p>
            <button
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-bold hover:shadow-lg transition-all"
              onClick={() => alert("Configuration Wizard coming soon!")}
            >
              Configure Game
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
