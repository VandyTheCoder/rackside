import type { AstroCookies } from "astro";

export const SESSION_COOKIE = "rk_session";
const MAX_AGE = 60 * 60 * 8;

export function setToken(cookies: AstroCookies, token: string): void {
  cookies.set(SESSION_COOKIE, token, {
    httpOnly: true,
    secure: import.meta.env.PROD,
    sameSite: "lax",
    path: "/",
    maxAge: MAX_AGE,
  });
}

export function getToken(cookies: AstroCookies): string | undefined {
  return cookies.get(SESSION_COOKIE)?.value;
}

export function clearToken(cookies: AstroCookies): void {
  cookies.delete(SESSION_COOKIE, { path: "/" });
}
