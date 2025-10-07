# Application Flow Diagram

## User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         LANDING PAGE                             │
│  • Welcome message                                               │
│  • Feature overview cards                                        │
│  • Login / Register buttons                                      │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├─── Not Authenticated ──┐
             │                        │
             │                        v
             │              ┌──────────────────┐
             │              │  REGISTER PAGE   │
             │              │  • Username      │
             │              │  • Email         │
             │              │  • Password      │
             │              └────────┬─────────┘
             │                       │
             │                       v
             │              ┌──────────────────┐
             │              │   LOGIN PAGE     │
             │              │  • Username      │
             │              │  • Password      │
             │              │  • Remember Me   │
             │              └────────┬─────────┘
             │                       │
             └───── Authenticated ───┘
                                     │
                                     v
                          ┌──────────────────────┐
                          │     DASHBOARD        │
                          │  • Available Tools   │
                          │  • Recent Activity   │
                          │  • Navigation        │
                          └──────────┬───────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     │               │               │
                     v               v               v
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │  ANALYTICS   │  │ DIFF CHECKER │  │ FUTURE TOOLS │
          │  • Charts    │  │ • Compare    │  │ • Claims     │
          │  • Usage     │  │ • History    │  │ • Workflows  │
          │  • Trends    │  │ • Results    │  │ • More...    │
          └──────────────┘  └──────────────┘  └──────────────┘
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                          │
│  Bootstrap 5 UI | Chart.js | JavaScript                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/HTTPS
                      v
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                           │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │  Auth Blueprint│  │ Main Blueprint │  │ Tools Blueprint │  │
│  │  • Login       │  │ • Dashboard    │  │ • Diff Checker  │  │
│  │  • Register    │  │ • Analytics    │  │ • History       │  │
│  │  • Logout      │  │ • API          │  │ • Future Tools  │  │
│  └────────────────┘  └────────────────┘  └─────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Flask-Login                           │  │
│  │              Session Management & Auth                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   SQLAlchemy ORM                          │  │
│  │              Database Abstraction Layer                   │  │
│  └───────────────────────┬──────────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           v
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite DATABASE                             │
│                                                                  │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  users  │  │  tools  │  │ tool_usages  │  │diff_history │  │
│  ├─────────┤  ├─────────┤  ├──────────────┤  ├─────────────┤  │
│  │ id      │  │ id      │  │ id           │  │ id          │  │
│  │ username│  │ name    │  │ user_id (FK) │  │ user_id (FK)│  │
│  │ email   │  │ display │  │ tool_id (FK) │  │ text1       │  │
│  │ password│  │ desc    │  │ timestamp    │  │ text2       │  │
│  └─────────┘  └─────────┘  └──────────────┘  │ diff        │  │
│                                               │ timestamp   │  │
│                                               └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow - Diff Checker

```
User Action: Compare Two Texts
        │
        v
┌──────────────────┐
│  POST /tools/diff│
│  with form data  │
└────────┬─────────┘
         │
         v
┌──────────────────────────────┐
│  1. Validate form            │
│  2. Generate diff (difflib)  │
│  3. Create HTML output       │
└────────┬─────────────────────┘
         │
         ├──── Save to Database ────┐
         │                          │
         v                          v
┌─────────────────┐      ┌──────────────────┐
│  DiffHistory    │      │   ToolUsage      │
│  • texts        │      │   • user_id      │
│  • result       │      │   • tool_id      │
│  • timestamp    │      │   • timestamp    │
└─────────────────┘      └──────────────────┘
         │
         v
┌──────────────────────────────┐
│  Render template with result │
│  • Show diff highlighting    │
│  • Display comparison        │
└──────────────────────────────┘
         │
         v
    Display to User
```

## Analytics Flow

```
Dashboard Request
        │
        v
┌─────────────────────┐
│ GET /analytics      │
│ Load page with      │
│ Chart.js setup      │
└──────┬──────────────┘
       │
       ├── Fetch Chart Data ──┐
       │                      │
       v                      v                      v
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ /api/most-used │   │ /api/usage-    │   │ /api/usage-    │
│     -tools     │   │   by-date      │   │   by-user      │
└───────┬────────┘   └───────┬────────┘   └───────┬────────┘
        │                    │                    │
        v                    v                    v
  ┌──────────────────────────────────────────────────┐
  │        Query ToolUsage + Tool + User             │
  │        • Group by tool/date/user                 │
  │        • Aggregate counts                        │
  │        • Last 30 days filter                     │
  └────────────────────┬─────────────────────────────┘
                       │
                       v
                 JSON Response
                       │
                       v
  ┌──────────────────────────────────────────┐
  │   Chart.js renders:                      │
  │   • Bar charts (tools, users)            │
  │   • Line chart (daily usage)             │
  │   • Interactive tooltips                 │
  └──────────────────────────────────────────┘
```

## Modular Tool Addition Flow

```
Developer wants to add new tool
        │
        v
┌─────────────────────────────────────────────┐
│ Step 1: Create route in app/tools/routes.py│
│  @bp.route('/new-tool')                     │
│  @login_required                            │
│  def new_tool():                            │
│      record_tool_usage('new_tool')          │
│      # tool logic                           │
│      return render_template(...)            │
└─────────────────┬───────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────┐
│ Step 2: Create template                     │
│  app/templates/tools/new_tool.html          │
│  extends base.html                          │
└─────────────────┬───────────────────────────┘
                  │
                  v
┌─────────────────────────────────────────────┐
│ Step 3: Register tool in database           │
│  python shell or update init_db.py          │
│  Add Tool entry with name, route, etc.      │
└─────────────────┬───────────────────────────┘
                  │
                  v
        Tool automatically appears
        in Dashboard & Analytics!
```

## Security Flow

```
User Request
     │
     v
┌──────────────────┐
│ Protected Route? │
└────┬─────────┬───┘
     │         │
     No        Yes
     │         │
     │         v
     │   ┌─────────────────┐
     │   │ @login_required │
     │   │   decorator     │
     │   └────┬────────────┘
     │        │
     │        v
     │   ┌──────────────────┐
     │   │ Check session    │
     │   │ via Flask-Login  │
     │   └────┬─────────┬───┘
     │        │         │
     │   Authenticated  Not Auth
     │        │         │
     │        │         v
     │        │   ┌──────────────┐
     │        │   │ Redirect to  │
     │        │   │ /auth/login  │
     │        │   └──────────────┘
     │        │
     v        v
   Allow Access
     │
     v
┌──────────────────┐
│ CSRF Protection  │
│ on POST requests │
└────┬─────────────┘
     │
     v
  Process Request
```
