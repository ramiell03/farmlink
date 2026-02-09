// app/api/auth/login/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Call backend auth service
    const res = await fetch(`${process.env.AUTH_SERVICE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json(
        { message: data.detail || "Invalid email or password" },
        { status: res.status }
      );
    }

     const response = NextResponse.json({ 
      role: data.role,
      user_id: data.user_id, // Add this
      email: data.email,
      username: data.username 
    });


    // ✅ Set httpOnly cookies for frontend domain
    response.cookies.set("access_token", data.access_token, {
      httpOnly: true,
      path: "/",
      sameSite: "lax",
    });
    response.cookies.set("refresh_token", data["refresh-token"], {
      httpOnly: true,
      path: "/",
      sameSite: "lax",
    });

    return response;
    
  } catch (error) {
    console.error("Login route error:", error);
    return NextResponse.json(
      { message: "Server error in login route" },
      { status: 500 }
    );
  }
}
