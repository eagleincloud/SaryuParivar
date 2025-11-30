# How Admin Gets Notified About Support Requests/Complaints

## 📧 **1. Email Notifications (Primary Method)**

When a user submits a support request/complaint:

✅ **Automatic Email Sent** to ALL superuser/admin accounts
- **Recipients**: All users with `is_superuser=True` and `is_active=True`
- **Fallback**: If no superuser emails found, sends to `DEFAULT_FROM_EMAIL` (ouruserverified@gmail.com)
- **Email Subject**: `🔔 New Support Request: [Subject]`

**Email Content Includes:**
- User's name, email, phone number
- Subject and detailed message
- Request ID
- **Direct link** to admin panel to view/manage the request
- Status and creation date
- Priority level

**Email Configuration:**
- SMTP Server: Gmail (smtp.gmail.com)
- From Email: ouruserverified@gmail.com
- Sent immediately when request is submitted

---

## 🔔 **2. Admin Panel Dashboard Notifications**

### Admin Homepage (`/admin/`)
- **Notification Badge**: Shows pending support requests count
- **Urgent Requests**: Highlights urgent priority requests separately
- **Quick Access Button**: Direct link to view all pending support requests
- **Visual Alert**: Blue notification box with count and action button

### Support Request List Page (`/admin/administration/supportrequest/`)
- **Notification Badge Column**: Shows "⚠️ NEW - Needs Attention" for pending requests
- **Status Badges**: Color-coded status indicators
  - 🟠 Pending
  - 🔵 In Progress
  - 🟢 Resolved
  - ⚫ Closed
- **Priority Badges**: Color-coded priority levels
  - 🟢 Low
  - 🟡 Medium (default)
  - 🟠 High
  - 🔴 Urgent
- **Smart Ordering**: Pending requests shown first, then sorted by creation date

---

## 📋 **3. Admin Panel Features**

### Support Request Management
- **View All Requests**: `/admin/administration/supportrequest/`
- **Filter by Status**: Pending, In Progress, Resolved, Closed
- **Filter by Priority**: Low, Medium, High, Urgent
- **Search**: By subject, name, email, phone, or message content
- **Update Status**: Change status and add admin notes
- **Auto-resolve**: Automatically sets `resolved_at` when status changes to "Resolved"
- **Admin Notes**: Internal notes field for tracking communication

---

## 🎯 **4. How to Access Support Requests**

### Step-by-Step:
1. **Login to Admin Panel**: Go to `/admin/`
2. **Check Dashboard**: Look for notification badge showing pending count
3. **Click "View Support Requests"**: Button in notification box
4. **Or Navigate Directly**: Administration → Support Requests
5. **Filter**: Use status filter to see only pending requests
6. **Respond**: 
   - Update status to "In Progress" when working on it
   - Add admin notes for internal tracking
   - Mark as "Resolved" when issue is fixed

---

## 📊 **5. Notification Priority System**

- **🔴 Urgent**: Red badge, shown prominently, highest priority
- **🟠 High**: Orange badge, high priority
- **🟡 Medium**: Yellow badge (default priority)
- **🟢 Low**: Green badge, lower priority

---

## ✅ **6. Best Practices for Admins**

1. **Check Email Regularly**: Monitor admin email for new support request notifications
2. **Check Admin Panel Daily**: Login to `/admin/` to see notification badges
3. **Respond Promptly**: Update status to "In Progress" when working on a request
4. **Add Notes**: Use `admin_notes` field to track internal communication and actions taken
5. **Mark Resolved**: Change status to "Resolved" when issue is fixed
6. **Follow Up**: Check resolved requests to ensure user satisfaction

---

## 📝 **Summary**

**Admin gets notified in 3 ways:**
1. ✅ **Email** - Sent to all superuser emails immediately
2. ✅ **Admin Dashboard** - Notification badge with count and urgent requests
3. ✅ **Support Request List** - Visual badges, ordering, and filtering

All support requests are stored in the database and can be managed through the Django admin panel at `/admin/administration/supportrequest/`.

---

## 🔗 **Quick Links**

- **Admin Panel**: `/admin/`
- **Support Requests**: `/admin/administration/supportrequest/`
- **Pending Requests**: `/admin/administration/supportrequest/?status__exact=pending`
- **Urgent Requests**: `/admin/administration/supportrequest/?status__exact=pending&priority__exact=urgent`
