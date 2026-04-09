# GHL Workflow Automation Setup Guide
## Aces Sports Academy — Summer Camp 2026 Registration Confirmation Email

---

## Overview

This guide walks you through creating a GoHighLevel (GHL) workflow that automatically sends a confirmation email whenever a contact is tagged with **"Summer Camp 2026"** inside the **Aces Sports Academy** sub-account.

**Trigger:** Contact Tag Added → `Summer Camp 2026`  
**Action:** Send Email (using the HTML template in `ghl-email-template.html`)

---

## Prerequisites — Verify Your Sending Domain First

Before building the workflow, confirm your sending email/domain is verified in GHL so emails don't land in spam.

1. Log into your GHL Agency Dashboard.
2. Click **Settings** (gear icon, bottom-left sidebar).
3. Navigate to **Email Services** (sometimes listed as **Email Configuration** or **Mailgun**).
4. Confirm that the domain you plan to send from (e.g., `acesportsacademy.net` or your Mailgun domain) shows a **Verified** status.
5. If not verified, follow GHL's domain verification steps (add the provided DNS records to your domain registrar, then click **Verify**).
6. Set your **From Email** and **From Name** defaults here if desired, or you will set them per-email in the workflow.

> **Important:** Sending from an unverified domain can cause emails to be marked as spam or blocked entirely.

---

## Step 1 — Log In and Navigate to the Aces Sports Academy Sub-Account

