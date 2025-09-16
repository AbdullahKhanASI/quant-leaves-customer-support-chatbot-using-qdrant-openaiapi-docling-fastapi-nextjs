"use client";

import { useState } from "react";
import ChatContainer from "../components/ChatContainer";
import AdminPanel from "../components/AdminPanel";

export default function Home() {
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [isWidgetOpen, setIsWidgetOpen] = useState(false);

  return (
    <>
      {/* Main Page Content - Demo/Landing */}
      <main className="h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100 flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-500 text-emerald-950 text-2xl font-bold">
              QL
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              QuantLeaves
            </h1>
          </div>

          <h2 className="text-3xl font-semibold text-slate-200">
            AI-Powered Customer Support
          </h2>

          <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Experience intelligent customer support with our advanced RAG-powered chatbot.
            Get instant, accurate answers backed by our comprehensive knowledge base.
          </p>

          <div className="flex gap-4 justify-center pt-8">
            <button
              onClick={() => setIsWidgetOpen(true)}
              className="px-8 py-4 bg-emerald-500 hover:bg-emerald-600 text-emerald-950 font-semibold rounded-lg transition-colors shadow-lg"
            >
              Try the Chat Widget
            </button>

            <button
              onClick={() => setIsAdminOpen(true)}
              className="px-8 py-4 bg-slate-700 hover:bg-slate-600 text-slate-200 font-semibold rounded-lg transition-colors"
            >
              Admin Settings
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12 text-left">
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
              <h3 className="text-lg font-semibold text-emerald-400 mb-2">Intelligent Responses</h3>
              <p className="text-slate-300">Powered by advanced AI and retrieval-augmented generation for accurate, contextual answers.</p>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
              <h3 className="text-lg font-semibold text-cyan-400 mb-2">Real-time Support</h3>
              <p className="text-slate-300">Instant responses with typing indicators and seamless conversation flow.</p>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
              <h3 className="text-lg font-semibold text-purple-400 mb-2">Knowledge Base</h3>
              <p className="text-slate-300">Comprehensive document processing with citations and source references.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Chat Widget */}
      {isWidgetOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-slate-950 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-md h-[600px] flex flex-col overflow-hidden">
            {/* Widget Header */}
            <div className="flex items-center justify-between p-4 border-b border-slate-700 bg-slate-900/60">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500 text-emerald-950 text-sm font-bold">
                  QL
                </div>
                <div>
                  <h3 className="font-semibold text-slate-100">Support Assistant</h3>
                  <p className="text-xs text-slate-400">AI-powered help</p>
                </div>
              </div>

              <button
                onClick={() => setIsWidgetOpen(false)}
                className="p-1 rounded-md hover:bg-slate-700 transition-colors text-slate-400 hover:text-slate-200"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Chat Container */}
            <div className="flex-1 overflow-hidden">
              <ChatContainer />
            </div>
          </div>
        </div>
      )}

      {/* Admin Panel Modal */}
      <AdminPanel
        isOpen={isAdminOpen}
        onClose={() => setIsAdminOpen(false)}
      />
    </>
  );
}
