"use client";

import { useState } from "react";

export const Login = ({ onLogin }: { onLogin: (token: string) => void }) => {
  const [username, setUsername] = useState("user");
  const [password, setPassword] = useState("password");
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const body = await res.json();
        setError(body.detail || "Login failed");
        return;
      }
      const data = await res.json();
      const token = data.token;
      localStorage.setItem("pm_token", token);
      onLogin(token);
    } catch (err: any) {
      setError(err?.message || "Login failed");
    }
  };

  return (
    <form onSubmit={submit} className="mx-auto mt-24 w-full max-w-md">
      <div className="rounded-xl border bg-white p-6">
        <h2 className="mb-4 text-2xl font-semibold">Sign in</h2>
        <label className="block text-sm">
          Username
          <input
            className="mt-1 w-full rounded border px-3 py-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <label className="mt-3 block text-sm">
          Password
          <input
            type="password"
            className="mt-1 w-full rounded border px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
        <div className="mt-4 text-right">
          <button className="rounded bg-[var(--primary-blue)] px-4 py-2 text-white">Sign in</button>
        </div>
      </div>
    </form>
  );
};
