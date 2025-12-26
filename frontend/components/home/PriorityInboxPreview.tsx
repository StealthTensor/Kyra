"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Clock } from "lucide-react";
import { useEmailStore } from "@/store/useEmailStore";

export function PriorityInboxPreview() {
    const { emails, fetchEmails } = useEmailStore();

    useEffect(() => {
        // Ensure we have emails. If category isn't All, we might miss some, 
        // but 'All' usually fetches everything sorted by priority.
        fetchEmails('All');
    }, [fetchEmails]);

    // Filter top 3 urgent/high priority emails
    const highPriorityEmails = emails
        .filter(e => e.score > 50)
        .slice(0, 3);

    if (highPriorityEmails.length === 0) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-3"
        >
            <div className="flex items-center justify-between px-1">
                <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-widest">Priority Inbox</h3>
                <span className="text-xs text-zinc-500">{highPriorityEmails.length} Important</span>
            </div>

            <div className="space-y-3">
                {highPriorityEmails.map((email, index) => (
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
                                        <span className="font-medium text-zinc-100 text-sm truncate max-w-[150px]">{email.from}</span>
                                        {email.score > 80 && (
                                            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">Urgent</span>
                                        )}
                                    </div>
                                    <span className="text-[10px] text-zinc-500 flex items-center gap-1">
                                        <Clock size={10} /> {new Date(email.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                                <h4 className="text-sm font-medium text-zinc-200 mb-1 group-hover:text-white transition-colors truncate">
                                    {email.subject}
                                </h4>
                                <p className="text-xs text-zinc-400 line-clamp-2 leading-relaxed">
                                    {email.labels.includes('Urgent') ? "Marked as Urgent. " : ""}
                                    {email.snippet}
                                </p>
                            </CardContent>
                        </Card>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}
