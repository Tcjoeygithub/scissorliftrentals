#!/usr/bin/env python3
"""
Simple static site generator for Vercel deployment.
This version doesn't rely on pandas or other complex dependencies.
"""

import os
import json
import shutil
from datetime import datetime

def main():
    """Generate a simple static site."""
    print("Starting simple site generation...")
    
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Create assets directories
    for dir_path in ['output/assets/css', 'output/assets/js', 'output/assets/images']:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    # Copy static assets if they exist
    if os.path.exists('scissor-lift.jpeg'):
        shutil.copy('scissor-lift.jpeg', 'output/assets/images/')
    if os.path.exists('scissor-lift-favicon.png'):
        shutil.copy('scissor-lift-favicon.png', 'output/assets/images/')
    
    # Create a simple CSS file
    with open('output/assets/css/style.css', 'w') as f:
        f.write("""
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #0066cc;
            color: white;
            padding: 1rem 0;
        }
        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        nav ul {
            display: flex;
            list-style: none;
            padding: 0;
        }
        nav ul li {
            margin-left: 20px;
        }
        nav ul li a {
            color: white;
            text-decoration: none;
        }
        .hero {
            background-color: #f4f4f4;
            padding: 2rem 0;
            text-align: center;
        }
        .hero img {
            max-width: 100%;
            height: auto;
            margin-top: 20px;
        }
        .states-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .state-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .state-card a {
            color: #0066cc;
            text-decoration: none;
            font-weight: bold;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
        }
        """)
    
    # Create a simple homepage
    with open('output/index.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Scissor Lifts for Rent | Find Scissor Lift Rental Companies</title>
            <meta name="description" content="Find scissor lift rental companies near you. Browse our directory of scissor lift rental providers across the United States.">
            <link rel="stylesheet" href="/assets/css/style.css">
            <link rel="icon" href="/assets/images/scissor-lift-favicon.png">
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Scissor Lifts for Rent</h1>
                    <nav>
                        <ul>
                            <li><a href="/">Home</a></li>
                            <li><a href="/states/">States</a></li>
                        </ul>
                    </nav>
                </div>
            </header>
            
            <section class="hero">
                <div class="container">
                    <h2>Find Scissor Lift Rental Companies Near You</h2>
                    <p>Browse our directory of scissor lift rental providers across the United States.</p>
                    <img src="/assets/images/scissor-lift.jpeg" alt="Scissor Lift" />
                </div>
            </section>
            
            <section class="container">
                <h2>Browse Scissor Lift Rentals by State</h2>
                <div class="states-grid">
                    <div class="state-card">
                        <a href="/ca/">California</a>
                    </div>
                    <div class="state-card">
                        <a href="/ny/">New York</a>
                    </div>
                    <div class="state-card">
                        <a href="/tx/">Texas</a>
                    </div>
                    <div class="state-card">
                        <a href="/fl/">Florida</a>
                    </div>
                    <div class="state-card">
                        <a href="/states/">View All States</a>
                    </div>
                </div>
            </section>
            
            <footer>
                <div class="container">
                    <p>&copy; 2025 Scissor Lifts for Rent. All rights reserved.</p>
                </div>
            </footer>
        </body>
        </html>
        """)
    
    # Create a states directory page
    os.makedirs('output/states', exist_ok=True)
    with open('output/states/index.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Browse Scissor Lift Rentals by State | Scissor Lifts for Rent</title>
            <meta name="description" content="Find scissor lift rental companies in your state. Browse our directory of scissor lift rental providers across all 50 states.">
            <link rel="stylesheet" href="/assets/css/style.css">
            <link rel="icon" href="/assets/images/scissor-lift-favicon.png">
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Scissor Lifts for Rent</h1>
                    <nav>
                        <ul>
                            <li><a href="/">Home</a></li>
                            <li><a href="/states/">States</a></li>
                        </ul>
                    </nav>
                </div>
            </header>
            
            <section class="container">
                <h1>Browse Scissor Lift Rentals by State</h1>
                <div class="states-grid">
                    <div class="state-card">
                        <a href="/al/">Alabama</a>
                    </div>
                    <div class="state-card">
                        <a href="/ak/">Alaska</a>
                    </div>
                    <div class="state-card">
                        <a href="/az/">Arizona</a>
                    </div>
                    <div class="state-card">
                        <a href="/ar/">Arkansas</a>
                    </div>
                    <div class="state-card">
                        <a href="/ca/">California</a>
                    </div>
                    <div class="state-card">
                        <a href="/co/">Colorado</a>
                    </div>
                    <div class="state-card">
                        <a href="/ct/">Connecticut</a>
                    </div>
                    <div class="state-card">
                        <a href="/de/">Delaware</a>
                    </div>
                    <div class="state-card">
                        <a href="/fl/">Florida</a>
                    </div>
                    <div class="state-card">
                        <a href="/ga/">Georgia</a>
                    </div>
                </div>
            </section>
            
            <footer>
                <div class="container">
                    <p>&copy; 2025 Scissor Lifts for Rent. All rights reserved.</p>
                </div>
            </footer>
        </body>
        </html>
        """)
    
    # Create placeholder state pages for a few states
    for state_abbr, state_name in [
        ('ca', 'California'),
        ('ny', 'New York'),
        ('tx', 'Texas'),
        ('fl', 'Florida')
    ]:
        os.makedirs(f'output/{state_abbr}', exist_ok=True)
        with open(f'output/{state_abbr}/index.html', 'w') as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Scissor Lift Rental in {state_name} | Top Equipment Rental Companies</title>
                <meta name="description" content="Looking for scissor lift rentals in {state_name}? Browse our directory of {state_name} scissor lift rental companies. Compare prices, equipment types, and availability for your project needs.">
                <link rel="stylesheet" href="/assets/css/style.css">
                <link rel="icon" href="/assets/images/scissor-lift-favicon.png">
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>Scissor Lifts for Rent</h1>
                        <nav>
                            <ul>
                                <li><a href="/">Home</a></li>
                                <li><a href="/states/">States</a></li>
                            </ul>
                        </nav>
                    </div>
                </header>
                
                <section class="container">
                    <h1>Scissor Lift Rentals in {state_name}</h1>
                    <p>This is a placeholder page for {state_name}. In the full version of the site, this page would list all scissor lift rental companies in {state_name}.</p>
                </section>
                
                <footer>
                    <div class="container">
                        <p>&copy; 2025 Scissor Lifts for Rent. All rights reserved.</p>
                    </div>
                </footer>
            </body>
            </html>
            """)
    
    print("Site generation complete!")
    return True

if __name__ == "__main__":
    main() 