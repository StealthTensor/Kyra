"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, CornerUpLeft, Trash2, MoreVertical } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Email {
    id: number;
    subject: string;
    sender: string;
    preview: string;
    time: string;
    thread_summary?: string;
    full_body?: string;
    why_here?: string;
}

interface EmailDetailDrawerProps {
    email: Email | null;
    onClose: () => void;
}

export function EmailDetailDrawer({ email, onClose }: EmailDetailDrawerProps) {
    if (!email) return null;

    return (
        <AnimatePresence>
            {email && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/60 z-50 backdrop-blur-sm"
                    />

                    {/* Drawer */}
                    <motion.div
                        initial={{ y: "100%" }}
                        animate={{ y: 0 }}
                        exit={{ y: "100%" }}
                        transition={{ type: "spring", damping: 25, stiffness: 300 }}
                        className="fixed bottom-0 left-0 right-0 h-[85vh] bg-zinc-900 rounded-t-3xl z-50 overflow-hidden flex flex-col border-t border-zinc-800"
                    >
                        {/* Handle */}
                        <div className="w-full flex justify-center pt-3 pb-1" onClick={onClose}>
                            <div className="w-12 h-1.5 bg-zinc-700 rounded-full" />
                        </div>

                        {/* Header */}
                        <div className="px-5 py-4 border-b border-zinc-800 flex justify-between items-start">
                            <div>
                                <h2 className="text-lg font-bold text-white leading-tight">{email.subject}</h2>
                                <p className="text-sm text-zinc-400 mt-1">{email.sender} • {email.time}</p>
                            </div>
                            <div className="flex gap-2">
                                <button className="p-2 rounded-full bg-zinc-800 text-zinc-400 hover:text-white">
                                    <MoreVertical size={20} />
                                </button>
                            </div>
                        </div>

                        {/* Content */}
                        <div className="flex-1 overflow-y-auto p-5 space-y-6">
                            {/* Why is this here? */}
                            <div className="bg-indigo-900/20 border border-indigo-500/30 p-3 rounded-lg">
                                <h3 className="text-xs font-semibold text-indigo-400 uppercase tracking-wide mb-1">Why is this here?</h3>
                                <p className="text-sm text-indigo-200 leading-relaxed">
                                    {email.why_here || "Detected as high priority based on deadline keywords."}
                                </p>
                            </div>

                            {/* Email Body */}
                            <div className="text-zinc-300 text-sm leading-relaxed space-y-4">
                                {/* Placeholder for body content split by paragraphs */}
                                <p>{email.thread_summary || email.preview}</p>
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.</p>
                                <p>Best regards,</p>
                                <p>{email.sender}</p>
                            </div>
                        </div>

                        {/* Bottom Actions */}
                        <div className="p-4 border-t border-zinc-800 bg-zinc-900 pb-[env(safe-area-inset-bottom)]">
                            <div className="flex gap-3">
                                <button className="flex-1 bg-white text-black py-3 rounded-xl font-medium text-sm flex items-center justify-center gap-2">
                                    <CornerUpLeft size={18} /> Reply
                                </button>
                                <button className="flex-1 bg-zinc-800 text-white py-3 rounded-xl font-medium text-sm flex items-center justify-center gap-2">
                                    <Trash2 size={18} /> Archive
                                </button>
                            </div>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
