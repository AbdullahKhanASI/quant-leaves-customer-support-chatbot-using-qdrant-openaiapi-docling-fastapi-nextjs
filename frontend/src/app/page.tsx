"use client";

import { useState } from "react";
import ChatContainer from "../components/ChatContainer";
import AdminPanel from "../components/AdminPanel";

export default function Home() {
  const [isAdminOpen, setIsAdminOpen] = useState(false);

  return (
    <main className="h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Navigation */}
      <nav className="border-b border-slate-700 bg-slate-900/60 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500 text-emerald-950 text-sm font-bold">
              QL
            </div>
            <div>
              <h1 className="text-xl font-semibold">QuantLeaves Support Assistant</h1>
              <p className="text-sm text-slate-400">AI-powered customer support</p>
            </div>
          </div>

          <button
            onClick={() => setIsAdminOpen(true)}
            className="flex items-center gap-2 rounded-md bg-slate-700 px-3 py-2 text-sm text-slate-200 transition hover:bg-slate-600"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Settings
          </button>
        </div>
      </nav>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden">
        <ChatContainer />
      </div>

      {/* Admin Panel Modal */}
      <AdminPanel
        isOpen={isAdminOpen}
        onClose={() => setIsAdminOpen(false)}
      />
    </main>
  );
}
