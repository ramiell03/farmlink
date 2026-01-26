// lib/api.ts
interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  username: string;
  role: string;
  location: string;
  phone_number: string;
}

interface LoginResponse {
  role: string;
}

export async function login(data: LoginData) {
  // ✅ Call Next.js API route, NOT the auth service directly
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result: LoginResponse = await res.json();

  if (!res.ok) {
    throw new Error(result.role || "Login failed");
  }

  // Store role in localStorage for UI routing
  localStorage.setItem("role", result.role);

  return result;
}

export async function register(data: RegisterData) {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Registration failed");
  }

  return res.json();
}
