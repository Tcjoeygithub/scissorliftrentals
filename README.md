# Scissor Lift Rentals Directory

A comprehensive directory website for scissor lift rental companies across the United States. This project generates a static website with pages for each state and city, making it easy for users to find scissor lift rental providers in their area.

## Features

- **State and City Pages**: Organized directory of scissor lift rental companies by state and city
- **Responsive Design**: Mobile-friendly layout that works on all devices
- **SEO Optimized**: Unique meta titles and descriptions for each page
- **Interactive Maps**: Location maps for rental companies with available coordinates
- **Comprehensive Information**: Contact details, hours, and reviews for each company
- **Browse by State**: Easy navigation through states and cities

## Technical Details

- **Static Site Generator**: Custom Python script that processes data and generates HTML pages
- **Data Source**: Excel file containing scissor lift rental company information
- **Styling**: Custom CSS for a clean, professional appearance
- **Maps**: JavaScript integration for interactive maps
- **Favicon**: Custom scissor lift icon for browser tabs

## Getting Started

### Prerequisites

- Python 3.6+
- Required Python packages: pandas, jinja2, requests

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Tcjoeygithub/scissorliftrentals.git
   cd scissorliftrentals
   ```

2. Install required packages:
   ```
   pip install pandas jinja2 requests
   ```

### Usage

1. Generate the website:
   ```
   python generate_site.py
   ```

2. Serve the website locally:
   ```
   python serve.py
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Project Structure

- `generate_site.py`: Main script that generates the static website
- `serve.py`: Simple HTTP server for local testing
- `scissor-lift-companies.xlsx`: Data source containing company information
- `output/`: Generated website files (not included in repository)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Font Awesome for icons
- Google Maps for location services 