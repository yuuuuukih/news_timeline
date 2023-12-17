# Timeline-aware fake news generation with LLM

This project is designed to create a timeline-aware fake news dataset from the [News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download).

## Project Structure

The project is structured as follows:

- `src/`: Contains the main source code for the project.
  - `create.py`: The main script to create the timeline.
  - `create_dataset/`: Contains scripts for creating and preprocessing the dataset.
    - `preprocess/`: Scripts for preprocessing the dataset.
    - `keyword_groups/`: Scripts for grouping keywords.
    - `timeline/`: Scripts for creating the timeline.
    - `split/`: Scripts for spliting the timeline into train, dev, and test.
    - `type/`: Scripts for original type.
    - `utils/`: Scripts for useful function (e.g., decorator).
- `others/`: Contains not important scripts.
- `bin/`: Contains shell scripts for creating entities and timelines.

## Usage

1. Clone the repository.
2. Download the [News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)
3. Install the project dependencies using [Poetry](https://python-poetry.org/). If you haven't installed Poetry, please follow the instructions on their [official website](https://python-poetry.org/docs/#installation). Once Poetry is installed, you can install the dependencies by running:
   ```sh
   poetry install
   ```
4. Run the `create_dataset.sh` script in the `bin/` directory to create the timeline-aware fake news dataset.

Please note that this project is still under development and the structure and usage may change in the future.