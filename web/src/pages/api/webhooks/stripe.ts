import type { APIRoute } from "astro";
import { API_URL } from "astro:env/server";

export const POST: APIRoute = async ({ request }) => {
  const payload = await request.text();
  const signature = request.headers.get("stripe-signature") ?? "";

  const response = await fetch(`${API_URL}/api/webhooks/stripe`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Stripe-Signature": signature,
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 RacksideWeb",
    },
    body: payload,
  });

  return new Response(await response.text(), { status: response.status });
};
