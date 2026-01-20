"use client";

import { useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation"; // <--- app router
import { login } from "@/lib/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignIn = async () => {
    const id = toast.loading("Signing in...");

    try {
      const data = await login({ email, password });

      // Set cookies if needed (or API route already sets httpOnly cookies)
      document.cookie = `access_token=${data.access_token}; path=/`;
      document.cookie = `refresh_token=${data["refresh-token"]}; path=/`;

      toast.success("Signed in successfully", { id });

      // <-- Redirect after successful login
      router.push("/dashboard");
    } catch (err: unknown) {
      const errorMessage =
        err && typeof err === "object" && "message" in err
          ? (err as { message?: string }).message
          : "Invalid credentials";
      toast.error(errorMessage || "Invalid credentials", { id });
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Sign in</CardTitle>
        <CardDescription>
          Enter your email and password to access your account
        </CardDescription>
      </CardHeader>

      <CardContent className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="john@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="grid gap-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <Button onClick={handleSignIn} className="w-full">
          Sign in
        </Button>
      </CardContent>

      <CardFooter className="flex flex-col gap-2">
        <p className="text-sm text-muted-foreground">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="underline">
            Sign up
          </Link>
        </p>
      </CardFooter>
    </Card>
  );
}
