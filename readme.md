# DAX Analytics Dashboard

## Overview

This project is a comprehensive Data Analysis Expressions (DAX) analytics dashboard built with Streamlit. It provides insights into DAX usage patterns, trends, and challenges based on Stack Overflow questions.

## Features

1. **Overview Page**
   - General statistics about DAX questions and answers
   - Visualizations of DAX function usage and categories
   - Temporal analysis of DAX activity

2. **Trends Over Time**
   - Temporal patterns in DAX query frequency
   - Evolution of DAX function utilization
   - Community engagement metrics over time

3. **Key Concepts and Functions**
   - Analysis of common DAX concepts and their difficulty levels
   - Visualization of most used DAX functions and their relationships
   - Historical trends in DAX function popularity

4. **Learning Path**
   - Curated resources for learning DAX
   - Practice suggestions and tips for mastering DAX

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```
streamlit run main.py
```


## Data

The dashboard uses data from Stack Overflow DAX questions. The data is loaded from a Parquet file located in the `data` directory.

## Project Structure

- `main.py`: Entry point of the Streamlit app
- `pages/`: Contains individual pages of the dashboard
  - `overview.py`: General overview and statistics
  - `trends_over_time.py`: Temporal analysis of DAX usage
  - `key_concepts_functions.py`: Analysis of DAX concepts and functions
  - `learning_path.py`: Resources and tips for learning DAX
- `utils/`: Utility functions
  - `data_loader.py`: Functions for loading and preprocessing data


## Contributing

Contributions to improve the dashboard or extend its functionality are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

[MIT License](LICENSE)

## Author

[Mandla Sibanda]

## Acknowledgments

- Data sourced from Stack Overflow
- Built with Streamlit and various data visualization libraries
