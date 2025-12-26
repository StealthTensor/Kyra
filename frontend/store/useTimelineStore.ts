import { create } from 'zustand';
import { api } from '@/lib/api';
import { toast } from 'sonner';

export interface Task {
    id: string;
    title: string;
    time: string;
    type: "event" | "task";
    status: "pending" | "completed" | "conflict";
    conflictReason?: string;
    duration?: string;
    priority?: string;
}

interface TimelineState {
    tasks: Task[];
    isLoading: boolean;
    fetchTasks: (email: string) => Promise<void>;
}

export const useTimelineStore = create<TimelineState>((set) => ({
    tasks: [],
    isLoading: false,

    fetchTasks: async (email: string) => {
        set({ isLoading: true });
        try {
            const response = await api.get('/tasks', { params: { email } });
            set({ tasks: response.data, isLoading: false });
        } catch (error) {
            console.error("Failed to fetch tasks", error);
            // toast.error("Failed to load timeline"); // Optional, generic error handling might be better
            set({ isLoading: false });
        }
    }
}));
