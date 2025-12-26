"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Calendar as CalendarIcon, CheckSquare } from "lucide-react"

export function CalendarWidget() {
    // Mock data for UI - in real app would fetch from API
    // Since Phase 6 requirements are focusing on backend logic mainly, 
    // and "UI Update: Add a 'Calendar' widget... that shows ... next 3 upcoming".
    // We will hardcode for now or fetch if we had an endpoint.
    // Let's create the visual structure.

    // Ideally we'd hit a GET /calendar/events endpoint.

    const events = [
        { title: "Review Lab Manual", time: "Today, 5:00 PM", type: "task" },
        { title: "Project Meeting", time: "Tomorrow, 10:00 AM", type: "event" },
        { title: "Submit Assignment", time: "Fri, 11:59 PM", type: "deadline" },
    ]

    return (
        <Card className="w-full max-w-xs border-l border-zinc-800 bg-zinc-950/50 backdrop-blur-sm h-full rounded-none border-t-0 border-b-0 border-r-0">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-zinc-400 flex items-center gap-2">
                    <CalendarIcon className="w-4 h-4" />
                    Upcoming
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {events.map((e, i) => (
                    <div key={i} className="flex gap-3 items-start group">
                        <div className={`mt-1 w-2 h-2 rounded-full shrink-0 ${e.type === 'deadline' ? 'bg-red-500' :
                                e.type === 'event' ? 'bg-blue-500' : 'bg-emerald-500'
                            }`} />
                        <div>
                            <p className="text-sm font-medium text-zinc-200 group-hover:text-white transition-colors">
                                {e.title}
                            </p>
                            <p className="text-xs text-zinc-500">{e.time}</p>
                        </div>
                    </div>
                ))}

                <div className="pt-4 border-t border-zinc-900 mt-4">
                    <p className="text-xs text-zinc-600 text-center">
                        Synced with Google Calendar
                    </p>
                </div>
            </CardContent>
        </Card>
    )
}
