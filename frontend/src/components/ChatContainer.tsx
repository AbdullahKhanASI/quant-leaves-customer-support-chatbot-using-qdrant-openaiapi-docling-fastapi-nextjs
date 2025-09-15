"use client";

import { useEffect, useRef, useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';
import { ChatMessage as ChatMessageType, ChatResponse, ChatError } from '../types/chat';

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export default function ChatContainer() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<ChatError | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    // Add welcome message
    const welcomeMessage: ChatMessageType = {
      id: 'welcome',
      type: 'assistant',
      content: 'Hello! I\'m your QuantLeaves support assistant. I can help you with questions about our products, policies, and troubleshooting. What can I help you with today?',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const generateMessageId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const handleSendMessage = async (content: string) => {
    const userMessage: ChatMessageType = {
      id: generateMessageId(),
      type: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    setError(null);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: content }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
      }

      const data: ChatResponse = await response.json();

      const assistantMessage: ChatMessageType = {
        id: generateMessageId(),
        type: 'assistant',
        content: data.answer,
        citations: data.citations,
        structuredResults: data.structured_results,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat request failed:', error);

      const errorMessage: ChatError = {
        message: error instanceof Error ? error.message : 'Unable to process your request right now.',
        type: error instanceof Error && error.message.includes('Backend returned') ? 'server' : 'network'
      };

      setError(errorMessage);

      const errorResponseMessage: ChatMessageType = {
        id: generateMessageId(),
        type: 'assistant',
        content: `I'm sorry, I encountered an error: ${errorMessage.message}. Please try again or contact support if the issue persists.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorResponseMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const clearError = () => setError(null);

  return (
    <div className="flex h-full flex-col">
      {/* Chat Header */}
      <div className="border-b border-slate-700 bg-slate-800/60 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-emerald-950 text-sm font-bold">
            QL
          </div>
          <div>
            <h2 className="font-semibold text-slate-100">QuantLeaves Support</h2>
            <p className="text-sm text-slate-400">AI-powered assistance</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        <div className="space-y-6">
          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              type={message.type}
              content={message.content}
              citations={message.citations}
              structuredResults={message.structuredResults}
              timestamp={message.timestamp}
            />
          ))}

          {isTyping && <TypingIndicator />}

          <div ref={chatEndRef} />
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="border-t border-rose-800 bg-rose-900/60 px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 rounded-full bg-rose-500" />
              <span className="text-sm text-rose-200">{error.message}</span>
            </div>
            <button
              onClick={clearError}
              className="text-rose-300 hover:text-rose-100 transition-colors"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-slate-700 bg-slate-800/60 px-6 py-4">
        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isTyping}
          placeholder="Ask me anything about QuantLeaves..."
        />
      </div>
    </div>
  );
}