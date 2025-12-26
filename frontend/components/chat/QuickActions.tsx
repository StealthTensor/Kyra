"use client";

import { motion } from "framer-motion";
import { Sparkles, Search, CheckCircle } from "lucide-react";

interface QuickActionsProps {
    onAction: (text: string) => void;
}

export function QuickActions({ onAction }: QuickActionsProps) {
    const actions = [
        { icon: Sparkles, text: "Summarize today", color: "bg-purple-500/10 text-purple-400 border-purple-500/20" },
        { icon: Search, text: "Find lab manual", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
        { icon: CheckCircle, text: "Check conflicts", color: "bg-green-500/10 text-green-400 border-green-500/20" },
    ];

    return (
        <div className="flex gap-2 pb-4 overflow-x-auto no-scrollbar px-1">
            {actions.map((action, index) => (
                <motion.button
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    onClick={() => onAction(action.text)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-full border text-xs font-medium whitespace-nowrap transition-transform active:scale-95 ${action.color}`}
                >
                    <action.icon size={14} />
                    {action.text}
                </motion.button>
            ))}
        </div>
    );
}
