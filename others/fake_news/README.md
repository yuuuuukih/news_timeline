# generate_fake_news.py

This is a Python-based script that makes use of the GPT-4, a generative pre-training transformer-based language prediction model developed by OpenAI. The purpose of the script is to generate a fake news article adhering to several given conditions and based on a specific timeline data.

## Dependencies

- **OpenAI Python library**: This script uses OpenAI for generating the fake news article. You need to have the OpenAI library installed. You can install it using the pip package manager.

  ```bash
  pip install openai
  ```

## Environment Variables

This script requires two environment variables to be set:

- `OPENAI_KUNLP`: This environment variable should hold the organization ID for your OpenAI account.

- `OPENAI_API_KEY_TIMELINE`: This environment variable should have your OpenAI API key.

## Usage

You can use the following shell command to run the script:

```bash
FILE_PATH=your_file_path
python generate_fake_news.py --model_name MODEL_NAME --file_path $FILE_PATH
```
### Arguments

The script accepts two command line arguments:

- `model_name`: (Optional) The name of the model to be used for generating fake news. This is 'gpt-4' by default.

- `file_path`: (Optional) The path to the JSON file that contains the timeline data for generating the fake news. The default value provided here is `'/mnt/mint/hara/datasets/news_category_dataset/preprocessed/keywords/2019_2022/keywords.json'`.

## How it works

- First, the script reads timeline data from a given (or default) JSON file. This data will serve as the basis for generating the fake news article.

- It then constructs a system message that lays out conditions for the generated fake news which includes properties like fake status, headline, date, short description, and content.

- The user_content variable is populated with existing timeline data to set as input for the GPT-4 model.

- It calls the OpenAI API method 'ChatCompletion.create' passing in the model name and system and user-content messages. This creates a completion in a conversational manner.

- The response from the OpenAI API is the generated fake news, which is then printed on the console.

## Output

The output, in successful cases, is a fake news article adhering to given conditions, blending smoothly with earlier timeline records, and contradicting the subsequent ones.