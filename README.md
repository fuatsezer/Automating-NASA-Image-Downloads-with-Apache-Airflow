# NASA Airflow DAG Project

## Overview
This project uses Apache Airflow to automate the process of fetching and saving NASA's Astronomy Picture of the Day (APOD). The pipeline consists of two tasks:
1. Fetching the image using NASA's API.
2. Sending a notification upon completion.

## Features
- Automatically fetches APOD images daily.
- Stores images locally.
- Provides a notification for task completion.

## Getting Started

### Prerequisites
- Python 3.8+
- Apache Airflow

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/nasa-airflow-project.git
   cd nasa-airflow-project
