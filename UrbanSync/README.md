# UrbanSync — Smart City Unified Platform

A responsive React/Vite demo for a municipal services website, inspired by the information architecture and public-service presentation of the Davis County, Utah website. It is an original UrbanSync interface and is not affiliated with Davis County or any government authority.

## What's included

- Public-facing home page with a large photographic hero, upper utility bar, main navigation, quick links, service directory, city feature, announcements and footer.
- Separate **Citizen Portal** for reporting and tracking civic issues.
- Separate **Admin Portal** for complaint workflow management, department snapshots, illustrative analytics and CSV export.
- Sample complaint data and sample city notices for demonstration purposes.
- Responsive layout for desktop, tablet and mobile.
- Existing FastAPI backend integration retained for complaint reads, submissions and status updates.

## Run the frontend

In a terminal, open the `frontend` directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (typically `http://localhost:5173`).

## Demo notes

- The frontend works with sample data if the backend is not running; locally created sample reports are kept in browser memory for the current session.
- To persist data through the API, start the FastAPI backend as described in the project setup and ensure it is available at `http://127.0.0.1:8000`.
- Images are loaded from Unsplash and require an internet connection.
- All dashboard figures and news notices are dummy data. This is an academic demonstration, not an official government service.
