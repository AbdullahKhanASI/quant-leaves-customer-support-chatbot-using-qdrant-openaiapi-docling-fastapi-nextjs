"use client";

import { useState } from 'react';

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

interface AdminPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AdminPanel({ isOpen, onClose }: AdminPanelProps) {
  const [ingestStatus, setIngestStatus] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    setIngestStatus(null);

    try {
      const response = await fetch(`${backendUrl}/ingest/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail ?? 'Ingestion failed');
      }

      setIngestStatus('Knowledge base refresh queued successfully.');
    } catch (error) {
      console.error('Ingestion refresh failed:', error);
      setIngestStatus(
        error instanceof Error
          ? `Failed: ${error.message}`
          : 'Failed to trigger knowledge base refresh.'
      );
    } finally {
      setIsRefreshing(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-slate-900 border border-slate-700 rounded-lg shadow-xl w-full max-w-md mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <h3 className="text-lg font-semibold text-slate-100">Admin Settings</h3>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-100 transition-colors"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <div>
            <h4 className="text-sm font-medium text-slate-200 mb-2">Knowledge Base Management</h4>
            <p className="text-sm text-slate-400 mb-4">
              Refresh the knowledge base when new documents are added to process PDF or markdown sources.
            </p>

            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="w-full inline-flex items-center justify-center rounded-md bg-emerald-500 px-4 py-2 text-sm font-medium text-emerald-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:bg-emerald-700 disabled:text-emerald-200"
            >
              {isRefreshing ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Refreshing Knowledge Base...
                </>
              ) : (
                'Refresh Knowledge Base'
              )}
            </button>

            {ingestStatus && (
              <div className={`mt-3 p-3 rounded-md text-sm ${
                ingestStatus.includes('Failed') || ingestStatus.includes('failed')
                  ? 'bg-rose-900/60 border border-rose-800 text-rose-200'
                  : 'bg-emerald-900/60 border border-emerald-800 text-emerald-200'
              }`}>
                {ingestStatus}
              </div>
            )}
          </div>

          <div className="border-t border-slate-700 pt-4">
            <h4 className="text-sm font-medium text-slate-200 mb-2">System Information</h4>
            <div className="text-sm text-slate-400 space-y-1">
              <p>Backend URL: {backendUrl}</p>
              <p>Frontend Version: 1.0.0</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-slate-700 px-6 py-3">
          <button
            onClick={onClose}
            className="w-full bg-slate-700 hover:bg-slate-600 text-slate-200 px-4 py-2 rounded-md text-sm transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}