# QuantLeaves Support Assistant - Frontend

A modern Next.js frontend for the QuantLeaves customer support chatbot using RAG technology.

## Features

- 🤖 **Conversational Chat Interface** - Real-time messaging with typing indicators
- 📚 **RAG Integration** - Displays citations and structured results from the backend
- ⚙️ **Admin Panel** - Knowledge base refresh functionality
- 🎨 **Modern UI** - Dark theme with Tailwind CSS
- 📱 **Responsive Design** - Works on desktop and mobile
- 🔧 **Error Handling** - Comprehensive error boundaries and user feedback

## Tech Stack

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **React 19** - UI library

## Getting Started

First, run the development server:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the chatbot interface.

## Environment Variables

Create a `.env.local` file with:

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── layout.tsx      # Root layout with error boundary
│   ├── page.tsx        # Main chat page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── ChatContainer.tsx    # Main chat interface
│   ├── ChatMessage.tsx      # Individual message component
│   ├── ChatInput.tsx        # Message input with auto-resize
│   ├── TypingIndicator.tsx  # AI typing animation
│   ├── AdminPanel.tsx       # Settings modal
│   └── ErrorBoundary.tsx    # Error handling
└── types/              # TypeScript type definitions
    └── chat.ts         # Chat-related types
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
