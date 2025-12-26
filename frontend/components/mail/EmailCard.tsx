"use client";

import { motion, useMotionValue, useTransform, PanInfo } from "framer-motion";
import { Archive, Reply, MoreHorizontal } from "lucide-react";
import { useState } from "react";

interface Email {
    id: string | number;
    subject: string;
    sender: string;
    preview?: string; // or snippet
    snippet?: string;
    time?: string;
    timestamp?: string; // allow either
    type?: string;
    thread_summary?: string;
    summary?: string; // store uses summary
}

interface EmailCardProps {
    email: any; // Relaxed type to support both Store and Mock for now, or unified.
    onOpen: (email: any) => void;
    onArchive: (id: string | number) => void;
    onReply: (id: string | number) => void;
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
            setSwiped(true); // Ideally reset or nav away
        }
    };

    if (swiped) return null; // Animate out in real app

    return (
        <div className="relative mb-2 overflow-hidden rounded-xl">
            {/* Background Actions */}
            <motion.div
                style={{ background }}
                className="absolute inset-0 flex items-center justify-between px-6"
            >
                <Reply className="text-white" />
                <Archive className="text-white" />
            </motion.div>

            {/* Card Content */}
            <motion.div
                drag="x"
                dragConstraints={{ left: 0, right: 0 }}
                style={{ x }}
                onDragEnd={handleDragEnd}
                onClick={() => onOpen(email)}
                className="relative bg-zinc-900 border border-zinc-800 p-4 rounded-xl z-10 cursor-pointer active:cursor-grabbing"
                whileTap={{ scale: 0.98 }}
            >
                <div className="flex justify-between items-start mb-1">
                    <h4 className="font-semibold text-zinc-200 text-sm">{email.sender || email.from}</h4>
                    <span className="text-xs text-zinc-500">{email.time || (email.timestamp ? new Date(email.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '')}</span>
                </div>
                <h5 className="text-sm font-medium text-zinc-300 mb-1">{email.subject}</h5>
                <div className="text-xs text-zinc-400 line-clamp-2">
                    {(email.thread_summary || email.summary) ? (
                        <span className="text-indigo-300">✨ {email.thread_summary || email.summary}</span>
                    ) : (
                        email.preview || email.snippet
                    )}
                </div>
            </motion.div >
        </div >
    );
}
