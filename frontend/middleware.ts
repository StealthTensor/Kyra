import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('token')?.value || request.cookies.get('auth-token')?.value;
    const isAuthPage = request.nextUrl.pathname.startsWith('/auth');

    // Protect strict B2B routes
    const protectedPaths = ['/app/'];
    const isProtectedPath = protectedPaths.some((path) =>
        request.nextUrl.pathname.startsWith(path)
    );

    if (isProtectedPath && !token) {
        const loginUrl = new URL('/auth/login', request.url);
        loginUrl.searchParams.set('from', request.nextUrl.pathname);
        return NextResponse.redirect(loginUrl);
    }

    // Redirect authenticated users away from login
    if (isAuthPage && token) {
        return NextResponse.redirect(new URL('/app/dashboard', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/app/:path*', '/mail/:path*', '/chat/:path*', '/timeline/:path*', '/auth/:path*'],
};
