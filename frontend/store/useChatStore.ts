import { create } from 'zustand';
import { api } from '@/lib/api';
import { toast } from 'sonner';
import { useAuthStore } from '@/store/useAuthStore';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    reasoning?: string; // Explanation from agent
}

interface ChatState {
    messages: Message[];
    isLoading: boolean;
    conversationId: string | null;

    sendMessage: (query: string) => Promise<void>;
    clearChat: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
    messages: [],
    isLoading: false,
    conversationId: null,

    sendMessage: async (query) => {
        const { messages, conversationId } = get();

        // Optimistic user message
        const userMsg: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: query,
            timestamp: new Date().toISOString(),
        };

        set({ messages: [...messages, userMsg], isLoading: true });

        try {
            const user = useAuthStore.getState().user;

            if (!user?.id) {
                toast.error("Please login to chat");
                set({ isLoading: false });
                return;
            }

            const response = await api.post('/chat', {
                query,
                conversation_id: conversationId,
                user_id: user.id
            });

            const { response: answer, conversation_id, explanation } = response.data;

            const botMsg: Message = {
                id: Date.now().toString() + '_bot',
                role: 'assistant',
                content: answer || "I recall... something.",
                timestamp: new Date().toISOString(),
                reasoning: explanation
            };

            set({
                messages: [...messages, userMsg, botMsg],
                isLoading: false,
                conversationId: conversation_id
            });

        } catch (error) {
            console.error("Chat Error", error);
            toast.error("Couldn't reach Kyra");
            set({ isLoading: false });
        }
    },

    clearChat: () => set({ messages: [], conversationId: null }),
}));
