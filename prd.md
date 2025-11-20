# Subscription Tracker – Vibe Coding PRD (MVP)
## 1. Overview

A simple web app that helps individuals keep track of recurring subscriptions, avoid forgotten renewals, and understand spending.

## 2. Goals

Centralize all subscriptions

Remind users 7 days before renewal

Provide basic analytics (monthly, annual, categories, trends)

## 3. Target User

The Overwhelmed Subscriber
20–40 subscriptions, often forgets billing dates, wants a clear dashboard.

## 4. Core Features (MVP)

Subscription Dashboard (list/grid + search)

Manual Add/Edit/Delete

Email Alerts (7 days before renewal)

Analytics (monthly/annual totals, category breakdown, trends)

## 5. Tech Stack

Next.js (App Router)

TypeScript

SQLite

TailwindCSS + shadcn/ui

NextAuth (email+password)

Resend (email delivery)

## 6. Data Model
User

id

email

password_hash

created_at

Subscription

id

user_id

name (R)

cost (R)

billing_frequency (R)

next_renewal_date (O)

category (O)

status (R)

notes (O)

color_tag (O)

manage_url (O)

created_at

updated_at

RenewalHistory

id

subscription_id

renewal_date

created_at

## 7. Feature Requirements
Dashboard

List + grid toggle

Search by name

Responsive

Subscription card fields: name, cost, frequency, renewal date, category, status, notes, tag, days until renewal

Edit opens drawer; delete uses confirmation modal

Manual Entry

Required: name, cost, billing_frequency, status
Optional: renewal date, category, notes, tag, URL
Duplicates allowed
Minimal history tracking

Renewal Alerts

Email only

Send 7 days before renewal

Daily cron job

Analytics

Total monthly spend

Total annual spend

Category breakdown chart

Renewals this month

6–12 month trend

## 8. System Architecture

Full-stack Next.js

Server Actions for CRUD

Vercel Cron → Server Action for email alerts

REST API only for future integrations (not MVP)

## 9. UI Pages

Dashboard

Add Subscription (modal or page)

Edit Subscription (drawer)

Analytics

Settings

Login / Signup / Forgot Password

## 10. Out of Scope (MVP)

Bank syncing

Email parsing

SMS, push, in-app notifications

Cancellation automation

Inline editing

Public API

Mobile app

CSV import/export

AI/LLM features

## 11. Success Metrics

Users add ≥ 3 subscriptions in 7 days

Users return at least once within 14 days

## 12. Milestones
M1 – Setup

Next.js project, DB schema, auth

M2 – User Account

Login, signup, reset password

M3 – Subscription CRUD

Add, edit drawer, delete modal, history

M4 – Dashboard

List/grid, search, responsive UI

M5 – Analytics + Alerts

Charts, monthly/annual data, renewal email cron