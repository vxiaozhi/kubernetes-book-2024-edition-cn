import getpass
import os
import logging
from langchain_core.messages import HumanMessage, SystemMessage

#os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import AzureChatOpenAI

from split_markdown4gpt import split

logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)


def split_long_file(file_name):
    with open(file_name, "r") as f:
        sections = split(f.read(), model="gpt-3.5-turbo", limit=1000)
        return sections


model = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

def do_translate(input_text):
    system_message = "<任务> 您是一名精通简体中文的专业译者，特别是在将专业的学术论文转换为通俗易懂的科普文章方面有着非凡的能力。"

    user_message = """请协助我把下面的英文段落翻译成中文，使其风格与中文的科普文章相似。
    <限制> 
    请根据英文内容直接翻译，维持原有的格式，不省略任何信息。
    <翻译前的原文> 
    {}

    <直接翻译> 
    """
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message.format(input_text)),
    ]

    res = model.invoke(messages)
    print(res)
    return res.content


if __name__ == "__main__":
    sections = split_long_file("../k8s-book-2024-en.md")
    translated_list = []
    process_total  = len(sections)
    process_count = 0
   
    for section in sections:
        process_count += 1
        logger.info(section)
        logger.info("########---------------------------------------------------------")
        logging.info(f"####processing: {process_count}/{process_total}")
        section_tanslated = do_translate(section)
        translated_list.append(section_tanslated)
        logger.info(section_tanslated)
        with open(f"sections/part_{process_count}.md", "w") as f_part:
            f_part.write(section_tanslated + "\n")
        
    with open("./cn.md", "w") as f:
        for trans in translated_list:
            f.write(trans + "\n")

            


