import { Citation } from '../types/chat';

interface ChatMessageProps {
  type: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  structuredResults?: Record<string, unknown>[];
  timestamp: Date;
}

export default function ChatMessage({
  type,
  content,
  citations = [],
  structuredResults = [],
  timestamp
}: ChatMessageProps) {
  const isUser = type === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500 text-emerald-950 text-sm font-medium">
          AI
        </div>
      )}

      <div className={`max-w-[70%] ${isUser ? 'order-first' : ''}`}>
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-emerald-500 text-emerald-950'
              : 'bg-slate-800 text-slate-100 border border-slate-700'
          }`}
        >
          <p className="whitespace-pre-line text-sm leading-relaxed">{content}</p>
        </div>

        <div className="mt-1 text-xs text-slate-400">
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>

        {/* Citations */}
        {citations.length > 0 && (
          <div className="mt-3">
            <h4 className="text-xs font-medium text-emerald-300 mb-2">Sources</h4>
            <div className="space-y-2">
              {citations.map((citation) => (
                <div
                  key={citation.doc_id}
                  className="rounded-md border border-slate-700 bg-slate-900/60 p-2 text-xs"
                >
                  <p className="font-medium text-slate-200 mb-1">[{citation.doc_id}]</p>
                  <p className="text-slate-300 leading-relaxed">{citation.snippet}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Structured Results */}
        {structuredResults.length > 0 && (
          <div className="mt-3">
            <h4 className="text-xs font-medium text-emerald-300 mb-2">Structured Data</h4>
            <div className="space-y-2">
              {structuredResults.map((item, index) => (
                <div
                  key={index}
                  className="rounded-md border border-slate-700 bg-slate-900/60 p-2"
                >
                  <pre className="whitespace-pre-wrap break-words text-xs text-slate-300">
                    {JSON.stringify(item, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-600 text-slate-100 text-sm font-medium">
          U
        </div>
      )}
    </div>
  );
}