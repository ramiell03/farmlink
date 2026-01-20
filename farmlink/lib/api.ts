// lib/api.ts
const BASE_URL =
  process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://127.0.0.1:8000/api/v1";

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

export async function login(data: LoginData) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }

  return res.json(); // { access_token, refresh-token, role }
}

export async function register(data: RegisterData) {
  const res = await fetch(`${BASE_URL}/auth/register`, {
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

export async function getProfile(access_token: string) {
  const res = await fetch(`${BASE_URL}/auth/profile`, {
    method: "GET",
    headers: { Authorization: `Bearer ${access_token}` },
  });

  if (!res.ok) throw new Error("Failed to fetch profile");
  return res.json();
}
