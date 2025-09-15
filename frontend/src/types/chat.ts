export interface Citation {
  doc_id: string;
  snippet: string;
  metadata?: Record<string, unknown> | null;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
  structured_results: Record<string, unknown>[];
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  structuredResults?: Record<string, unknown>[];
  timestamp: Date;
}

export interface ChatError {
  message: string;
  type: 'network' | 'server' | 'validation' | 'unknown';
}