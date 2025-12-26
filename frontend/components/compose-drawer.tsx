"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { X, Wand2, Send } from "lucide-react"
import axios from "axios"

export function ComposeDrawer({ isOpen, onClose, defaultThreadId, defaultEmail, defaultSubject }: { isOpen: boolean, onClose: () => void, defaultThreadId?: string, defaultEmail?: string, defaultSubject?: string }) {
    const [recipient, setRecipient] = useState("")
    const [subject, setSubject] = useState("")
    const [body, setBody] = useState("")
    const [loading, setLoading] = useState(false)

    // Prompting for draft
    const [promptMode, setPromptMode] = useState(false)
    const [prompt, setPrompt] = useState("")

    useEffect(() => {
        if (isOpen) {
            if (defaultEmail) setRecipient(defaultEmail)
            if (defaultSubject) setSubject(defaultSubject.startsWith("Re:") ? defaultSubject : "Re: " + defaultSubject)
        }
    }, [isOpen, defaultEmail, defaultSubject])

    if (!isOpen) return null;

    const handleDraft = async () => {
        setLoading(true)
        try {
            const userEmail = localStorage.getItem("user_email") || "me" // Fallback

            const res = await axios.post("http://localhost:8000/api/v1/gmail/draft", {
                thread_id: defaultThreadId,
                prompt: prompt,
                tone: "Professional",
                email_address: userEmail
            })
            setBody(res.data.draft_body)
            setPromptMode(false)
        } catch (e) {
            console.error(e)
            alert("Failed to draft")
        } finally {
            setLoading(false)
        }
    }

    const handleSend = async () => {
        setLoading(true)
        try {
            const userEmail = localStorage.getItem("user_email") || "me"

            await axios.post("http://localhost:8000/api/v1/gmail/send", {
                email_address: userEmail,
                recipient,
                subject,
                body,
                thread_id: defaultThreadId
            })
            alert("Sent!")
            onClose()
        } catch (e) {
            console.error(e)
            alert("Failed to send")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed bottom-4 right-4 z-50 w-[500px] shadow-2xl animate-in slide-in-from-bottom-10 fade-in duration-300">
            <Card className="border-zinc-800 bg-zinc-950 text-zinc-50 shadow-2xl">
                <CardHeader className="flex flex-row items-center justify-between py-3 border-b border-zinc-900">
                    <CardTitle className="text-sm font-medium">Compose via Kyra</CardTitle>
                    <Button variant="ghost" size="icon" onClick={onClose} className="h-6 w-6 text-zinc-400 hover:text-white hover:bg-zinc-800">
                        <X className="h-4 w-4" />
                    </Button>
                </CardHeader>
                <CardContent className="space-y-3 py-4">
                    <div className="space-y-1">
                        <Input
                            placeholder="To"
                            value={recipient}
                            onChange={e => setRecipient(e.target.value)}
                            className="bg-zinc-900 border-zinc-800 focus-visible:ring-zinc-700 text-zinc-200"
                        />
                    </div>
                    <div className="space-y-1">
                        <Input
                            placeholder="Subject"
                            value={subject}
                            onChange={e => setSubject(e.target.value)}
                            className="bg-zinc-900 border-zinc-800 focus-visible:ring-zinc-700 text-zinc-200"
                        />
                    </div>

                    {promptMode ? (
                        <div className="space-y-2 rounded-md bg-zinc-900/50 p-3 border border-zinc-800">
                            <div className="flex items-center gap-2 mb-2">
                                <Wand2 className="h-3 w-3 text-purple-400" />
                                <p className="text-xs text-zinc-400 font-medium">Describe your reply...</p>
                            </div>
                            <Textarea
                                value={prompt}
                                onChange={e => setPrompt(e.target.value)}
                                className="bg-zinc-950 border-zinc-800 min-h-[80px]"
                                placeholder="e.g. Tell them I'll be 10 mins late due to traffic"
                                autoFocus
                            />
                            <div className="flex justify-end gap-2 pt-2">
                                <Button variant="ghost" size="sm" onClick={() => setPromptMode(false)} className="text-zinc-400 hover:text-white">Cancel</Button>
                                <Button size="sm" onClick={handleDraft} disabled={loading} className="bg-purple-600 hover:bg-purple-700 text-white border-0">
                                    {loading ? "Thinking..." : "Generate Draft"}
                                </Button>
                            </div>
                        </div>
                    ) : (
                        <Textarea
                            value={body}
                            onChange={e => setBody(e.target.value)}
                            className="min-h-[300px] bg-zinc-900 border-zinc-800 focus-visible:ring-zinc-700 font-mono text-sm leading-relaxed text-zinc-300"
                            placeholder="Type your message..."
                        />
                    )}
                </CardContent>
                <CardFooter className="justify-between py-3 border-t border-zinc-900">
                    <Button variant="outline" size="sm" onClick={() => setPromptMode(true)} className="border-zinc-800 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white">
                        <Wand2 className="mr-2 h-4 w-4" />
                        Kyra Draft
                    </Button>
                    <Button size="sm" onClick={handleSend} disabled={loading || !body} className="bg-white text-black hover:bg-zinc-200 font-medium">
                        <Send className="mr-2 h-4 w-4" />
                        {loading ? "Sending..." : "Send Email"}
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}
