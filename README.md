# Resume Builder Project

This project is a dynamic resume builder that allows users to create and manage their resume using a web-based interface. The resume is generated and displayed as a clean, professional HTML page, with options to save the data and compile the final document. Currently, I've built this thing just for personal need thus being so rigid with the format/layout. Tho, I foresee myself developing this later to be more flexible to accomodate a variety of resume styles/formats.

## Features

- **Web-based Workspace**: Edit your resume in real-time through a simple and intuitive interface.
- **Data Persistence**: Resume data is saved automatically to `resume.json`, ensuring your information is never lost.
- **Live Preview**: Watch your resume change instantly as you type and edit.
- **Direct Compilation**: Compile your resume into a professional HTML document ready for export.

## Local Development

To run the development server locally, use the following command:

```bash
python app.py
```

The server will start on `http://localhost:5000`, where you can access the resume builder workspace.

## Building the Resume

To generate the final HTML resume from the data in `resume.json`, run:

```bash
python builder.py
```

The generated resume will be saved to `output/resume.html`.

## Project Structure

- `app.py`: Contains the main application logic, including the development server and API endpoints.
- `builder.py`: Handles the compilation of the resume template using the data from `resume.json`.
- `resume.json`: Stores all the resume data (name, experience, education, skills, etc.).
- `templates/`: Contains the HTML templates for the workspace and the final resume.
- `output/`: The directory where the generated resume HTML will be saved.
