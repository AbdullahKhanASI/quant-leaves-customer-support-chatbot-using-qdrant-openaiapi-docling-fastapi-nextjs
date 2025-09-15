export default function TypingIndicator() {
  return (
    <div className="flex gap-3 justify-start">
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500 text-emerald-950 text-sm font-medium">
        AI
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
        </div>
      </div>
    </div>
  );
}