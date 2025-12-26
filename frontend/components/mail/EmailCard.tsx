"use client";

import { motion, useMotionValue, useTransform, PanInfo } from "framer-motion";
import { Archive, Reply, MoreHorizontal } from "lucide-react";
import { useState, useMemo } from "react";

interface Email {
    id: string | number;
    subject: string;
    sender: string;
    from?: string;
    preview?: string;
    snippet?: string;
    time?: string;
    timestamp?: string;
    type?: string;
    thread_summary?: string;
    summary?: string;
    isRead?: boolean;
    labels?: string[];
    score?: number;
}

interface EmailCardProps {
    email: any;
    onOpen: (email: any) => void;
    onArchive: (id: string) => void;
    onReply: (id: string) => void;
}

function getInitials(name: string): string {
    const parts = name.split(/[<@]/);
    const firstPart = parts[0]?.trim() || "";
    if (firstPart.includes(" ")) {
        return firstPart
            .split(" ")
            .map(n => n[0])
            .join("")
            .toUpperCase()
            .slice(0, 2);
    }
    return firstPart.slice(0, 2).toUpperCase();
}

function formatRelativeTime(timestamp: string | undefined): string {
    if (!timestamp) return "";
    
    try {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / (1000 * 60));
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        if (diffMins < 1) return "Just now";
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays === 1) return "Yesterday";
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    } catch {
        return timestamp;
    }
}

export function EmailCard({ email, onOpen, onArchive, onReply }: EmailCardProps) {
    const x = useMotionValue(0);
    const background = useTransform(x, [-100, 0, 100], ["#ef4444", "#18181b", "#3b82f6"]);
    const [swiped, setSwiped] = useState(false);

    const handleDragEnd = (_: any, info: PanInfo) => {
        if (info.offset.x < -100) {
            onArchive(email.id);
            setSwiped(true);
        } else if (info.offset.x > 100) {
            onReply(email.id);
            setSwiped(true);
        }
    };

    const senderName = email.sender || email.from || "Unknown";
    const initials = useMemo(() => getInitials(senderName), [senderName]);
    const isUnread = !email.isRead;
    const isUrgent = (email.score || 0) > 80;
    const timeDisplay = formatRelativeTime(email.timestamp || email.time);
    const category = email.labels?.[0] || "";

    if (swiped) return null;

    return (
        <div className="relative mb-2 overflow-hidden rounded-xl">
            <motion.div
                style={{ background }}
                className="absolute inset-0 flex items-center justify-between px-6"
            >
                <Reply className="text-white" />
                <Archive className="text-white" />
            </motion.div>

            <motion.div
                drag="x"
                dragConstraints={{ left: 0, right: 0 }}
                style={{ x }}
                onDragEnd={handleDragEnd}
                onClick={() => onOpen(email)}
                className={`relative p-4 rounded-xl z-10 cursor-pointer active:cursor-grabbing transition-colors ${
                    isUnread 
                        ? "bg-zinc-900 border-l-4 border-l-blue-500" 
                        : "bg-zinc-900/60 border border-zinc-800"
                }`}
                whileTap={{ scale: 0.98 }}
            >
                <div className="flex gap-3 items-start">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 font-semibold text-sm ${
                        isUrgent ? "bg-red-500" : "bg-gradient-to-br from-blue-500 to-purple-600"
                    }`}>
                        {initials}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                        <div className="flex justify-between items-start mb-1 gap-2">
                            <div className="flex items-center gap-2 flex-1 min-w-0">
                                <h4 className={`font-semibold text-sm truncate ${isUnread ? "text-white" : "text-zinc-300"}`}>
                                    {senderName}
                                </h4>
                                {!isUnread && (
                                    <div className="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0" />
                                )}
                                {isUrgent && (
                                    <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 shrink-0">
                                        Urgent
                                    </span>
                                )}
                                {category && category !== "All" && (
                                    <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-zinc-800 text-zinc-400 shrink-0">
                                        {category}
                                    </span>
                                )}
                            </div>
                            <span className="text-xs text-zinc-500 shrink-0">{timeDisplay}</span>
                        </div>
                        
                        <h5 className={`text-sm font-medium mb-1.5 line-clamp-1 ${isUnread ? "text-zinc-100" : "text-zinc-400"}`}>
                            {email.subject || "(No Subject)"}
                        </h5>
                        
                        <div className="text-xs text-zinc-400 line-clamp-2 leading-relaxed">
                            {(email.thread_summary || email.summary) ? (
                                <span className="text-indigo-300">✨ {email.thread_summary || email.summary}</span>
                            ) : (
                                email.preview || email.snippet || ""
                            )}
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