1. Go to [https://app.gohighlevel.com](https://app.gohighlevel.com) and log in with your agency credentials.
2. On the Agency Dashboard, locate the **sub-accounts** list (left sidebar or main panel).
3. Find **Aces Sports Academy** in the list.
4. Click on **Aces Sports Academy** to switch into that sub-account. The interface will reload showing the sub-account's data.
   - Confirm you are in the correct account by checking the sub-account name shown in the top-left or top-center of the screen.

---

## Step 2 — Open the Automation / Workflows Section

1. In the left-hand sidebar of the Aces Sports Academy sub-account, click **Automation**.
2. From the Automation submenu, click **Workflows**.
   - You will see a list of existing workflows (if any).

---

## Step 3 — Create a New Workflow

1. Click the **+ Create Workflow** button (top-right of the Workflows screen).
2. A dialog will appear asking how you want to start. Select **Start from Scratch**.
3. Click **Create** (or **Continue**).
   - The Workflow Builder canvas will open.
4. At the top of the builder, click on the default workflow name (e.g., "New Workflow") and rename it to:
   > **Summer Camp 2026 — Registration Confirmation**
5. Press **Enter** or click away to save the name.

---

## Step 4 — Add the Trigger: Contact Tag Added

1. On the workflow canvas, click **+ Add New Trigger** (or the trigger placeholder at the top of the flow).
2. A panel will slide out on the right showing all available trigger types.
3. Search for or scroll to find **Contact Tag**.
4. Click **Contact Tag** to select it.
5. In the trigger configuration options that appear:
   - **Filter / Tag:** Type `Summer Camp 2026` in the tag field.
   - GHL will suggest existing tags — select **Summer Camp 2026** if it already exists, or type the full tag name exactly as it should appear.
   - **Trigger condition:** Ensure it is set to **Tag Added** (not Tag Removed).
6. Click **Save Trigger** (or **Save**) to confirm.
   - The trigger block on the canvas should now read: *"Contact Tag — Summer Camp 2026 is added"* (or similar).

---

## Step 5 — Add the Action: Send Email

1. Below the trigger block on the canvas, click the **+** icon to add an action.
2. In the action search panel, search for **Send Email** or browse to the **Communication** or **Email** category.
3. Click **Send Email** to add it.
4. The email action configuration panel will open on the right.

---

## Step 6 — Configure the Email Action

Fill in each field as follows:

### From Name
- Click the **From Name** field.
- Enter: `Aces Baseball Academy`

### From Email
- Click the **From Email** field.
- Select or enter your verified sending email address (e.g., `info@acesportsacademy.net` or your verified Mailgun/SMTP address).
- This must match a domain you verified in **Settings → Email Services** (see Prerequisites).

### Reply-To (Optional)
- You may enter `info@acesportsacademy.net` or leave as default.

### Subject Line
- Click the **Subject** field.
- Enter exactly:
  > `You're Registered! ⚾ Aces Baseball Academy Summer Camp 2026`
- To insert the baseball emoji (⚾), copy-paste it directly from this guide.

### Email Body — Paste the HTML Template

1. In the email body area, look for a toggle or button that says **HTML**, **Code View**, or a `</>` icon. Click it to switch to **HTML / Code mode**.
   - In some GHL versions this is a small icon in the toolbar (looks like angle brackets `< >`).
   - In others, there is a dedicated **HTML Editor** tab at the top of the email body section.
2. Once in HTML mode, **select all** existing code in the editor (Ctrl+A / Cmd+A) and **delete** it.
3. Open the file `ghl-email-template.html` from your workspace/files.
4. **Select all** the HTML code (Ctrl+A / Cmd+A) and **copy** it (Ctrl+C / Cmd+C).
5. Return to GHL and **paste** the HTML into the code editor (Ctrl+V / Cmd+V).
6. Click **Save** or switch back to the visual preview to confirm the email renders correctly.

> **Tip:** If you see a visual preview of the styled email (dark navy header, gold accents, camp details, coaches section), the HTML pasted correctly.

### Custom Values / Merge Tags Used in the Template

The HTML template already contains the following GHL custom values:
- `{{contact.name}}` — Automatically replaced with the contact's full name in the greeting.
- `{{contact.tags}}` — Can be referenced anywhere in the email body if you want to display the contact's tags (optional; not displayed by default in the current template but available for use).

> **Note:** All registration details (name, age, session, emergency contact, etc.) collected during registration are stored in the **contact's Notes field** in GHL. Staff can view these details by opening the contact record → scrolling to the **Notes** section. You do not need to add this data to the email unless you create custom fields and reference them with additional `{{contact.custom_field_name}}` values.

---

## Step 7 — Review the Full Workflow

At this point your workflow should look like this on the canvas:

```
[TRIGGER]
Contact Tag Added → "Summer Camp 2026"
        ↓
[ACTION]
Send Email
  From:    Aces Baseball Academy <info@acesportsacademy.net>
  Subject: You're Registered! ⚾ Aces Baseball Academy Summer Camp 2026
  Body:    [HTML Confirmation Email Template]
```

Double-check:
- [ ] Trigger tag name matches exactly: `Summer Camp 2026` (case-sensitive in GHL)
- [ ] From Name is: `Aces Baseball Academy`
- [ ] Subject line is correct and contains the emoji
- [ ] HTML body is pasted and previewing correctly
- [ ] `{{contact.name}}` appears in the greeting line in the HTML

---

## Step 8 — Save and Publish the Workflow

1. Click **Save** (top-right of the Workflow Builder) to save a draft.
2. Once saved, toggle the workflow status from **Draft / Inactive** to **Active** (or **Published**).
   - In GHL, this is typically a toggle switch at the top of the builder labeled **Active** or a **Publish** button.
3. Confirm the status indicator shows the workflow is **Active** / **Published** (usually green).

> **The workflow is now live.** Any time a contact in the Aces Sports Academy sub-account receives the tag "Summer Camp 2026", they will automatically receive the confirmation email.

---

## Step 9 — Test the Workflow (Recommended)

Before going live with real registrations, test with a dummy contact:

1. Navigate to **Contacts** in the left sidebar.
2. Create a test contact (or find an existing one you own — use your own email address).
3. Open the contact record.
4. Click **+ Add Tag** and add the tag `Summer Camp 2026`.
5. Wait 1–2 minutes and check the email inbox for the confirmation email.
6. Verify:
   - Email arrived and was not in spam.
   - The contact's name populated correctly in the greeting (`Dear [Your Name],`).
   - All camp details, coaches, and formatting render correctly.
7. Remove the `Summer Camp 2026` tag from the test contact when done.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Email not sending | Confirm sending domain is verified in **Settings → Email Services** |
| `{{contact.name}}` shows as literal text | Ensure the email body is saved as HTML with GHL's custom value syntax intact (double curly braces) |
| Email lands in spam | Verify your domain's SPF, DKIM, and DMARC DNS records in **Settings → Email Services** |
| Workflow not triggering | Check that the tag name on the contact is spelled exactly `Summer Camp 2026` — GHL tags are case-sensitive |
| HTML not rendering | Paste the HTML only in Code/HTML mode, not in the visual editor, to avoid stripping inline styles |

---

## Quick Reference

| Item | Value |
|---|---|
| Sub-account | Aces Sports Academy |
| Trigger type | Contact Tag Added |
| Tag name | `Summer Camp 2026` |
| Action | Send Email |
| From Name | `Aces Baseball Academy` |
| Subject | `You're Registered! ⚾ Aces Baseball Academy Summer Camp 2026` |
| Template file | `ghl-email-template.html` |
| Contact custom value | `{{contact.name}}` |
| Phone | (689) 312-9568 |
| Website | acesportsacademy.net |

---

*Guide prepared for Aces Sports Academy — GoHighLevel Sub-Account Setup*
