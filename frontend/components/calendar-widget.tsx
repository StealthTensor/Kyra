"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Calendar as CalendarIcon, Loader2 } from "lucide-react"
import { api } from "@/lib/api"
import { useAuthStore } from "@/store/useAuthStore"

interface CalendarEvent {
    id: string
    title: string
    time: string | null
    type: string
    source: "calendar" | "task"
    start_time?: string | null
}

function formatRelativeTime(dateTimeStr: string | null | undefined): string {
    if (!dateTimeStr) return "No date"
    
    try {
        const date = new Date(dateTimeStr)
        const now = new Date()
        const diffMs = date.getTime() - now.getTime()
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
        
        if (diffDays === 0) {
            return `Today, ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
        } else if (diffDays === 1) {
            return `Tomorrow, ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
        } else if (diffDays === -1) {
            return `Yesterday, ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
        } else if (diffDays > 1 && diffDays <= 7) {
            return date.toLocaleDateString([], { weekday: 'short', hour: '2-digit', minute: '2-digit' })
        } else {
            return date.toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
        }
    } catch {
        return dateTimeStr
    }
}

function getEventTypeColor(type: string): string {
    if (type === 'deadline' || type === 'Deadline') return 'bg-red-500'
    if (type === 'event' || type === 'Event') return 'bg-blue-500'
    if (type === 'meeting' || type === 'Meeting') return 'bg-purple-500'
    return 'bg-emerald-500'
}

export function CalendarWidget() {
    const { user } = useAuthStore()
    const [events, setEvents] = useState<CalendarEvent[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!user?.email) {
            setIsLoading(false)
            return
        }

        const fetchEvents = async () => {
            try {
                setIsLoading(true)
                setError(null)
                const response = await api.get(`/calendar/events?email=${encodeURIComponent(user.email)}&days=7&limit=3`)
                setEvents(response.data || [])
            } catch (err: any) {
                console.error("Error fetching calendar events:", err)
                setError(err.response?.data?.detail || "Failed to load events")
                setEvents([])
            } finally {
                setIsLoading(false)
            }
        }

        fetchEvents()
    }, [user?.email])

    return (
        <Card className="w-full max-w-xs border-l border-zinc-800 bg-zinc-950/50 backdrop-blur-sm h-full rounded-none border-t-0 border-b-0 border-r-0">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-zinc-400 flex items-center gap-2">
                    <CalendarIcon className="w-4 h-4" />
                    Upcoming
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {isLoading ? (
                    <div className="flex items-center justify-center py-4">
                        <Loader2 className="w-4 h-4 animate-spin text-zinc-500" />
                    </div>
                ) : error ? (
                    <p className="text-xs text-zinc-500 text-center py-2">{error}</p>
                ) : events.length === 0 ? (
                    <p className="text-xs text-zinc-500 text-center py-2">No upcoming events</p>
                ) : (
                    events.map((e) => (
                        <div key={e.id} className="flex gap-3 items-start group">
                            <div className={`mt-1 w-2 h-2 rounded-full shrink-0 ${getEventTypeColor(e.type)}`} />
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-zinc-200 group-hover:text-white transition-colors truncate">
                                    {e.title}
                                </p>
                                <p className="text-xs text-zinc-500">{formatRelativeTime(e.start_time || e.time)}</p>
                            </div>
                        </div>
                    ))
                )}

                <div className="pt-4 border-t border-zinc-900 mt-4">
                    <p className="text-xs text-zinc-600 text-center">
                        Synced with Google Calendar
                    </p>
                </div>
            </CardContent>
        </Card>
    )
}
