'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function CreateProjectPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Use env variable or fallback
  const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";
  // Determine base API URL (remove /events suffix if present from previous config)
  const BASE_API_URL = rawApiUrl.replace(/\/events\/?$/, "");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an Excel file first.');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${BASE_API_URL}/projects/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const projectId = response.data.project_id;
      // Redirect to dashboard or config page
      // Using existing dashboard path for now
      router.push(`/events/${projectId}/dashboard`);

    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Error uploading file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700">
        <h1 className="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
          Cluedo Maker
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Upload your participants list (Excel) to start a new mystery.
        </p>

        {/* Upload Area */}
        <div className="mb-6">
          <label className="block mb-2 text-sm font-medium text-gray-300">
            Select Excel File (.xlsx)
          </label>
          <input
            type="file"
            accept=".xlsx, .xls"
            onChange={handleFileChange}
            disabled={isLoading}
            className="block w-full text-sm text-gray-400
              file:mr-4 file:py-2.5 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-purple-600 file:text-white
              hover:file:bg-purple-700
              cursor-pointer bg-gray-700 rounded-lg border border-gray-600"
          />
          <p className="mt-2 text-xs text-gray-500">
            Expected columns: Name, Email (optimal), Notes (optional)
          </p>
        </div>

        {error && (
          <div className="mb-6 p-3 bg-red-900/50 border border-red-500 rounded text-red-200 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || isLoading}
          className={`w-full py-3 px-4 rounded-lg font-bold text-lg transition-all duration-200
            ${!file || isLoading
              ? 'bg-gray-600 cursor-not-allowed text-gray-400'
              : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white shadow-lg hover:shadow-purple-500/25'
            }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Parsing & Creating Project...
            </span>
          ) : (
            'Upload & Create Project'
          )}
        </button>
      </div>
    </div>
  );
}
