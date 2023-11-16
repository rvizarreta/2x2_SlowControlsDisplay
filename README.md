# 2x2_SlowControlsDisplay

This repository contains the code used for setting up the slow controls monitoring system for Mx2. 

## Technology Stack:

- Backend: FastAPI. Go to `https://localhost:8000/docs` for more detail.
- Frontend: React JS
- Database: InfluxDB version 1.8.10
- Monitoring: Grafana
- Working on python virtual environment venv that contains influxdb and pysnmp (do pip install for these).

## The Architecture:

This is the architecture for the Slow Controls GUI:

![image](https://github.com/rvizarreta/Mx2_SlowControlsDisplay/assets/34606228/5ad2391b-7a69-4a3b-a731-de15dd602a69)

## How to Start this App?
To run this, follow this steps:

**Backend:**

1) Go to my personal work area:
```bash
/home/acd/rvizarr/Mx2_SlowControlsDisplay
```
2) Source python environment:
```bash
source myenv/bin/activate
```

3) Go to backend directory:
```bash
/home/acd/rvizarr/Mx2_SlowControlsDisplay/MyApp
```
4) Start backend server:
```bash
uvicorn main:app --reload
```

**Frontend (use a new terminal session):**

1) Go to my personal work area:
```bash
/home/acd/rvizarr/Mx2_SlowControlsDisplay
```
2) Source python environment:
```bash
source myenv/bin/activate
```

3) Go to frontend app directory:
```bash
/home/acd/rvizarr/Mx2_SlowControlsDisplay/MyApp/my-app
```

4) Start server:
```bash
npm start
```

5) Access GUI in your VNC browser:
```bash
localhost:3006
```



