"use client"

import * as React from "react"
import { Send, User, Bot, Loader2 } from "lucide-react"
import axios from "axios"
import { cn } from "@/lib/utils"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

type Message = {
    id: string
    role: "user" | "assistant"
    content: string
}

import { CalendarWidget } from "@/components/calendar-widget"

export function ChatInterface() {
    // ... items ...
    const [messages, setMessages] = React.useState<Message[]>([])
    // ... existing state ...
    const [input, setInput] = React.useState("")
    const [isLoading, setIsLoading] = React.useState(false)
    const [conversationId, setConversationId] = React.useState<string | null>(null)
    const scrollRef = React.useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        if (scrollRef.current) {
            const scrollAreaViewport = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
            if (scrollAreaViewport) {
                scrollAreaViewport.scrollTop = scrollAreaViewport.scrollHeight;
            }
        }
    }

    React.useEffect(() => { scrollToBottom() }, [messages])

    const handleSend = async () => {
        // ... existing handleSend logic ...
        if (!input.trim() || isLoading) return
        const userMsg: Message = { id: Date.now().toString(), role: "user", content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setIsLoading(true)
        try {
            const response = await axios.post("http://localhost:8000/api/v1/chat/", {
                query: userMsg.content,
                user_id: conversationId ? undefined : "default_user",
                conversation_id: conversationId
            })
            const data = response.data
            if (data.conversation_id) setConversationId(data.conversation_id)
            setMessages(prev => [...prev, { id: Date.now().toString() + "_ai", role: "assistant", content: data.response }])
        } catch (e) {
            console.error(e)
            setMessages(prev => [...prev, { id: Date.now().toString() + "_err", role: "assistant", content: "Error." }])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <Card className="w-full max-w-5xl h-[600px] flex bg-background border-border shadow-2xl overflow-hidden">
            {/* Left: Chat Area */}
            <div className="flex-1 flex flex-col h-full">
                <CardHeader className="border-b py-3">
                    <CardTitle className="flex items-center gap-2 text-base">
                        <Bot className="w-5 h-5 text-indigo-500" />
                        Kyra Intelligence
                    </CardTitle>
                </CardHeader>

                <div className="flex-1 overflow-hidden p-4 bg-zinc-950/30">
                    <ScrollArea className="h-full pr-4" ref={scrollRef}>
                        <div className="flex flex-col gap-6 pb-4">
                            {messages.length === 0 && (
                                <div className="text-center text-muted-foreground mt-32 space-y-2">
                                    <Bot className="w-12 h-12 mx-auto text-zinc-700 mb-4" />
                                    <p className="font-medium text-zinc-400">Ready to organize your day.</p>
                                    <p className="text-xs text-zinc-600">Try "What's my schedule?" or "Draft an email"</p>
                                </div>
                            )}

                            {messages.map((msg) => (
                                <div key={msg.id} className={cn("flex gap-3 text-sm max-w-[85%]", msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto")}>
                                    <div className={cn("w-8 h-8 rounded-full flex items-center justify-center shrink-0 border border-zinc-700", msg.role === "user" ? "bg-zinc-800" : "bg-indigo-950/30")}>
                                        {msg.role === "user" ? <User className="w-4 h-4 text-zinc-400" /> : <Bot className="w-4 h-4 text-indigo-400" />}
                                    </div>
                                    <div className={cn("p-3 rounded-2xl whitespace-pre-wrap leading-relaxed shadow-sm", msg.role === "user" ? "bg-zinc-800 text-zinc-100 rounded-tr-sm" : "bg-black/40 border border-zinc-800 text-zinc-300 rounded-tl-sm")}>
                                        {msg.content}
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex gap-3 mr-auto max-w-[85%]">
                                    <div className="w-8 h-8 rounded-full bg-indigo-950/30 border border-zinc-700 flex items-center justify-center shrink-0">
                                        <Bot className="w-4 h-4 text-indigo-400" />
                                    </div>
                                    <div className="flex items-center gap-2 text-zinc-500 text-sm pl-2">
                                        <Loader2 className="w-3 h-3 animate-spin" />
                                        Kyra is thinking...
                                    </div>
                                </div>
                            )}
                        </div>
                    </ScrollArea>
                </div>

                <div className="p-4 border-t bg-zinc-950/50">
                    <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-2 relative">
                        <Input
                            placeholder="Ask Kyra..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={isLoading}
                            className="flex-1 bg-zinc-900 border-zinc-800 focus-visible:ring-indigo-500/50 pl-4 h-11"
                        />
                        <Button type="submit" size="icon" disabled={isLoading || !input.trim()} className="h-11 w-11 bg-indigo-600 hover:bg-indigo-700 text-white">
                            <Send className="w-4 h-4" />
                        </Button>
                    </form>
                </div>
            </div>

            {/* Right: Calendar Widget (Hidden on mobile ideally, visible on md+) */}
            <div className="hidden md:block w-72 h-full">
                <CalendarWidget />
            </div>
        </Card>
    )
}
