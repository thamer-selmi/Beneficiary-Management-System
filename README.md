# Beneficiary Management System

A Python desktop application for managing farmers who benefit from irrigation services. The application provides a graphical interface for beneficiary records, invoices, consumption tracking, reports, and application settings.

> **Demo data:** The database included with this project is intended for demonstration and testing. Do not use it as a source of real beneficiary information.

## Features

- **Dashboard:** overview of the system and key information.
- **Farmers management:** add, view, and edit farmer records.
- **Invoices:** generate invoice PDF documents.
- **Consumption reports:** create PDF reports related to water consumption.
- **Reports:** view management/reporting information.
- **Settings:** configure application settings, including the database path.
- **Arabic PDF output:** PDF generation uses Arabic text shaping and bidirectional text support.

## Built With

- **Python** — application logic
- **Tkinter / ttk** — desktop graphical user interface
- **Object-Oriented Programming (OOP)** — application organization
- **SQLite** — local database
- **ReportLab** — PDF generation
- **arabic-reshaper** and **python-bidi** — Arabic text rendering in PDFs

## Project Structure

```text
Beneficiary-Management-System/
├── backend/                 # Database access and business services
│   ├── farmers_services.py
│   ├── documents_services.py
│   ├── reports_services.py
│   └── database.db          # Demo SQLite database
├── gui/                     # Tkinter interface
│   ├── dashboard.py
│   ├── farmers_tab.py
│   ├── invoices_tab.py
│   ├── reports_tab.py
│   ├── settings.py
│   ├── dialogs.py
│   └── main_window.py
├── models/                  # Consumption and invoice/PDF logic
├── fonts/                   # Fonts used when generating PDFs
├── img/                     # Application images and icons
├── config.py                # Application configuration
└── main.py                  # Application entry point
```

## Requirements

- Python 3.10 or later is recommended.
- Tkinter (usually included with the standard Python installation; on some Linux distributions it must be installed separately).
- The Python packages listed below.

## Installation and Run

1. Clone the repository:

   ```bash
   git clone https://github.com/thamer-selmi/Beneficiary-Management-System.git
   cd Beneficiary-Management-System
   ```

2. (Recommended) Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install reportlab arabic-reshaper python-bidi
   ```

4. Start the application from the project root:

   ```bash
   python main.py
   ```

## Screenshots

Screenshots will be added here. If you add screenshots to the repository, place them in a `screenshots/` directory and embed them like this:

```markdown
![Application dashboard](screenshots/dashboard.png)
```

Use screenshots containing demo data only. Do not publish personal, financial, or other sensitive information.

## Notes

- Run `main.py` from the project root so that the package imports and relative asset paths resolve as expected.
- The application uses a local SQLite database. Keep a backup before replacing or changing the database file.
- PDF documents are generated locally by the application.
- This README describes the current project structure and features; setup instructions may need adjustment if dependencies or startup behavior change.

## License

No license has been specified yet. Unless a license is added to this repository, the project is not explicitly released for reuse, modification, or redistribution.
