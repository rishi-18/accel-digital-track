import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params;
  const subpath = path.join('/');
  const search = request.nextUrl.search;
  const targetUrl = `${BACKEND_URL}/api/v1/${subpath}${search}`;

  try {
    const res = await fetch(targetUrl, {
      headers: {
        'Accept': 'application/json',
      },
      cache: 'no-store'
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Backend unreachable', details: err?.message },
      { status: 502 }
    );
  }
}

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params;
  const subpath = path.join('/');
  const targetUrl = `${BACKEND_URL}/api/v1/${subpath}`;

  try {
    const contentType = request.headers.get('content-type') || '';
    let body: any;
    const headers: Record<string, string> = {};

    if (contentType.includes('multipart/form-data') || contentType.includes('application/x-www-form-urlencoded')) {
      const formData = await request.formData();
      const res = await fetch(targetUrl, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      return NextResponse.json(data, { status: res.status });
    } else {
      body = await request.text();
      headers['Content-Type'] = contentType || 'application/json';
      const res = await fetch(targetUrl, {
        method: 'POST',
        headers,
        body,
      });
      const data = await res.json();
      return NextResponse.json(data, { status: res.status });
    }
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Backend unreachable', details: err?.message },
      { status: 502 }
    );
  }
}
