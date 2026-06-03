import { defineMiddleware } from "astro:middleware";
import { getToken } from "@/lib/auth";

export const onRequest = defineMiddleware((context, next) => {
  const { pathname } = context.url;
  const isAdminPage = pathname === "/admin" || pathname.startsWith("/admin/");
  const isLogin = pathname === "/admin/login";

  if (isAdminPage && !isLogin && !getToken(context.cookies)) {
    return context.redirect("/admin/login");
  }
  return next();
});
