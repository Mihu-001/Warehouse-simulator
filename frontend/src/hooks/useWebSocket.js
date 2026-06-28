import { useState, useEffect, useRef, useCallback } from 'react';

export default function useWebSocket(url) {
  const [state, setState] = useState(null);
  const [status, setStatus] = useState("DISCONNECTED"); // CONNECTING, CONNECTED, DISCONNECTED
  
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    if (wsRef.current && (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING)) {
      return;
    }

    setStatus("CONNECTING");
    
    // Resolve dynamic address: fallback to localhost if none provided
    const targetUrl = url || `ws://${window.location.hostname}:8000/ws`;
    const socket = new WebSocket(targetUrl);
    wsRef.current = socket;

    socket.onopen = () => {
      setStatus("CONNECTED");
      console.log("WebSocket connected to " + targetUrl);
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setState(data);
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
      }
    };

    socket.onclose = () => {
      setStatus("DISCONNECTED");
      console.log("WebSocket connection closed. Attempting reconnect in 3s...");
      // Auto reconnect
      reconnectTimeoutRef.current = setTimeout(() => {
        connect();
      }, 3000);
    };

    socket.onerror = (err) => {
      console.error("WebSocket encountered error:", err);
      socket.close();
    };
  }, [url]);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  const sendMessage = useCallback((msg) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(msg));
    } else {
      console.warn("WebSocket is not open. Msg queued/dropped:", msg);
    }
  }, []);

  return { state, status, sendMessage };
}
