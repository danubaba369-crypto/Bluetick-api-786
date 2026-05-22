/* eslint-disable @typescript-eslint/no-explicit-any */
import { PUBLIC_API_URL } from "@/src/constants/route";
import { getServerSession } from "next-auth";
import { NextResponse } from "next/server";
import { authoption } from "../../auth/[...nextauth]/authOption";

export async function POST() {
  try {
    const session = await getServerSession(authoption);
    const token = session?.accessToken as string | undefined;

    const response = await fetch(`${PUBLIC_API_URL}/facebook/sync`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, error: "Failed to synchronize Facebook pages", details: error.message },
      { status: 500 }
    );
  }
}
