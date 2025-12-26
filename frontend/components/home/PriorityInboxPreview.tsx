"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Mail, Clock } from "lucide-react";

export function PriorityInboxPreview() {
    // Mock data for now
    const emails = [
        { id: 1, subject: "Urgent: Server Downtime", sender: "DevOps", time: "10m ago", summary: "Production server is down. API returning 500 errors. Team investigating." },
        { id: 2, subject: "Invoice #3492 Pending", sender: "Finance", time: "1h ago", summary: "Payment overdue forAWS. Please approve immediately to avoid service interruption." },
        { id: 3, subject: "Client Meeting Reschedule", sender: "Sarah J.", time: "2h ago", summary: "Can we move the 3 PM call to 4 PM? Something came up." },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-3"
        >
            <div className="flex items-center justify-between px-1">
                <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-widest">Priority Inbox</h3>
                <span className="text-xs text-zinc-500">3 Urgent</span>
            </div>

            <div className="space-y-3">
                {emails.map((email, index) => (
                    <motion.div
                        key={email.id}
                        initial={{ opacity: 0, x: 10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + index * 0.1 }}
                    >
                        <Card className="bg-zinc-900/60 border-zinc-800 hover:bg-zinc-800/80 transition-colors cursor-pointer group">
                            <CardContent className="p-4">
                                <div className="flex justify-between items-start mb-1">
                                    <div className="flex items-center gap-2">
                                        <span className="font-medium text-zinc-100 text-sm">{email.sender}</span>
                                        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">Urgent</span>
                                    </div>
                                    <span className="text-[10px] text-zinc-500 flex items-center gap-1">
                                        <Clock size={10} /> {email.time}
                                    </span>
                                </div>
                                <h4 className="text-sm font-medium text-zinc-200 mb-1 group-hover:text-white transition-colors">
                                    {email.subject}
                                </h4>
                                <p className="text-xs text-zinc-400 line-clamp-2 leading-relaxed">
                                    {email.summary}
                                </p>
                            </CardContent>
                        </Card>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}
