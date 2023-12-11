# Archive_12112023
**English**:
This branch serves as an archive of the project as it was on 12/11/2023.
This snapshot was taken just before a significant restructuring of the project's directory structure. No more commits will be made on this branch and it is not intended to be merged back into main.
It functions as a historical record and reference of the code at this point in time.

**日本語**:
このブランチは、プロジェクトが 2023/12/11 にどのような状態であったかをアーカイブするためのものです。
このスナップショットは、プロジェクトのディレクトリ構造を大幅に再構築する前に取られました。 このブランチにはこれ以上コミットは行われず、mainにマージすることを意図していません。
この時点でのコードの歴史的な記録およびリファレンスとして機能します。


# News Timeline
## data_preprocess
- without_content
    - Format the [News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download)
- with_content
    - Create a dataset by adding the content acquired by scraping to the "News Category Dataset" formatted by "without_content".
- keywords
    - Classify articles that contain the specified keywords in the headline or short_description.

## fake_news
- Generate fake news using OPENAI_API.