"use client";

import { motion } from "framer-motion";
import { format } from "date-fns";
import { Calendar, CheckCircle2, Clock, AlertTriangle } from "lucide-react";

interface TimelineItem {
    id: number;
    title: string;
    time: string;
    type: "event" | "task";
    status: "pending" | "completed" | "conflict";
    conflictReason?: string;
    duration?: string; // for events
}

export default function TimelinePage() {
    // Mock Data - mixed tasks and events
    const timelineItems: TimelineItem[] = [
        { id: 1, title: "Morning Standup", time: "10:00 AM", type: "event", duration: "30m", status: "completed" },
        { id: 2, title: "Review PR #402", time: "10:30 AM", type: "task", status: "pending" },
        { id: 3, title: "Lunch with Sarah", time: "12:00 PM", type: "event", duration: "1h", status: "pending" },
        { id: 4, title: "Submit Project Titan", time: "02:00 PM", type: "task", status: "conflict", conflictReason: "Overlaps with Lab Meeting" },
        { id: 5, title: "Lab Meeting", time: "02:00 PM", type: "event", duration: "1h", status: "pending" },
        { id: 6, title: "Email Catchup", time: "04:00 PM", type: "task", status: "pending" },
    ];

    const today = new Date();

    return (
        <div className="flex flex-col h-full bg-zinc-950 pt-4">
            {/* Header */}
            <div className="px-6 pb-4">
                <h1 className="text-2xl font-bold text-white">Timeline</h1>
                <p className="text-zinc-400 text-sm flex items-center gap-2">
                    <Calendar size={14} />
                    {format(today, "EEEE, MMMM do")}
                </p>
            </div>

            {/* Timeline List */}
            <div className="flex-1 overflow-y-auto px-6 pb-24 relative">
                {/* Vertical Line */}
                <div className="absolute left-10 top-0 bottom-0 w-px bg-zinc-800" />

                <div className="space-y-6">
                    {timelineItems.length === 0 ? (
                        <div className="flex flex-col items-center justify-center pt-20 text-zinc-500 text-center">
                            <p className="text-lg">You're all caught up.</p>
                            <p className="text-sm mt-1">Go touch grass, bro. 🌲</p>
                        </div>
                    ) : (
                        timelineItems.map((item, index) => (
                            <motion.div
                                key={item.id}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="relative pl-8"
                            >
                                {/* Dot */}
                                <div className={`absolute left-0 top-1.5 w-3 h-3 rounded-full border-2 ${item.status === 'conflict' ? 'bg-orange-500 border-orange-500' :
                                        item.status === 'completed' ? 'bg-zinc-800 border-zinc-600' : 'bg-zinc-950 border-indigo-500'
                                    } z-10`} />

                                {/* Card */}
                                <div className={`p-4 rounded-xl border ${item.status === 'conflict' ? 'bg-orange-950/20 border-orange-500/20' :
                                        'bg-zinc-900/50 border-zinc-800'
                                    }`}>
                                    <div className="flex justify-between items-start mb-1">
                                        <span className={`text-xs font-semibold ${item.status === 'conflict' ? 'text-orange-400' : 'text-indigo-400'
                                            }`}>
                                            {item.time} {item.duration && `• ${item.duration}`}
                                        </span>
                                        {item.status === 'conflict' && (
                                            <AlertTriangle size={14} className="text-orange-500" />
                                        )}
                                    </div>

                                    <h3 className={`font-medium ${item.status === 'completed' ? 'text-zinc-500 line-through' : 'text-zinc-200'
                                        }`}>
                                        {item.title}
                                    </h3>

                                    {item.conflictReason && (
                                        <p className="text-xs text-orange-400 mt-2 flex items-center gap-1">
                                            Why? {item.conflictReason}
                                        </p>
                                    )}

                                    {item.type === 'task' && item.status !== 'conflict' && item.status !== 'completed' && (
                                        <div className="mt-3 flex gap-2">
                                            <button className="text-xs bg-zinc-800 hover:bg-zinc-700 text-white px-3 py-1.5 rounded-lg transition-colors">
                                                Mark Done
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
