"use client";

import { useState } from "react";
import { useChatStore } from "@/store/useChatStore";
import { WaveformVisualizer } from "@/components/chat/WaveformVisualizer";
import { QuickActions } from "@/components/chat/QuickActions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Mic, Send, Paperclip } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function ChatPage() {
    const { messages, isLoading, sendMessage } = useChatStore();
    const [input, setInput] = useState("");

    const handleSend = () => {
        if (!input.trim()) return;
        sendMessage(input);
        setInput("");
    };

    return (
        <div className="flex flex-col h-full bg-zinc-950 pt-10">
            {/* Visualizer Area */}
            <div className="relative h-1/3 flex flex-col items-center justify-end pb-8">
                <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 to-purple-300 mb-2">
                    Kyra's Brain
                </h1>
                <WaveformVisualizer />
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-hidden flex flex-col bg-zinc-900/40 rounded-t-3xl border-t border-zinc-800">

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.map((msg) => (
                        <motion.div
                            key={msg.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-none'
                                : 'bg-zinc-800 text-zinc-200 rounded-bl-none'
                                }`}>
                                {msg.content}
                                {msg.role === 'assistant' && msg.reasoning && (
                                    <div className="mt-2 text-xs text-indigo-300 border-t border-zinc-700/50 pt-2">
                                        🧠 {msg.reasoning}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Quick Actions & Input */}
                <div className="p-4 bg-zinc-900/80 backdrop-blur-lg border-t border-zinc-800 pb-[calc(1rem+env(safe-area-inset-bottom))]">
                    <QuickActions onAction={(text) => setInput(text)} />

                    <div className="flex gap-2 items-center">
                        <button className="text-zinc-400 p-2 hover:text-white transition-colors">
                            <Paperclip size={20} />
                        </button>
                        <Input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask Kyra..."
                            className="flex-1 bg-zinc-800/50 border-zinc-700 text-white rounded-full h-12 px-4 focus-visible:ring-indigo-500"
                            onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        />
                        {input.trim() ? (
                            <Button onClick={handleSend} size="icon" className="rounded-full h-12 w-12 bg-indigo-600 hover:bg-indigo-500">
                                <Send size={20} />
                            </Button>
                        ) : (
                            <Button size="icon" className="rounded-full h-12 w-12 bg-zinc-800 hover:bg-zinc-700">
                                <Mic size={20} />
                            </Button>
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
}
