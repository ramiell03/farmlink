// app/api/auth/register/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Call FastAPI register endpoint
    const res = await fetch(`${process.env.AUTH_SERVICE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    // If FastAPI returns an error, forward it
    if (!res.ok) {
      return NextResponse.json(
        { message: data.detail || "Registration failed" },
        { status: res.status },
      );
    }

    // Optionally, you can auto-login after signup by calling /auth/login here
    // For now, we just return the new user data
    return NextResponse.json(data);
  } catch (error) {
    console.error("Register route error:", error);
    return NextResponse.json(
      { message: "Server error during registration" },
      { status: 500 },
    );
  }
}
