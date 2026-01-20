import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const token = req.cookies.get("access_token")?.value;
  const { pathname } = req.nextUrl;

  const isAuthPage =
    pathname.startsWith("/signin") || pathname.startsWith("/signup");

  // Not logged in → block protected routes
  if (!token && !isAuthPage) {
    return NextResponse.redirect(new URL("/signin", req.url));
  }

  // Logged in → block auth pages
  if (token && isAuthPage) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
