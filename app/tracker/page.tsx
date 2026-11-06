'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import {
  CheckCircle2,
  Clock,
  PhoneCall,
  MessageSquare,
  ShieldCheck,
  Truck,
  ArrowLeft,
  RefreshCw,
  ExternalLink,
  MapPin,
  Calendar,
  Lock,
  UserCheck
} from 'lucide-react';

export default function OrderTrackerPage() {
  return (
    <React.Suspense fallback={<div className="p-8 text-center text-slate-500">Loading Order Tracker...</div>}>
      <OrderTrackerContent />
    </React.Suspense>
  );
}

function OrderTrackerContent() {
  const searchParams = useSearchParams();
  const orderId = searchParams.get('order') || 'UDYAM-2026-DEMO';
  const [order, setOrder] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function fetchOrder() {
      setLoading(true);
      try {
        const res = await fetch(`/api/v1/order/${orderId}`);
        if (res.ok) {
          const data = await res.json();
          setOrder(data);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchOrder();
  }, [orderId]);

  return (
    <div className="min-h-screen bg-slate-100 py-6 px-4 flex flex-col items-center justify-center">
      <div className="w-full max-w-[420px] min-h-[800px] bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col text-slate-800">
        {/* Header */}
        <div className="bg-gradient-to-r from-red-600 to-red-700 text-white p-4 pt-5 pb-4">
          <div className="flex items-center justify-between mb-3">
            <Link
              href="/"
              className="flex items-center space-x-1 text-xs text-red-100 hover:text-white transition font-medium"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Portal</span>
            </Link>
            <div className="flex items-center space-x-1.5 text-[10px] bg-red-800/60 px-2 py-0.5 rounded-full border border-red-400/30">
              <Lock className="w-3 h-3 text-emerald-300" />
              <span>HMAC Signed</span>
            </div>
          </div>

          <div className="text-center space-y-1">
            <div className="inline-block px-2.5 py-0.5 rounded-full bg-white/20 text-white text-[10px] font-mono font-bold tracking-wider uppercase mb-1">
              Order {orderId}
            </div>
            <h2 className="text-lg font-black tracking-tight text-white">
              Live Fulfillment Milestone Tracker
            </h2>
            <p className="text-xs text-red-100">
              Zero-Touch Auto-Provisioning & Dispatch Pipeline
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-4 flex-1 space-y-4 overflow-y-auto">
          {loading ? (
            <div className="py-20 text-center space-y-2 text-slate-500">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto text-red-600" />
              <p className="text-xs">Verifying cryptographic order token...</p>
            </div>
          ) : order ? (
            <>
              {/* Order Status Overview */}
              <div className="bg-slate-900 text-white p-4 rounded-2xl shadow-sm space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-400">Target Enterprise:</span>
                  <span className="font-bold text-white">{order.business_name}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-400">Configured Bundle:</span>
                  <span className="font-bold text-emerald-400">{order.bundle_name}</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-400">Monthly Plan (MRC):</span>
                  <span className="font-black text-white text-sm">₹{order.monthly_mrc}/mo</span>
                </div>

                <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-300">
                  <span className="flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    <span>Guaranteed SLA: &lt; 48 Hours</span>
                  </span>
                  <span className="font-mono text-emerald-400">Token Verified</span>
                </div>
              </div>

              {/* 4 Milestones */}
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-3">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Milestone Progress
                </h4>

                <div className="relative pl-6 space-y-4 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
                  {order.milestones &&
                    order.milestones.map((m: any, idx: number) => {
                      const isDone = m.status === 'COMPLETED';
                      const isProg = m.status === 'IN_PROGRESS';
                      return (
                        <div key={idx} className="relative">
                          <div
                            className={`absolute -left-6 top-0.5 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold border-2 ${
                              isDone
                                ? 'bg-emerald-600 border-emerald-600 text-white'
                                : isProg
                                ? 'bg-red-600 border-red-600 text-white animate-pulse'
                                : 'bg-white border-slate-300 text-slate-400'
                            }`}
                          >
                            {isDone ? '✓' : idx + 1}
                          </div>
                          <div>
                            <div className="font-bold text-xs text-slate-800">{m.step}</div>
                            <div className="text-[11px] text-slate-500">{m.timestamp}</div>
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>

              {/* Technician Dispatch Card */}
              {order.technician && (
                <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2.5">
                      <div className="w-10 h-10 rounded-full bg-red-50 border border-red-200 flex items-center justify-center">
                        <UserCheck className="w-5 h-5 text-red-600" />
                      </div>
                      <div>
                        <div className="font-bold text-xs text-slate-900">
                          {order.technician.name}
                        </div>
                        <div className="text-[10px] text-slate-500">
                          Badge #{order.technician.badge_id} • {order.technician.role}
                        </div>
                      </div>
                    </div>
                    <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                      Dispatched
                    </span>
                  </div>

                  <div className="bg-slate-50 p-2.5 rounded-xl text-xs text-slate-700 space-y-1">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Reserved Slot:</span>
                      <span className="font-bold text-slate-900">{order.technician.slot}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Target Delivery PIN:</span>
                      <span className="font-bold text-slate-900">{order.delivery_pincode}</span>
                    </div>
                  </div>

                  {/* 1-Tap Contact Action Buttons to eliminate chasing */}
                  <div className="grid grid-cols-2 gap-2 pt-1">
                    <a
                      href={order.technician.whatsapp_link}
                      target="_blank"
                      rel="noreferrer"
                      className="py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center justify-center space-x-1.5 transition shadow"
                    >
                      <MessageSquare className="w-3.5 h-3.5" />
                      <span>WhatsApp Direct</span>
                    </a>

                    <a
                      href={`tel:${order.technician.phone}`}
                      className="py-2 px-3 rounded-xl bg-slate-900 hover:bg-black text-white font-bold text-xs flex items-center justify-center space-x-1.5 transition shadow"
                    >
                      <PhoneCall className="w-3.5 h-3.5" />
                      <span>Direct Phone</span>
                    </a>
                  </div>
                </div>
              )}

              {/* Accel SLA Promise */}
              <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-2xl text-xs text-emerald-800 space-y-1">
                <div className="flex items-center space-x-1.5 font-bold">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" />
                  <span>Guaranteed Activation SLA</span>
                </div>
                <p className="text-[11px] text-emerald-700">
                  {order.sla_guarantee ||
                    'Activation guaranteed within 48 hours, or receive ₹500 billing credit automatically.'}
                </p>
              </div>
            </>
          ) : (
            <div className="py-20 text-center text-xs text-slate-400">
              Order not found.
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 bg-slate-50 border-t border-slate-200 text-center text-[11px] text-slate-400">
          Accel Business Project Udyam • High-Assurance Zero-Trust Engine
        </div>
      </div>
    </div>
  );
}

