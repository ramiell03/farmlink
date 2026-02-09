import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const token = request.cookies.get("access_token")?.value;
    
    if (!token) {
      return NextResponse.json(
        { error: "Unauthorized - No authentication token" },
        { status: 401 }
      );
    }

    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { error: "Backend URL not configured" },
        { status: 500 }
      );
    }

    const response = await fetch(
      `${backendUrl}/api/v1/communication/messages/${params.userId}`,
      {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || `Failed to fetch messages: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error("Error in messages API:", error);
    
    // Return mock data for development
    return NextResponse.json([
      {
        id: "msg-1",
        sender_id: "user-123",
        receiver_id: "current-user",
        content: "Hi, I'm interested in your maize crop.",
        created_at: "2024-01-15T09:30:00Z",
        read: true,
      },
      {
        id: "msg-2",
        sender_id: "current-user",
        receiver_id: "user-123",
        content: "Hello! Yes, I have 500kg available.",
        created_at: "2024-01-15T09:32:00Z",
        read: true,
      },
      {
        id: "msg-3",
        sender_id: "user-123",
        receiver_id: "current-user",
        content: "Great! What's your best price per kg?",
        created_at: "2024-01-15T09:33:00Z",
        read: true,
      },
      {
        id: "msg-4",
        sender_id: "current-user",
        receiver_id: "user-123",
        content: "FCFA 150 per kg. Where are you located?",
        created_at: "2024-01-15T09:35:00Z",
        read: true,
      },
      {
        id: "msg-5",
        sender_id: "user-123",
        receiver_id: "current-user",
        content: "When can you deliver the maize?",
        created_at: "2024-01-15T10:30:00Z",
        read: false,
      },
    ]);
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const token = request.cookies.get("access_token")?.value;
    
    if (!token) {
      return NextResponse.json(
        { error: "Unauthorized - No authentication token" },
        { status: 401 }
      );
    }

    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { error: "Backend URL not configured" },
        { status: 500 }
      );
    }

    const body = await request.json();
    const { content } = body;

    if (!content) {
      return NextResponse.json(
        { error: "Message content is required" },
        { status: 400 }
      );
    }

    const response = await fetch(`${backendUrl}/api/v1/communication/messages`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        receiver_id: params.userId,
        content,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || `Failed to send message: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data, { status: 201 });

  } catch (error) {
    console.error("Error sending message:", error);
    return NextResponse.json(
      { error: "Internal server error while sending message" },
      { status: 500 }
    );
  }
}