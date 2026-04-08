import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-black flex items-center justify-center p-4 sm:p-8">
      <div className="w-full max-w-5xl h-[85vh]">
        <ChatInterface />
      </div>
    </main>
  );
}
