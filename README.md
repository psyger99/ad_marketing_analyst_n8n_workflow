# 🧠 Ad Marketing Analysis Workflow
An Automated Weekly Ad Campaign Performance Report Generator Using N8N

---

## ⚙️ Workflow Design

#### 1. 🕐 Schedule Trigger
- **Node:** `Schedule Trigger`
- **Frequency:** Weekly (every Monday, 8 AM)
- **Purpose:** Initiates the reporting process automatically at the start of each week.

---

#### 2. 📁 File & Folder Validation
- **Nodes:**
  - `Search folder` — searches Google Drive for a folder named `n8n_input`.
  - `If folder exists` — checks if the folder search returned a result.
  - `Search file` — looks for a file named `mock_data` (Google Sheet).
  - `If file exists` — verifies if the file exists in the folder.

**Fail-Safe Behavior:**
If either the folder or file is missing:
- A **Slack notification** is sent (`Send Folder Error` / `Send File Error`).
- The workflow halts using `Stop and Error` nodes.  

This ensures missing data sources are immediately reported.

---

#### 3. 📊 Data Extraction
- **Node:** `Get row(s) in sheet`
- Pulls campaign metrics from Google Sheets → *Mock Data* tab.

Each row contains:
- Campaign Name  
- Clicks  
- Impressions  
- Conversions  
- Cost  
- CTR (%)  
- CPA ($)

---

#### 4. 🧹 Data Cleaning & Transformation
- **Node:** `Data Cleaning and Transformation (Code Node)`
- **Purpose:** Standardizes and enhances campaign data before AI analysis.

**Key Transformations:**
- Numeric formatting (e.g., `1,200` instead of `1200`)
- Financial formatting (adds `$` prefix)
- Percentage formatting (adds `%` symbol)
- Performance classification (✅ Excellent CTR, ⚠️ High CPA, 🚨 Underperforming)
- Calculates overall totals and averages:
  - Total Clicks, Impressions, Conversions, Cost
  - Average CTR (%) and CPA ($) 

**Output:** A structured JSON containing both **campaigns** and **summary** data objects.

---

#### 5. 🤖 AI-Generated Analysis
- **Node:**
  - Chat Model: `GPT-4o-mini` - used for fast response, and low latency and token cost which is designed for automation pipelines.

**Prompt Purpose:**
The prompt instructs GPT-4o-mini to act as an **Ad Marketing Analyst assistant**, creating a formatted Google Docs report with:

1. **Title:** `Weekly Campaign Performance Report`  
2. **Data Table:** Campaign metrics table (non-fabricated values).  
3. **AI-Generated Summary:** Overview of trends, top performers, and weak areas.  
4. **Key Recommendations:** 3 concise action items (10–15 words each).

**Formatting Rules:**
- Markdown headings using `###`
- Emoji-enabled bullet points
- Clear section separation for HTML conversion

---

#### 6. 🧾 Google Docs Report Generation
- **Nodes:**
  - `Create file from text` → creates Google Document 
  - `Markdown` → converts GPT output into HTML  
  - `Convert to File` → converts an HTML file to text file (text/plain)
  - `Set to text/html` → ensures proper MIME type (text/html) 
  - `Update file` → inputs the generated content to newly created Google Docs

**Result:**  
A formatted Google Doc titled like: `3rd Week of October 2025 - Weekly Report`, stored inside the `n8n` Google Drive folder.

---

#### 7. 📈 Spreadsheet Report Generation
- **Nodes:**
  - `Get Week of the Month` → generates current week label.
  - `Create spreadsheet` → creates a new Google Sheet.
  - `Move file` → relocates it into the Drive folder.
  - `Merge1` → Merges the output of Data Cleaning and Transformation node and Move file node for the creation of spreadsheet.
  - `Split out` → to split out the array of campaigns
  - `Map table` → to set the table for seamless data transfer to spreadsheet .
  - `Append row in sheet` → adds the mapped table to spreadsheet.
  - `Map title` → to set the title of table
  - `Update row in sheet` → updates the title of table inside the existing spreadsheet.

This creates a structured record of every week’s campaign performance in tabular form.

---

#### 8. 💬 Slack Notification
- **Nodes:**
  - `Extract summary (Code Node)` — extracts “AI-Generated Summary” section using regex.
  - `Send a message` — posts to Slack channel `#all-marketing-agency`.

**Message Structure:**

```
[Week Label (e.g., 3rd Week of October 2025) - Weekly Report]

Summary:
[AI-generated summary content]

Access the data here:
[Google Sheets link]

Performance Values (from the Data Cleaning and Transformation node's summary array):
• Total Campaigns: ...
• Total Clicks: ...
• Total Impressions: ...
• Total Conversions: ...
• Total Cost: ...
• Average CTR (%): ...
• Average CPA ($): ...
```

## 🛡️ Error Handling Strategies

| Stage | Failure Scenario | Handling Mechanism |
|-------|------------------|--------------------|
| **Folder Check** | Folder not found | Slack alert (`Send Folder Error`) + Stop workflow |
| **File Check** | File missing | Slack alert (`Send File Error`) + Stop workflow |
| **Data Check** | Empty or missing data | Slack alert (`Send Data Error`) + Stop workflow |
| **Markdown Conversion** | Missing or malformed output | Code node validation check |

Each critical node either reports the issue through Slack or halts execution safely to prevent silent failures.

---

## 🚀 Extending the Workflow for New Clients

#### 1. 🧩 Duplicate and Rename
Clone the workflow and rename it per client (e.g., `Ad Marketing Analyst Workflow - Client A`).

#### 2. 📊 Update Data Sources
- Change **Google Sheet** name or ID in the `Search file` node.
- Adjust **Drive folder query** (e.g., `name = 'client_a_data'`).

#### 3. ✍️ Client-Specific AI Customization
- Modify the AI Agent prompt:
  - Emphasize different KPIs (e.g., ROI, CPM).
  - Adjust writing tone or language style.

#### 4. 💬 Slack Integration
- Update `channelId` in the `Send a message` node to point to the client’s Slack channel.

#### 5. 🖋️ Report Branding
- Update Google Docs template:
  - Add logos or brand colors.
  - Customize header/footer styling.

#### 6. 🗓️ Adjust Scheduling
- Modify the `Schedule Trigger` node to generate reports daily, bi-weekly, or monthly.

With minimal configuration changes, the workflow can serve multiple clients independently.

## 🧪 Synthetic Data Generator
To help you test or demonstrate the workflow without using real ad campaign data, the repository includes a utility script named `syn_data_generator.py`. 

This script generates mock ad campaign performance data and can either save it locally as a CSV file or upload it directly to Google Sheets which is perfect for initial setup, demos, or debugging the workflow.

**🧭 Usage**
1. Replace the placeholders:
- SERVICE_ACCOUNT_FILE = "<your_service_account.json>"
- SPREADSHEET_ID = "<spreadsheet_id>"
- SHEET_NAME = "<sheet_name>" 
2. Run the program using CLI and appropriate flag:
- Either: `python syn_data_generator.py --csv` or: `python syn_data_generator.py --sheet`

