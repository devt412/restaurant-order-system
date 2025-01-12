import { useEffect, useRef, useState } from 'react'

export default function useWebSocket(url: string) {
    const [socket, setSocket] = useState<WebSocket | null>(null)
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined)

    useEffect(() => {
        const connect = () => {
            try {
                const ws = new WebSocket(url)

                ws.onopen = () => {
                    console.log('WebSocket connected')
                    setSocket(ws)
                }

                ws.onclose = () => {
                    console.log('WebSocket disconnected')
                    setSocket(null)
                    // Attempt to reconnect after 2 seconds
                    reconnectTimeoutRef.current = setTimeout(connect, 2000)
                }

                ws.onerror = (error) => {
                    console.error('WebSocket error:', error)
                    ws.close()
                }

            } catch (error) {
                console.error('WebSocket connection error:', error)
                reconnectTimeoutRef.current = setTimeout(connect, 2000)
            }
        }

        connect()

        return () => {
            if (socket) {
                socket.close()
            }
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current)
            }
        }
    }, [url])

    return socket
}