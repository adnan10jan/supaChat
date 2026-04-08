"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2, Database, AlertCircle } from 'lucide-react';
import VisualGraph from './VisualGraph';
import ResultsTable from './ResultsTable';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    data?: any[];
    error?: string;
    suggested_sql?: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const res = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg.content }),
            });

            const data = await res.json();

            const assistantMsg: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.text || "Here are your results.",
                data: data.table && data.table.length > 0 ? data.table : undefined,
                suggested_sql: data.suggested_sql
            };

            setMessages(prev => [...prev, assistantMsg]);
        } catch (error: any) {
            setMessages(prev => [...prev, {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: "I encountered an error connecting to the backend server.",
                error: error.message
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-gray-950 text-gray-100 font-sans shadow-2xl rounded-2xl overflow-hidden border border-gray-800">
            {/* Header */}
            <header className="bg-gray-900 border-b border-gray-800 p-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
                        <Database className="w-4 h-4 text-white" />
                    </div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                        SupaChat
                    </h1>
                </div>
                <span className="text-xs px-2 py-1 bg-gray-800 rounded-full text-gray-400 border border-gray-700">Analytics AI</span>
            </header>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-4">
                        <Database className="w-16 h-16 opacity-20" />
                        <p className="text-lg">Ask me anything about your blog analytics.</p>
                        <div className="flex flex-wrap gap-2 justify-center max-w-md">
                            {['Show top trending topics in last 30 days', 'Plot daily views trend for AI articles'].map(q => (
                                <button key={q} onClick={() => setInput(q)}
                                    className="text-xs bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded-full transition-colors">
                                    "{q}"
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-sm'
                                : 'bg-gray-900 border border-gray-800 rounded-bl-sm'
                            }`}>
                            <p className="text-sm md:text-base leading-relaxed">{msg.content}</p>

                            {msg.suggested_sql && (
                                <div className="mt-3 p-2 bg-gray-950 rounded border border-gray-800">
                                    <code className="text-xs text-green-400 font-mono">{msg.suggested_sql}</code>
                                </div>
                            )}

                            {msg.error && (
                                <div className="mt-3 flex items-center gap-2 text-red-400 text-sm p-3 bg-red-950/30 rounded border border-red-900/50">
                                    <AlertCircle className="w-4 h-4" />
                                    <span>{msg.error}</span>
                                </div>
                            )}

                            {msg.data && (
                                <div className="mt-4 space-y-4">
                                    <ResultsTable data={msg.data} />
                                    <VisualGraph data={msg.data} />
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-900 border border-gray-800 rounded-2xl rounded-bl-sm p-4 flex items-center gap-3">
                            <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
                            <span className="text-gray-400 text-sm">Querying database...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-gray-900 border-t border-gray-800">
                <form onSubmit={handleSubmit} className="relative flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about your analytics... e.g., 'Compare article engagement by topic'"
                        className="w-full bg-gray-950 border border-gray-800 rounded-full py-3 px-5 pr-12 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 rounded-full text-white transition-colors"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </form>
            </div>
        </div>
    );
}
