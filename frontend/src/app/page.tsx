"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import { Login } from "@/components/Login";

export default function Home() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const t = localStorage.getItem("pm_token");
    setToken(t);
  }, []);

  if (!token) {
    return <Login onLogin={(t) => setToken(t)} />;
  }

  return <KanbanBoard />;
}
