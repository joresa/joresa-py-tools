# joresa-py-tools

A dashboard application for managing and tracking Python tools with usage analytics.

## Features

- **Dashboard Landing Page**: Displays all available tools with descriptions and launch statistics
- **Usage Analytics**: 
  - Chart showing most used tools
  - Department usage breakdown with pie chart
  - Timeline view of tool launches over time
- **Quick Stats**: 
  - Most used tool this week
  - Total launches
  - Average daily usage
  - Active users count
  - Available tools count
- **User Analytics**: View tool usage by individual users

## Installation

1. Clone the repository:
```bash
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask development server:
```bash
python app.py
```

The dashboard will be available at: http://localhost:5000

## Usage

1. Open your browser and navigate to http://localhost:5000
2. Browse available tools in the "Available Tools" section
3. Click on any tool card to launch it (demo mode shows an alert)
4. View usage analytics in the charts below
5. Switch between "By Date" and "By User" tabs to see different timeline views

## API Endpoints

- `GET /` - Dashboard home page
- `GET /api/tools` - List all available tools
- `GET /api/analytics/top-tools` - Get most used tools
- `GET /api/analytics/timeline` - Get usage timeline by date
- `GET /api/analytics/by-department` - Get usage by department
- `GET /api/analytics/by-user` - Get usage by user
- `GET /api/analytics/quick-stats` - Get quick statistics

## Project Structure

```
joresa-py-tools/
├── app.py                 # Flask application with API endpoints
├── templates/
│   └── dashboard.html     # Dashboard UI with charts
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js for data visualization
- **CORS**: Flask-CORS for cross-origin requests