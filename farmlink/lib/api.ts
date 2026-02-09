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
  user_id: string;  // Add this
  email: string;    // Add this
  username: string;
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
  localStorage.setItem("user_id", result.user_id);
  localStorage.setItem("email", result.email);
  localStorage.setItem("username", result.username);
  localStorage.setItem("is_authenticated", "true");

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

// Logout function
export async function logout() {
  // Clear localStorage
  localStorage.removeItem("role");
  localStorage.removeItem("user_id");
  localStorage.removeItem("email");
  localStorage.removeItem("username");
  localStorage.removeItem("is_authenticated");
  
  // Call logout API to clear cookies
  await fetch("/api/auth/logout", {
    method: "POST",
    credentials: "include",
  });
}
