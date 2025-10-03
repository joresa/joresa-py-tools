# joresa-py-tools

A clean and simple analytics dashboard with a FastAPI backend and React frontend featuring real-time usage charts.

## Features

- **Clean UI/UX**: Modern interface built with React and Tailwind CSS
- **Real-time Charts**: Interactive charts powered by Chart.js
- **FastAPI Backend**: High-performance REST API
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
joresa-py-tools/
├── backend/          # FastAPI backend
│   ├── main.py       # API endpoints
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── App.jsx   # Main application component
│   │   └── index.css # Tailwind CSS styles
│   └── package.json
└── README.md
```

## Setup Instructions

### Quick Start (Recommended)

Run the automated setup script:
```bash
./start.sh
```

This will:
- Set up both backend and frontend
- Install all dependencies
- Start both services
- Open the dashboard at http://localhost:5173

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## API Endpoints

- `GET /` - API information
- `GET /api/usage/daily` - Get daily usage statistics for the last 7 days
- `GET /api/usage/summary` - Get overall usage summary

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: JavaScript library for building user interfaces
- **Vite**: Next-generation frontend tooling
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Simple yet flexible JavaScript charting library
- **react-chartjs-2**: React wrapper for Chart.js

## Development

The application features:
- Clean, minimal design with Tailwind CSS
- Responsive layout that works on all screen sizes
- Interactive charts for data visualization
- Real-time data fetching with loading states
- Error handling and user feedback

## License

MIT