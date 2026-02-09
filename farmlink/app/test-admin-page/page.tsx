"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function TestAdminApiPage() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testApi = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/admin/stats", {
        credentials: 'include',
      });
      const data = await res.json();
      setResult({
        status: res.status,
        ok: res.ok,
        data: data
      });
    } catch (error) {
      setResult({
        error: error instanceof Error ? error.message : "Unknown error"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-4">Test Admin Stats API</h1>
      <Button onClick={testApi} disabled={loading} className="mb-4">
        {loading ? "Testing..." : "Test /api/admin/stats"}
      </Button>
      
      {result && (
        <div className="p-4 bg-gray-100 rounded-lg">
          <pre className="whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}