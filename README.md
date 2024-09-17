# Commodity Web Scraper

This project is a web scraper built with **Scrapy** for scraping commodity data from a specified website. It allows users to scrape data for different products and save the output to a CSV file. The scraper is highly configurable, enabling users to specify:
- A **base URL** for scraping.
- A list of **product numbers** to scrape.
- Custom **column names** for the CSV file.
- A custom **CSV file name**.

## Features

- Supports dynamic input for the base URL, product numbers, column names, and output file.
- Scrapes large datasets from websites with pagination handling.
- Data is saved in a customizable CSV file format.
- Simple to use with clear command-line options.

## Prerequisites

- **Python 3.6+**
- **Scrapy** (Install via `pip`)

### Installing Scrapy

Install Scrapy using `pip`:

```bash
pip install scrapy
