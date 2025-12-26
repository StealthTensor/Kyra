"use client";

import { motion } from "framer-motion";

interface FilterPillsProps {
    activeFilter: string;
    onFilterChange: (filter: string) => void;
}

export function FilterPills({ activeFilter, onFilterChange }: FilterPillsProps) {
    const filters = ["Urgent", "Important", "FYI", "All"];

    return (
        <div className="flex gap-2 p-4 overflow-x-auto no-scrollbar">
            {filters.map((filter) => {
                const isActive = activeFilter === filter;
                return (
                    <button
                        key={filter}
                        onClick={() => onFilterChange(filter)}
                        className="relative px-5 py-2 rounded-full text-sm font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-zinc-500"
                    >
                        {isActive && (
                            <motion.div
                                layoutId="activeFilter"
                                className="absolute inset-0 bg-white rounded-full"
                                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                            />
                        )}
                        <span className={`relative z-10 ${isActive ? "text-zinc-950" : "text-zinc-500"}`}>
                            {filter}
                        </span>
                    </button>
                );
            })}
        </div>
    );
}
