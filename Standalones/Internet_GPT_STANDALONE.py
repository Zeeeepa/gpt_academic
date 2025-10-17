#!/usr/bin/env python3
"""
CONSOLIDATED STANDALONE VERSION: gpt_academic_fresh
======================================================================

All dependencies have been recursively inlined.
This file is completely self-contained.

Original location: /tmp/gpt_academic_fresh
Generated: 2025-10-17 13:04:23
Modules included: 27
"""

# Standard Library Imports
# ============================================================================
import base64
import copy
import functools
import glob
import gzip
import html
import importlib
import inspect
import itertools
import json
import logging
import math
import mimetypes
import os
import pickle
import platform
import queue
import random
import re
import requests
import shutil
import subprocess
import sys
import textwrap
import threading
import time
import traceback
import uuid
import warnings
import zipfile

from __future__ import annotations
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from functools import lru_cache, wraps
from hashlib import md5
from itertools import zip_longest
from pathlib import Path
from sys import stdout
from textwrap import dedent
from typing import (
    Any,
    Dict,
    Generator,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union
)
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from xml.etree import ElementTree

# External Package Imports
# ============================================================================
import gradio
import markdown
import nltk
import tiktoken
import trafilatura
import uvicorn

from bs4 import BeautifulSoup
from latex2mathml.converter import convert as tex2mathml
from loguru import logger
from pymdownx.superfences import fence_code_format


# ============================================================================
# INLINED MODULE CODE
# ============================================================================


# ----------------------------------------------------------------------
# MODULE: crazy_functions.rag_fns.rag_file_support
# SOURCE: crazy_functions/rag_fns/rag_file_support.py
# ----------------------------------------------------------------------


supports_format = ['.csv', '.docx', '.epub', '.ipynb',  '.mbox', '.md', '.pdf',  '.txt', '.ppt', '.pptm', '.pptx', '.bat']

def convert_to_markdown(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())

    if ext in ['.docx', '.doc', '.pptx', '.ppt', '.pptm', '.xls', '.xlsx', '.csv', 'pdf']:
        try:
            # 创建输出Markdown文件路径
            md_path = os.path.splitext(file_path)[0] + '.md'
            # 使用markitdown工具将文件转换为Markdown
            command = f"markitdown {file_path} > {md_path}"
            subprocess.run(command, shell=True, check=True)
            print(f"已将{ext}文件转换为Markdown: {md_path}")
            return md_path
        except Exception as e:
            print(f"{ext}转Markdown失败: {str(e)}，将继续处理原文件")
            return file_path

    return file_path

# 修改后的 extract_text 函数，结合 SimpleDirectoryReader 和自定义解析逻辑
def extract_text(file_path):
    from llama_index.core import SimpleDirectoryReader
    _, ext = os.path.splitext(file_path.lower())

    # 使用 SimpleDirectoryReader 处理它支持的文件格式
    if ext in supports_format:
        try:
            reader = SimpleDirectoryReader(input_files=[file_path])
            print(f"Extracting text from {file_path} using SimpleDirectoryReader")
            documents = reader.load_data()
            print(f"Complete: Extracting text from {file_path} using SimpleDirectoryReader")
            buffer = [ doc.text for doc in documents ]
            return '\n'.join(buffer)
        except Exception as e:
            pass
    else:
        return '格式不支持'



# ----------------------------------------------------------------------
# MODULE: shared_utils.colorful
# SOURCE: shared_utils/colorful.py
# ----------------------------------------------------------------------


if platform.system()=="Linux":
    pass
else:
    from colorama import init
    init()

# Do you like the elegance of Chinese characters?
def print红(*kw,**kargs):
    print("\033[0;31m",*kw,"\033[0m",**kargs)
def print绿(*kw,**kargs):
    print("\033[0;32m",*kw,"\033[0m",**kargs)
def print黄(*kw,**kargs):
    print("\033[0;33m",*kw,"\033[0m",**kargs)
def print蓝(*kw,**kargs):
    print("\033[0;34m",*kw,"\033[0m",**kargs)
def print紫(*kw,**kargs):
    print("\033[0;35m",*kw,"\033[0m",**kargs)
def print靛(*kw,**kargs):
    print("\033[0;36m",*kw,"\033[0m",**kargs)

def print亮红(*kw,**kargs):
    print("\033[1;31m",*kw,"\033[0m",**kargs)
def print亮绿(*kw,**kargs):
    print("\033[1;32m",*kw,"\033[0m",**kargs)
def print亮黄(*kw,**kargs):
    print("\033[1;33m",*kw,"\033[0m",**kargs)
def print亮蓝(*kw,**kargs):
    print("\033[1;34m",*kw,"\033[0m",**kargs)
def print亮紫(*kw,**kargs):
    print("\033[1;35m",*kw,"\033[0m",**kargs)
def print亮靛(*kw,**kargs):
    print("\033[1;36m",*kw,"\033[0m",**kargs)

# Do you like the elegance of Chinese characters?
def sprint红(*kw):
    return "\033[0;31m"+' '.join(kw)+"\033[0m"
def sprint绿(*kw):
    return "\033[0;32m"+' '.join(kw)+"\033[0m"
def sprint黄(*kw):
    return "\033[0;33m"+' '.join(kw)+"\033[0m"
def sprint蓝(*kw):
    return "\033[0;34m"+' '.join(kw)+"\033[0m"
def sprint紫(*kw):
    return "\033[0;35m"+' '.join(kw)+"\033[0m"
def sprint靛(*kw):
    return "\033[0;36m"+' '.join(kw)+"\033[0m"
def sprint亮红(*kw):
    return "\033[1;31m"+' '.join(kw)+"\033[0m"
def sprint亮绿(*kw):
    return "\033[1;32m"+' '.join(kw)+"\033[0m"
def sprint亮黄(*kw):
    return "\033[1;33m"+' '.join(kw)+"\033[0m"
def sprint亮蓝(*kw):
    return "\033[1;34m"+' '.join(kw)+"\033[0m"
def sprint亮紫(*kw):
    return "\033[1;35m"+' '.join(kw)+"\033[0m"
def sprint亮靛(*kw):
    return "\033[1;36m"+' '.join(kw)+"\033[0m"

def log红(*kw,**kargs):
    logger.opt(depth=1).info(sprint红(*kw))
def log绿(*kw,**kargs):
    logger.opt(depth=1).info(sprint绿(*kw))
def log黄(*kw,**kargs):
    logger.opt(depth=1).info(sprint黄(*kw))
def log蓝(*kw,**kargs):
    logger.opt(depth=1).info(sprint蓝(*kw))
def log紫(*kw,**kargs):
    logger.opt(depth=1).info(sprint紫(*kw))
def log靛(*kw,**kargs):
    logger.opt(depth=1).info(sprint靛(*kw))

def log亮红(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮红(*kw))
def log亮绿(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮绿(*kw))
def log亮黄(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮黄(*kw))
def log亮蓝(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮蓝(*kw))
def log亮紫(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮紫(*kw))
def log亮靛(*kw,**kargs):
    logger.opt(depth=1).info(sprint亮靛(*kw))


# ----------------------------------------------------------------------
# MODULE: core_functional
# SOURCE: core_functional.py
# ----------------------------------------------------------------------

# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er

def get_core_functions():
    return {

        "学术语料润色": {
            # [1*] 前缀字符串，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等。
            #      这里填一个提示词字符串就行了，这里为了区分中英文情景搞复杂了一点
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, "
                                r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. "
                                r"Firstly, you should provide the polished paragraph (in English). "
                                r"Secondly, you should list all your modification and explain the reasons to do so in markdown table.",
                            text_show_chinese=
                                r"作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，"
                                r"同时分解长句，减少重复，并提供改进建议。请先提供文本的更正版本，然后在markdown表格中列出修改的内容，并给出修改的理由:"
                        ) + "\n\n",
            # [2*] 后缀字符串，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # [3] 按钮颜色 (可选参数，默认 secondary)
            "Color":    r"secondary",
            # [4] 按钮是否可见 (可选参数，默认 True，即可见)
            "Visible": True,
            # [5] 是否在触发时清除历史 (可选参数，默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False,
            # [6] 文本预处理 （可选参数，默认 None，举例：写个函数移除所有的换行符）
            "PreProcess": None,
            # [7] 模型选择 （可选参数。如不设置，则使用当前全局模型；如设置，则用指定模型覆盖全局模型。）
            # "ModelOverride": "gpt-3.5-turbo", # 主要用途：强制点击此基础功能按钮时，使用指定的模型。
        },


        "总结绘制脑图": {
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix":   '''"""\n\n''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":
                # dedent() 函数用于去除多行字符串的缩进
                dedent("\n\n"+r'''
                    """

                    使用mermaid flowchart对以上文本进行总结，概括上述段落的内容以及内在逻辑关系，例如：

                    以下是对以上文本的总结，以mermaid flowchart的形式展示：
                    ```mermaid
                    flowchart LR
                        A["节点名1"] --> B("节点名2")
                        B --> C{"节点名3"}
                        C --> D["节点名4"]
                        C --> |"箭头名1"| E["节点名5"]
                        C --> |"箭头名2"| F["节点名6"]
                    ```

                    注意：
                    （1）使用中文
                    （2）节点名字使用引号包裹，如["Laptop"]
                    （3）`|` 和 `"`之间不要存在空格
                    （4）根据情况选择flowchart LR（从左到右）或者flowchart TD（从上到下）
                '''),
        },


        "查找语法错误": {
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # 预处理：清除换行符
        },


        "中译英": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },


        "学术英中互译": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_chinese=
                                r"I want you to act as a scientific English-Chinese translator, "
                                r"I will provide you with some paragraphs in one language "
                                r"and your task is to accurately and academically translate the paragraphs only into the other language. "
                                r"Do not repeat the original provided paragraphs after translation. "
                                r"You should use artificial intelligence tools, "
                                r"such as natural language processing, and rhetorical knowledge "
                                r"and experience about effective writing techniques to reply. "
                                r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:",
                            text_show_english=
                                r"你是经验丰富的翻译，请把以下学术文章段落翻译成中文，"
                                r"并同时充分考虑中文的语法、清晰、简洁和整体可读性，"
                                r"必要时，你可以修改整个句子的顺序以确保翻译后的段落符合中文的语言习惯。"
                                r"你需要翻译的文本如下："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "英译中": {
            "Prefix":   r"翻译成地道的中文：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "找图片": {
            "Prefix":   r"我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，"
                        r"然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "解释代码": {
            "Prefix":   r"请解释以下代码：" + "\n```\n",
            "Suffix":   "\n```\n",
        },


        "参考文献转Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style."
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly."
                        r"Items need to be transformed:" + "\n\n",
            "Visible":  False,
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # 热更新prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional[additional_fn]:
            if core_functional[additional_fn]["PreProcess"] is not None:
                inputs = core_functional[additional_fn]["PreProcess"](inputs)  # 获取预处理函数（如果有的话）
        # 为字符串加上上面定义的前缀和后缀。
        inputs = apply_gpt_academic_string_mask_langbased(
            string = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"],
            lang_reference = inputs,
        )
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history

if __name__ == "__main__":
    t = get_core_functions()["总结绘制脑图"]
    print(t["Prefix"] + t["Suffix"])


# ----------------------------------------------------------------------
# MODULE: themes.theme
# SOURCE: themes/theme.py
# ----------------------------------------------------------------------




def load_dynamic_theme(THEME):
    adjust_dynamic_theme = None
    if THEME == "Chuanhu-Small-and-Beautiful":
        from .green import adjust_theme, advanced_css

        theme_declaration = (
            '<h2 align="center"  class="small">[Chuanhu-Small-and-Beautiful主题]</h2>'
        )
    elif THEME == "High-Contrast":
        from .contrast import adjust_theme, advanced_css

        theme_declaration = ""
    elif "/" in THEME:
        from .gradios import adjust_theme, advanced_css
        from .gradios import dynamic_set_theme

        adjust_dynamic_theme = dynamic_set_theme(THEME)
        theme_declaration = ""
    else:
        from .default import adjust_theme, advanced_css

        theme_declaration = ""
    return adjust_theme, advanced_css, theme_declaration, adjust_dynamic_theme


adjust_theme, advanced_css, theme_declaration, _ = load_dynamic_theme(get_conf("THEME"))


"""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
第 2 部分
cookie相关工具函数
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""
def assign_user_uuid(cookies):
    # 为每一位访问的用户赋予一个独一无二的uuid编码
    cookies.update({"uuid": uuid.uuid4()})
    return cookies


def to_cookie_str(d):
    # serialize the dictionary and encode it as a string
    serialized_dict = json.dumps(d)
    cookie_value = base64.b64encode(serialized_dict.encode('utf8')).decode("utf-8")
    return cookie_value


def from_cookie_str(c):
    # Decode the base64-encoded string and unserialize it into a dictionary
    serialized_dict = base64.b64decode(c.encode("utf-8"))
    serialized_dict.decode("utf-8")
    return json.loads(serialized_dict)


"""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
第 3 部分
内嵌的javascript代码（这部分代码会逐渐移动到common.js中）
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""

js_code_for_toggle_darkmode = """() => {
    if (document.querySelectorAll('.dark').length) {
        setCookie("js_darkmode_cookie", "False", 365);
        document.querySelectorAll('.dark').forEach(el => el.classList.remove('dark'));
    } else {
        setCookie("js_darkmode_cookie", "True", 365);
        document.querySelector('body').classList.add('dark');
    }
    document.querySelectorAll('code_pending_render').forEach(code => {code.remove();})
}"""


js_code_clear = """
(a,b)=>{
    return ["", ""];
}
"""


js_code_show_or_hide = """
(display_panel_arr)=>{
setTimeout(() => {
    // get conf
    display_panel_arr = get_checkbox_selected_items("cbs");

    ////////////////////// 输入清除键 ///////////////////////////
    let searchString = "输入清除键";
    let ele = "none";
    if (display_panel_arr.includes(searchString)) {
        let clearButton = document.getElementById("elem_clear");
        let clearButton2 = document.getElementById("elem_clear2");
        clearButton.style.display = "block";
        clearButton2.style.display = "block";
        setCookie("js_clearbtn_show_cookie", "True", 365);
    } else {
        let clearButton = document.getElementById("elem_clear");
        let clearButton2 = document.getElementById("elem_clear2");
        clearButton.style.display = "none";
        clearButton2.style.display = "none";
        setCookie("js_clearbtn_show_cookie", "False", 365);
    }

    ////////////////////// 基础功能区 ///////////////////////////
    searchString = "基础功能区";
    if (display_panel_arr.includes(searchString)) {
        ele = document.getElementById("basic-panel");
        ele.style.display = "block";
    } else {
        ele = document.getElementById("basic-panel");
        ele.style.display = "none";
    }

    ////////////////////// 函数插件区 ///////////////////////////
    searchString = "函数插件区";
    if (display_panel_arr.includes(searchString)) {
        ele = document.getElementById("plugin-panel");
        ele.style.display = "block";
    } else {
        ele = document.getElementById("plugin-panel");
        ele.style.display = "none";
    }

}, 50);
}
"""




# ----------------------------------------------------------------------
# MODULE: shared_utils.text_mask
# SOURCE: shared_utils/text_mask.py
# ----------------------------------------------------------------------


# 这段代码是使用Python编程语言中的re模块，即正则表达式库，来定义了一个正则表达式模式。
# 这个模式被编译成一个正则表达式对象，存储在名为const_extract_exp的变量中，以便于后续快速的匹配和查找操作。
# 这里解释一下正则表达式中的几个特殊字符：
# - . 表示任意单一字符。
# - * 表示前一个字符可以出现0次或多次。
# - ? 在这里用作非贪婪匹配，也就是说它会匹配尽可能少的字符。在(.*?)中，它确保我们匹配的任意文本是尽可能短的，也就是说，它会在</show_llm>和</show_render>标签之前停止匹配。
# - () 括号在正则表达式中表示捕获组。
# - 在这个例子中，(.*?)表示捕获任意长度的文本，直到遇到括号外部最近的限定符，即</show_llm>和</show_render>。

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=/1=-=-=-=-=-=-=-=-=-=-=-=-=-=/2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
const_extract_re = re.compile(
    r"<gpt_academic_string_mask><show_llm>(.*?)</show_llm><show_render>(.*?)</show_render></gpt_academic_string_mask>"
)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=/1=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-/2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
const_extract_langbased_re = re.compile(
    r"<gpt_academic_string_mask><lang_english>(.*?)</lang_english><lang_chinese>(.*?)</lang_chinese></gpt_academic_string_mask>",
    flags=re.DOTALL,
)

@lru_cache(maxsize=128)
def apply_gpt_academic_string_mask(string, mode="show_all"):
    """
    当字符串中有掩码tag时（<gpt_academic_string_mask><show_...>），根据字符串要给谁看（大模型，还是web渲染），对字符串进行处理，返回处理后的字符串
    示意图：https://mermaid.live/edit#pako:eNqlkUtLw0AUhf9KuOta0iaTplkIPlpduFJwoZEwJGNbzItpita2O6tF8QGKogXFtwu7cSHiq3-mk_oznFR8IYLgrGbuOd9hDrcCpmcR0GDW9ubNPKaBMDauuwI_A9M6YN-3y0bODwxsYos4BdMoBrTg5gwHF-d0mBH6-vqFQe58ed5m9XPW2uteX3Tubrj0ljLYcwxxR3h1zB43WeMs3G19yEM9uapDMe_NG9i2dagKw1Fee4c1D9nGEbtc-5n6HbNtJ8IyHOs8tbs7V2HrlDX2w2Y7XD_5haHEtQiNsOwfMVa_7TzsvrWIuJGo02qTrdwLk9gukQylHv3Afv1ML270s-HZUndrmW1tdA-WfvbM_jMFYuAQ6uCCxVdciTJ1CPLEITpo_GphypeouzXuw6XAmyi7JmgBLZEYlHwLB2S4gHMUO-9DH7tTnvf1CVoFFkBLSOk4QmlRTqpIlaWUHINyNFXjaQWpCYRURUKiWovBYo8X4ymEJFlECQUpqaQkJmuvWygPpg
    """
    if not string:
        return string
    if "<gpt_academic_string_mask>" not in string: # No need to process
        return string

    if mode == "show_all":
        return string
    if mode == "show_llm":
        string = const_extract_re.sub(r"\1", string)
    elif mode == "show_render":
        string = const_extract_re.sub(r"\2", string)
    else:
        raise ValueError("Invalid mode")
    return string


@lru_cache(maxsize=128)
def build_gpt_academic_masked_string(text_show_llm="", text_show_render=""):
    """
    根据字符串要给谁看（大模型，还是web渲染），生成带掩码tag的字符串
    """
    return f"<gpt_academic_string_mask><show_llm>{text_show_llm}</show_llm><show_render>{text_show_render}</show_render></gpt_academic_string_mask>"


@lru_cache(maxsize=128)
def apply_gpt_academic_string_mask_langbased(string, lang_reference):
    """
    当字符串中有掩码tag时（<gpt_academic_string_mask><lang_...>），根据语言，选择提示词，对字符串进行处理，返回处理后的字符串
    例如，如果lang_reference是英文，那么就只显示英文提示词，中文提示词就不显示了
    举例：
        输入1
            string = "注意，lang_reference这段文字是：<gpt_academic_string_mask><lang_english>英语</lang_english><lang_chinese>中文</lang_chinese></gpt_academic_string_mask>"
            lang_reference = "hello world"
        输出1
            "注意，lang_reference这段文字是：英语"

        输入2
            string = "注意，lang_reference这段文字是中文"   # 注意这里没有掩码tag，所以不会被处理
            lang_reference = "hello world"
        输出2
            "注意，lang_reference这段文字是中文"            # 原样返回
    """

    if "<gpt_academic_string_mask>" not in string: # No need to process
        return string

    def contains_chinese(string):
        chinese_regex = re.compile(u'[\u4e00-\u9fff]+')
        return chinese_regex.search(string) is not None

    mode = "english" if not contains_chinese(lang_reference) else "chinese"
    if mode == "english":
        string = const_extract_langbased_re.sub(r"\1", string)
    elif mode == "chinese":
        string = const_extract_langbased_re.sub(r"\2", string)
    else:
        raise ValueError("Invalid mode")
    return string


@lru_cache(maxsize=128)
def build_gpt_academic_masked_string_langbased(text_show_english="", text_show_chinese=""):
    """
    根据语言，选择提示词，对字符串进行处理，返回处理后的字符串
    """
    return f"<gpt_academic_string_mask><lang_english>{text_show_english}</lang_english><lang_chinese>{text_show_chinese}</lang_chinese></gpt_academic_string_mask>"


if __name__ == "__main__":
    # Test
    input_string = (
        "你好\n"
        + build_gpt_academic_masked_string(text_show_llm="mermaid", text_show_render="")
        + "你好\n"
    )
    print(
        apply_gpt_academic_string_mask(input_string, "show_llm")
    )  # Should print the strings with 'abc' in place of the academic mask tags
    print(
        apply_gpt_academic_string_mask(input_string, "show_render")
    )  # Should print the strings with 'xyz' in place of the academic mask tags



# ----------------------------------------------------------------------
# MODULE: shared_utils.advanced_markdown_format
# SOURCE: shared_utils/advanced_markdown_format.py
# ----------------------------------------------------------------------


markdown_extension_configs = {
    "mdx_math": {
        "enable_dollar_delimiter": True,
        "use_gitlab_delimiters": False,
    },
}

code_highlight_configs = {
    "pymdownx.superfences": {
        "css_class": "codehilite",
        "custom_fences": [
            {"name": "mermaid", "class": "mermaid", "format": fence_code_format}
        ],
    },
    "pymdownx.highlight": {
        "css_class": "codehilite",
        "guess_lang": True,
        # 'auto_title': True,
        # 'linenums': True
    },
}

code_highlight_configs_block_mermaid = {
    "pymdownx.superfences": {
        "css_class": "codehilite",
        # "custom_fences": [
        #     {"name": "mermaid", "class": "mermaid", "format": fence_code_format}
        # ],
    },
    "pymdownx.highlight": {
        "css_class": "codehilite",
        "guess_lang": True,
        # 'auto_title': True,
        # 'linenums': True
    },
}


mathpatterns = {
    r"(?<!\\|\$)(\$)([^\$]+)(\$)": {"allow_multi_lines": False},  #  $...$
    r"(?<!\\)(\$\$)([^\$]+)(\$\$)": {"allow_multi_lines": True},  # $$...$$
    r"(?<!\\)(\\\[)(.+?)(\\\])": {"allow_multi_lines": False},  # \[...\]
    r'(?<!\\)(\\\()(.+?)(\\\))': {'allow_multi_lines': False},                       # \(...\)
    # r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\2})': {'allow_multi_lines': True},  # \begin...\end
    # r'(?<!\\)(\$`)([^`]+)(`\$)': {'allow_multi_lines': False},                       # $`...`$
}

def tex2mathml_catch_exception(content, *args, **kwargs):
    try:
        content = tex2mathml(content, *args, **kwargs)
    except:
        content = content
    return content


def replace_math_no_render(match):
    content = match.group(1)
    if "mode=display" in match.group(0):
        content = content.replace("\n", "</br>")
        return f'<font color="#00FF00">$$</font><font color="#FF00FF">{content}</font><font color="#00FF00">$$</font>'
    else:
        return f'<font color="#00FF00">$</font><font color="#FF00FF">{content}</font><font color="#00FF00">$</font>'


def replace_math_render(match):
    content = match.group(1)
    if "mode=display" in match.group(0):
        if "\\begin{aligned}" in content:
            content = content.replace("\\begin{aligned}", "\\begin{array}")
            content = content.replace("\\end{aligned}", "\\end{array}")
            content = content.replace("&", " ")
        content = tex2mathml_catch_exception(content, display="block")
        return content
    else:
        return tex2mathml_catch_exception(content)


def markdown_bug_hunt(content):
    """
    解决一个mdx_math的bug（单$包裹begin命令时多余<script>）
    """
    content = content.replace(
        '<script type="math/tex">\n<script type="math/tex; mode=display">',
        '<script type="math/tex; mode=display">',
    )
    content = content.replace("</script>\n</script>", "</script>")
    return content


def is_equation(txt):
    """
    判定是否为公式 | 测试1 写出洛伦兹定律，使用tex格式公式 测试2 给出柯西不等式，使用latex格式 测试3 写出麦克斯韦方程组
    """
    if "```" in txt and "```reference" not in txt:
        return False
    if "$" not in txt and "\\[" not in txt:
        return False

    matches = []
    for pattern, property in mathpatterns.items():
        flags = re.ASCII | re.DOTALL if property["allow_multi_lines"] else re.ASCII
        matches.extend(re.findall(pattern, txt, flags))
    if len(matches) == 0:
        return False
    contain_any_eq = False
    illegal_pattern = re.compile(r"[^\x00-\x7F]|echo")
    for match in matches:
        if len(match) != 3:
            return False
        eq_canidate = match[1]
        if illegal_pattern.search(eq_canidate):
            return False
        else:
            contain_any_eq = True
    return contain_any_eq


def fix_markdown_indent(txt):
    # fix markdown indent
    if (" - " not in txt) or (". " not in txt):
        # do not need to fix, fast escape
        return txt
    # walk through the lines and fix non-standard indentation
    lines = txt.split("\n")
    pattern = re.compile(r"^\s+-")
    activated = False
    for i, line in enumerate(lines):
        if line.startswith("- ") or line.startswith("1. "):
            activated = True
        if activated and pattern.match(line):
            stripped_string = line.lstrip()
            num_spaces = len(line) - len(stripped_string)
            if (num_spaces % 4) == 3:
                num_spaces_should_be = math.ceil(num_spaces / 4) * 4
                lines[i] = " " * num_spaces_should_be + stripped_string
    return "\n".join(lines)


FENCED_BLOCK_RE = re.compile(
    dedent(
        r"""
        (?P<fence>^[ \t]*(?:~{3,}|`{3,}))[ ]*                      # opening fence
        ((\{(?P<attrs>[^\}\n]*)\})|                              # (optional {attrs} or
        (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
        (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
        \n                                                       # newline (end of opening fence)
        (?P<code>.*?)(?<=\n)                                     # the code block
        (?P=fence)[ ]*$                                          # closing fence
    """
    ),
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


def get_line_range(re_match_obj, txt):
    start_pos, end_pos = re_match_obj.regs[0]
    num_newlines_before = txt[: start_pos + 1].count("\n")
    line_start = num_newlines_before
    line_end = num_newlines_before + txt[start_pos:end_pos].count("\n") + 1
    return line_start, line_end


def fix_code_segment_indent(txt):
    lines = []
    change_any = False
    txt_tmp = txt
    while True:
        re_match_obj = FENCED_BLOCK_RE.search(txt_tmp)
        if not re_match_obj:
            break
        if len(lines) == 0:
            lines = txt.split("\n")

        # 清空 txt_tmp 对应的位置方便下次搜索
        start_pos, end_pos = re_match_obj.regs[0]
        txt_tmp = txt_tmp[:start_pos] + " " * (end_pos - start_pos) + txt_tmp[end_pos:]
        line_start, line_end = get_line_range(re_match_obj, txt)

        # 获取公共缩进
        shared_indent_cnt = 1e5
        for i in range(line_start, line_end):
            stripped_string = lines[i].lstrip()
            num_spaces = len(lines[i]) - len(stripped_string)
            if num_spaces < shared_indent_cnt:
                shared_indent_cnt = num_spaces

        # 修复缩进
        if (shared_indent_cnt < 1e5) and (shared_indent_cnt % 4) == 3:
            num_spaces_should_be = math.ceil(shared_indent_cnt / 4) * 4
            for i in range(line_start, line_end):
                add_n = num_spaces_should_be - shared_indent_cnt
                lines[i] = " " * add_n + lines[i]
            if not change_any:  # 遇到第一个
                change_any = True

    if change_any:
        return "\n".join(lines)
    else:
        return txt


def fix_dollar_sticking_bug(txt):
    """
    修复不标准的dollar公式符号的问题
    """
    txt_result = ""
    single_stack_height = 0
    double_stack_height = 0
    while True:
        while True:
            index = txt.find('$')

            if index == -1:
                txt_result += txt
                return txt_result

            if single_stack_height > 0:
                if txt[:(index+1)].find('\n') > 0 or txt[:(index+1)].find('<td>') > 0 or txt[:(index+1)].find('</td>') > 0:
                    logger.error('公式之中出现了异常 (Unexpect element in equation)')
                    single_stack_height = 0
                    txt_result += ' $'
                    continue

            if double_stack_height > 0:
                if txt[:(index+1)].find('\n\n') > 0:
                    logger.error('公式之中出现了异常 (Unexpect element in equation)')
                    double_stack_height = 0
                    txt_result += '$$'
                    continue

            is_double = (txt[index+1] == '$')
            if is_double:
                if single_stack_height != 0:
                    # add a padding
                    txt = txt[:(index+1)] + " " + txt[(index+1):]
                    continue
                if double_stack_height == 0:
                    double_stack_height = 1
                else:
                    double_stack_height = 0
                txt_result += txt[:(index+2)]
                txt = txt[(index+2):]
            else:
                if double_stack_height != 0:
                    # logger.info(txt[:(index)])
                    logger.info('发现异常嵌套公式')
                if single_stack_height == 0:
                    single_stack_height = 1
                else:
                    single_stack_height = 0
                    # logger.info(txt[:(index)])
                txt_result += txt[:(index+1)]
                txt = txt[(index+1):]
            break


def markdown_convertion_for_file(txt):
    """
    将Markdown格式的文本转换为HTML格式。如果包含数学公式，则先将公式转换为HTML格式。
    """
    from themes.theme import advanced_css
    pre = f"""
    <!DOCTYPE html><head><meta charset="utf-8"><title>GPT-Academic输出文档</title><style>{advanced_css}</style></head>
    <body>
    <div class="test_temp1" style="width:10%; height: 500px; float:left;"></div>
    <div class="test_temp2" style="width:80%;padding: 40px;float:left;padding-left: 20px;padding-right: 20px;box-shadow: rgba(0, 0, 0, 0.2) 0px 0px 8px 8px;border-radius: 10px;">
        <div class="markdown-body">
    """
    suf = """
        </div>
    </div>
    <div class="test_temp3" style="width:10%; height: 500px; float:left;"></div>
    </body>
    """

    if txt.startswith(pre) and txt.endswith(suf):
        # print('警告，输入了已经经过转化的字符串，二次转化可能出问题')
        return txt  # 已经被转化过，不需要再次转化

    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'
    txt = fix_markdown_indent(txt)
    convert_stage_1 = fix_dollar_sticking_bug(txt)
    # convert everything to html format
    convert_stage_2 = markdown.markdown(
        text=convert_stage_1,
        extensions=[
            "sane_lists",
            "tables",
            "mdx_math",
            "pymdownx.superfences",
            "pymdownx.highlight",
        ],
        extension_configs={**markdown_extension_configs, **code_highlight_configs},
    )


    def repl_fn(match):
        content = match.group(2)
        return f'<script type="math/tex">{content}</script>'

    pattern = "|".join([pattern for pattern, property in mathpatterns.items() if not property["allow_multi_lines"]])
    pattern = re.compile(pattern, flags=re.ASCII)
    convert_stage_3 = pattern.sub(repl_fn, convert_stage_2)

    convert_stage_4 = markdown_bug_hunt(convert_stage_3)

    # 2. convert to rendered equation
    convert_stage_5, n = re.subn(
        find_equation_pattern, replace_math_render, convert_stage_4, flags=re.DOTALL
    )
    # cat them together
    return pre + convert_stage_5 + suf

def compress_string(s):
    compress_string = gzip.compress(s.encode('utf-8'))
    return base64.b64encode(compress_string).decode()

def decompress_string(s):
    decoded_string = base64.b64decode(s)
    return gzip.decompress(decoded_string).decode('utf-8')

@lru_cache(maxsize=128)  # 使用 lru缓存 加快转换速度
def markdown_convertion(txt):
    """
    将Markdown格式的文本转换为HTML格式。如果包含数学公式，则先将公式转换为HTML格式。
    """
    pre = '<div class="markdown-body">'
    suf = "</div>"
    if txt.startswith(pre) and txt.endswith(suf):
        # print('警告，输入了已经经过转化的字符串，二次转化可能出问题')
        return txt  # 已经被转化过，不需要再次转化

    # 在文本中插入一个base64编码的原始文本，以便在复制时能够获得原始文本
    raw_text_encoded = compress_string(txt)
    raw_text_node = f'<div class="raw_text" style="display:none">{raw_text_encoded}</div><div class="message_tail" style="display:none"></div>'
    suf = raw_text_node + "</div>"

    # 用于查找数学公式的正则表达式
    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'

    txt = fix_markdown_indent(txt)
    # txt = fix_code_segment_indent(txt)
    if is_equation(txt):  # 有$标识的公式符号，且没有代码段```的标识
        # convert everything to html format
        split = markdown.markdown(text="---")
        convert_stage_1 = markdown.markdown(
            text=txt,
            extensions=[
                "sane_lists",
                "tables",
                "mdx_math",
                "pymdownx.superfences",
                "pymdownx.highlight",
            ],
            extension_configs={**markdown_extension_configs, **code_highlight_configs},
        )
        convert_stage_1 = markdown_bug_hunt(convert_stage_1)
        # 1. convert to easy-to-copy tex (do not render math)
        convert_stage_2_1, n = re.subn(
            find_equation_pattern,
            replace_math_no_render,
            convert_stage_1,
            flags=re.DOTALL,
        )
        # 2. convert to rendered equation
        convert_stage_2_2, n = re.subn(
            find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL
        )
        # cat them together
        return pre + convert_stage_2_1 + f"{split}" + convert_stage_2_2 + suf
    else:
        return (
            pre
            + markdown.markdown(
                txt,
                extensions=[
                    "sane_lists",
                    "tables",
                    "pymdownx.superfences",
                    "pymdownx.highlight",
                ],
                extension_configs=code_highlight_configs,
            )
            + suf
        )


def code_block_title_replace_format(match):
    lang = match.group(1)
    filename = match.group(2)
    return f"```{lang} {{title=\"{filename}\"}}\n"


def get_last_backticks_indent(text):
    # 从后向前查找最后一个 ```
    lines = text.splitlines()
    for line in reversed(lines):
        if '```' in line:
            # 计算前面的空格数量
            indent = len(line) - len(line.lstrip())
            return indent
    return 0 # 如果没找到返回0


@lru_cache(maxsize=16)  # 使用lru缓存
def close_up_code_segment_during_stream(gpt_reply):
    """
    在gpt输出代码的中途（输出了前面的```，但还没输出完后面的```），补上后面的```

    Args:
        gpt_reply (str): GPT模型返回的回复字符串。

    Returns:
        str: 返回一个新的字符串，将输出代码片段的“后面的```”补上。

    """
    if "```" not in gpt_reply:
        return gpt_reply

    # replace [```python:warp.py] to [```python {title="warp.py"}]
    pattern = re.compile(r"```([a-z]{1,12}):([^:\n]{1,35}\.([a-zA-Z^:\n]{1,3}))\n")
    if pattern.search(gpt_reply):
        gpt_reply = pattern.sub(code_block_title_replace_format, gpt_reply)

    if gpt_reply.endswith("```"):
        return gpt_reply

    # 排除了以上两个情况，我们
    segments = gpt_reply.split("```")
    n_mark = len(segments) - 1
    if n_mark % 2 == 1:
        try:
            num_padding = get_last_backticks_indent(gpt_reply)
        except:
            num_padding = 0
        return gpt_reply + "\n" + " "*num_padding + "```"  # 输出代码片段中！
    else:
        return gpt_reply


def special_render_issues_for_mermaid(text):
    # 用不太优雅的方式处理一个core_functional.py中出现的mermaid渲染特例：
    # 我不希望"总结绘制脑图"prompt中的mermaid渲染出来
    @lru_cache(maxsize=1)
    def get_special_case():
        from core_functional import get_core_functions
        special_case = get_core_functions()["总结绘制脑图"]["Suffix"]
        return special_case
    if text.endswith(get_special_case()): text = text.replace("```mermaid", "```")
    return text


def contain_html_tag(text):
    """
    判断文本中是否包含HTML标签。
    """
    pattern = r'</?([a-zA-Z0-9_]{3,16})>|<script\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
    return re.search(pattern, text) is not None


def contain_image(text):
    pattern = r'<br/><br/><div align="center"><img src="file=(.*?)" base64="(.*?)"></div>'
    return re.search(pattern, text) is not None


def compat_non_markdown_input(text):
    """
    改善非markdown输入的显示效果，例如将空格转换为&nbsp;，将换行符转换为</br>等。
    """
    if "```" in text:
        # careful input：markdown输入
        text = special_render_issues_for_mermaid(text)  # 处理特殊的渲染问题
        return text
    elif ("<" in text) and (">" in text) and contain_html_tag(text):
        # careful input：html输入
        if contain_image(text):
            return text
        else:
            escaped_text = html.escape(text)
            return escaped_text
    else:
        # whatever input：非markdown输入
        lines = text.split("\n")
        for i, line in enumerate(lines):
            lines[i] = lines[i].replace(" ", "&nbsp;")  # 空格转换为&nbsp;
        text = "</br>".join(lines)  # 换行符转换为</br>
        return text


@lru_cache(maxsize=128)  # 使用lru缓存
def simple_markdown_convertion(text):
    pre = '<div class="markdown-body">'
    suf = "</div>"
    if text.startswith(pre) and text.endswith(suf):
        return text  # 已经被转化过，不需要再次转化

    text = compat_non_markdown_input(text)    # 兼容非markdown输入
    text = markdown.markdown(
        text,
        extensions=["pymdownx.superfences", "tables", "pymdownx.highlight"],
        extension_configs=code_highlight_configs,
    )
    return pre + text + suf


def format_io(self, y):
    """
    将输入和输出解析为HTML格式。将y中最后一项的输入部分段落化，并将输出部分的Markdown和数学公式转换为HTML格式。
    """
    if y is None or y == []:
        return []
    i_ask, gpt_reply = y[-1]
    i_ask = apply_gpt_academic_string_mask(i_ask, mode="show_render")
    gpt_reply = apply_gpt_academic_string_mask(gpt_reply, mode="show_render")
    # 当代码输出半截的时候，试着补上后个```
    if gpt_reply is not None:
        gpt_reply = close_up_code_segment_during_stream(gpt_reply)
    # 处理提问与输出
    y[-1] = (
        # 输入部分
        None if i_ask is None else simple_markdown_convertion(i_ask),
        # 输出部分
        None if gpt_reply is None else markdown_convertion(gpt_reply),
    )
    return y


# ----------------------------------------------------------------------
# MODULE: shared_utils.key_pattern_manager
# SOURCE: shared_utils/key_pattern_manager.py
# ----------------------------------------------------------------------



pj = os.path.join
default_user_name = 'default_user'

# match openai keys
openai_regex = re.compile(
    r"sk-[a-zA-Z0-9_-]{48}$|" +
    r"sk-[a-zA-Z0-9_-]{92}$|" +
    r"sk-proj-[a-zA-Z0-9_-]{48}$|"+
    r"sk-proj-[a-zA-Z0-9_-]{124}$|"+
    r"sk-proj-[a-zA-Z0-9_-]{156}$|"+ #新版apikey位数不匹配故修改此正则表达式
    r"sess-[a-zA-Z0-9]{40}$"
)
def is_openai_api_key(key):
    CUSTOM_API_KEY_PATTERN = get_conf('CUSTOM_API_KEY_PATTERN')
    if len(CUSTOM_API_KEY_PATTERN) != 0:
        API_MATCH_ORIGINAL = re.match(CUSTOM_API_KEY_PATTERN, key)
    else:
        API_MATCH_ORIGINAL = openai_regex.match(key)
    return bool(API_MATCH_ORIGINAL)


def is_azure_api_key(key):
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_AZURE)


def is_api2d_key(key):
    API_MATCH_API2D = re.match(r"fk[a-zA-Z0-9]{6}-[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_API2D)

def is_openroute_api_key(key):
    API_MATCH_OPENROUTE = re.match(r"sk-or-v1-[a-zA-Z0-9]{64}$", key)
    return bool(API_MATCH_OPENROUTE)

def is_cohere_api_key(key):
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{40}$", key)
    return bool(API_MATCH_AZURE)


def is_any_api_key(key):
    # key 一般只包含字母、数字、下划线、逗号、中划线
    if not re.match(r"^[a-zA-Z0-9_\-,]+$", key):
        # 如果配置了 CUSTOM_API_KEY_PATTERN，再检查以下以免误杀
        if CUSTOM_API_KEY_PATTERN := get_conf('CUSTOM_API_KEY_PATTERN'):
            return bool(re.match(CUSTOM_API_KEY_PATTERN, key))
        return False

    if ',' in key:
        keys = key.split(',')
        for k in keys:
            if is_any_api_key(k): return True
        return False
    else:
        return is_openai_api_key(key) or is_api2d_key(key) or is_azure_api_key(key) or is_cohere_api_key(key)


def what_keys(keys):
    avail_key_list = {'OpenAI Key': 0, "Azure Key": 0, "API2D Key": 0}
    key_list = keys.split(',')

    for k in key_list:
        if is_openai_api_key(k):
            avail_key_list['OpenAI Key'] += 1

    for k in key_list:
        if is_api2d_key(k):
            avail_key_list['API2D Key'] += 1

    for k in key_list:
        if is_azure_api_key(k):
            avail_key_list['Azure Key'] += 1

    return f"检测到： OpenAI Key {avail_key_list['OpenAI Key']} 个, Azure Key {avail_key_list['Azure Key']} 个, API2D Key {avail_key_list['API2D Key']} 个"

def is_o_family_for_openai(llm_model):
    if not llm_model.startswith('o'):
        return False
    if llm_model in ['o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8']:
        return True
    if llm_model[:3] in ['o1-', 'o2-', 'o3-', 'o4-', 'o5-', 'o6-', 'o7-', 'o8-']:
        return True
    return False

def select_api_key(keys, llm_model):
    import random
    avail_key_list = []
    key_list = keys.split(',')

    if llm_model.startswith('gpt-') or llm_model.startswith('chatgpt-') or \
       llm_model.startswith('one-api-') or is_o_family_for_openai(llm_model):
        for k in key_list:
            if is_openai_api_key(k): avail_key_list.append(k)

    if llm_model.startswith('api2d-'):
        for k in key_list:
            if is_api2d_key(k): avail_key_list.append(k)

    if llm_model.startswith('azure-'):
        for k in key_list:
            if is_azure_api_key(k): avail_key_list.append(k)

    if llm_model.startswith('cohere-'):
        for k in key_list:
            if is_cohere_api_key(k): avail_key_list.append(k)
    
    if llm_model.startswith('openrouter-'):
        for k in key_list:
            if is_openroute_api_key(k): avail_key_list.append(k)

    if len(avail_key_list) == 0:
        raise RuntimeError(f"您提供的api-key不满足要求，不包含任何可用于{llm_model}的api-key。您可能选择了错误的模型或请求源（左上角更换模型菜单中可切换openai,azure,claude,cohere等请求源）。")

    api_key = random.choice(avail_key_list) # 随机负载均衡
    return api_key


def select_api_key_for_embed_models(keys, llm_model):
    import random
    avail_key_list = []
    key_list = keys.split(',')

    if llm_model.startswith('text-embedding-'):
        for k in key_list:
            if is_openai_api_key(k): avail_key_list.append(k)

    if len(avail_key_list) == 0:
        raise RuntimeError(f"您提供的api-key不满足要求，不包含任何可用于{llm_model}的api-key。您可能选择了错误的模型或请求源。")

    api_key = random.choice(avail_key_list) # 随机负载均衡
    return api_key



# ----------------------------------------------------------------------
# MODULE: shared_utils.config_loader
# SOURCE: shared_utils/config_loader.py
# ----------------------------------------------------------------------


pj = os.path.join
default_user_name = 'default_user'

def read_env_variable(arg, default_value):
    """
    环境变量可以是 `GPT_ACADEMIC_CONFIG`(优先)，也可以直接是`CONFIG`
    例如在windows cmd中，既可以写：
        set USE_PROXY=True
        set API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    也可以写：
        set GPT_ACADEMIC_USE_PROXY=True
        set GPT_ACADEMIC_API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set GPT_ACADEMIC_proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set GPT_ACADEMIC_AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set GPT_ACADEMIC_AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    """
    arg_with_prefix = "GPT_ACADEMIC_" + arg
    if arg_with_prefix in os.environ:
        env_arg = os.environ[arg_with_prefix]
    elif arg in os.environ:
        env_arg = os.environ[arg]
    else:
        raise KeyError
    log亮绿(f"[ENV_VAR] 尝试加载{arg}，默认值：{default_value} --> 修正值：{env_arg}")
    try:
        if isinstance(default_value, bool):
            env_arg = env_arg.strip()
            if env_arg == 'True': r = True
            elif env_arg == 'False': r = False
            else: log亮红('Expect `True` or `False`, but have:', env_arg); r = default_value
        elif isinstance(default_value, int):
            r = int(env_arg)
        elif isinstance(default_value, float):
            r = float(env_arg)
        elif isinstance(default_value, str):
            r = env_arg.strip()
        elif isinstance(default_value, dict):
            r = eval(env_arg)
        elif isinstance(default_value, list):
            r = eval(env_arg)
        elif default_value is None:
            assert arg == "proxies"
            r = eval(env_arg)
        else:
            log亮红(f"[ENV_VAR] 环境变量{arg}不支持通过环境变量设置! ")
            raise KeyError
    except:
        log亮红(f"[ENV_VAR] 环境变量{arg}加载失败! ")
        raise KeyError(f"[ENV_VAR] 环境变量{arg}加载失败! ")

    log亮绿(f"[ENV_VAR] 成功读取环境变量{arg}")
    return r


@lru_cache(maxsize=128)
def read_single_conf_with_lru_cache(arg):
    from shared_utils.key_pattern_manager import is_any_api_key
    try:
        # 优先级1. 获取环境变量作为配置
        default_ref = getattr(importlib.import_module('config'), arg) # 读取默认值作为数据类型转换的参考
        r = read_env_variable(arg, default_ref)
    except:
        try:
            # 优先级2. 获取config_private中的配置
            r = getattr(importlib.import_module('config_private'), arg)
        except:
            # 优先级3. 获取config中的配置
            r = getattr(importlib.import_module('config'), arg)

    # 在读取API_KEY时，检查一下是不是忘了改config
    if arg == 'API_URL_REDIRECT':
        oai_rd = r.get("https://api.openai.com/v1/chat/completions", None) # API_URL_REDIRECT填写格式是错误的，请阅读`https://github.com/binary-husky/gpt_academic/wiki/项目配置说明`
        if oai_rd and not oai_rd.endswith('/completions'):
            log亮红("\n\n[API_URL_REDIRECT] API_URL_REDIRECT填错了。请阅读`https://github.com/binary-husky/gpt_academic/wiki/项目配置说明`。如果您确信自己没填错，无视此消息即可。")
            time.sleep(5)
    if arg == 'API_KEY':
        log亮蓝(f"[API_KEY] 本项目现已支持OpenAI和Azure的api-key。也支持同时填写多个api-key，如API_KEY=\"openai-key1,openai-key2,azure-key3\"")
        log亮蓝(f"[API_KEY] 您既可以在config.py中修改api-key(s)，也可以在问题输入区输入临时的api-key(s)，然后回车键提交后即可生效。")
        if is_any_api_key(r):
            log亮绿(f"[API_KEY] 您的 API_KEY 是: {r[:15]}*** API_KEY 导入成功")
        else:
            log亮红(f"[API_KEY] 您的 API_KEY（{r[:15]}***）不满足任何一种已知的密钥格式，请在config文件中修改API密钥之后再运行（详见`https://github.com/binary-husky/gpt_academic/wiki/api_key`）。")
    if arg == 'proxies':
        if not read_single_conf_with_lru_cache('USE_PROXY'): r = None # 检查USE_PROXY，防止proxies单独起作用
        if r is None:
            log亮红('[PROXY] 网络代理状态：未配置。无代理状态下很可能无法访问OpenAI家族的模型。建议：检查USE_PROXY选项是否修改。')
        else:
            log亮绿('[PROXY] 网络代理状态：已配置。配置信息如下：', str(r))
            assert isinstance(r, dict), 'proxies格式错误，请注意proxies选项的格式，不要遗漏括号。'
    return r


@lru_cache(maxsize=128)
def get_conf(*args):
    """
    本项目的所有配置都集中在config.py中。 修改配置有三种方法，您只需要选择其中一种即可：
        - 直接修改config.py
        - 创建并修改config_private.py
        - 修改环境变量（修改docker-compose.yml等价于修改容器内部的环境变量）

    注意：如果您使用docker-compose部署，请修改docker-compose（等价于修改容器内部的环境变量）
    """
    res = []
    for arg in args:
        r = read_single_conf_with_lru_cache(arg)
        res.append(r)
    if len(res) == 1: return res[0]
    return res


def set_conf(key, value):
    from toolbox import read_single_conf_with_lru_cache
    read_single_conf_with_lru_cache.cache_clear()
    get_conf.cache_clear()
    os.environ[key] = str(value)
    altered = get_conf(key)
    return altered


def set_multi_conf(dic):
    for k, v in dic.items(): set_conf(k, v)
    return



# ----------------------------------------------------------------------
# MODULE: shared_utils.handle_upload
# SOURCE: shared_utils/handle_upload.py
# ----------------------------------------------------------------------


def html_local_file(file):
    base_path = os.path.dirname(__file__)  # 项目目录
    if os.path.exists(str(file)):
        file = f'file={file.replace(base_path, ".")}'
    return file


def html_local_img(__file, layout="left", max_width=None, max_height=None, md=True):
    style = ""
    if max_width is not None:
        style += f"max-width: {max_width};"
    if max_height is not None:
        style += f"max-height: {max_height};"
    __file = html_local_file(__file)
    a = f'<div align="{layout}"><img src="{__file}" style="{style}"></div>'
    if md:
        a = f"![{__file}]({__file})"
    return a


def file_manifest_filter_type(file_list, filter_: list = None):
    new_list = []
    if not filter_:
        filter_ = ["png", "jpg", "jpeg"]
    for file in file_list:
        if str(os.path.basename(file)).split(".")[-1] in filter_:
            new_list.append(html_local_img(file, md=False))
        else:
            new_list.append(file)
    return new_list


def zip_extract_member_new(self, member, targetpath, pwd):
    # 修复中文乱码的问题
    """Extract the ZipInfo object 'member' to a physical
        file on the path targetpath.
    """
    import zipfile
    if not isinstance(member, zipfile.ZipInfo):
        member = self.getinfo(member)

    # build the destination pathname, replacing
    # forward slashes to platform specific separators.
    arcname = member.filename.replace('/', os.path.sep)
    arcname = arcname.encode('cp437', errors='replace').decode('gbk', errors='replace')

    if os.path.altsep:
        arcname = arcname.replace(os.path.altsep, os.path.sep)
    # interpret absolute pathname as relative, remove drive letter or
    # UNC path, redundant separators, "." and ".." components.
    arcname = os.path.splitdrive(arcname)[1]
    invalid_path_parts = ('', os.path.curdir, os.path.pardir)
    arcname = os.path.sep.join(x for x in arcname.split(os.path.sep)
                                if x not in invalid_path_parts)
    if os.path.sep == '\\':
        # filter illegal characters on Windows
        arcname = self._sanitize_windows_name(arcname, os.path.sep)

    targetpath = os.path.join(targetpath, arcname)
    targetpath = os.path.normpath(targetpath)

    # Create all upper directories if necessary.
    upperdirs = os.path.dirname(targetpath)
    if upperdirs and not os.path.exists(upperdirs):
        os.makedirs(upperdirs)

    if member.is_dir():
        if not os.path.isdir(targetpath):
            os.mkdir(targetpath)
        return targetpath

    with self.open(member, pwd=pwd) as source, \
            open(targetpath, "wb") as target:
        shutil.copyfileobj(source, target)

    return targetpath


def safe_extract_rar(file_path, dest_dir):
    import rarfile
    import posixpath
    with rarfile.RarFile(file_path) as rf:
        os.makedirs(dest_dir, exist_ok=True)
        base_path = os.path.abspath(dest_dir)
        for file_info in rf.infolist():
            orig_filename = file_info.filename
            filename = posixpath.normpath(orig_filename).lstrip('/')
            # 路径遍历防护
            if '..' in filename or filename.startswith('../'):
                raise Exception(f"Attempted Path Traversal in {orig_filename}")
            # 符号链接防护
            if hasattr(file_info, 'is_symlink') and file_info.is_symlink():
                raise Exception(f"Attempted Symlink in {orig_filename}")
            # 构造完整目标路径
            target_path = os.path.join(base_path, filename)
            final_path = os.path.normpath(target_path)
            # 最终路径校验
            if not final_path.startswith(base_path):
                raise Exception(f"Attempted Path Traversal in {orig_filename}")
        rf.extractall(dest_dir)


def extract_archive(file_path, dest_dir):
    import zipfile
    import tarfile
    import os

    # Get the file extension of the input file
    file_extension = os.path.splitext(file_path)[1]

    # Extract the archive based on its extension
    if file_extension == ".zip":
        with zipfile.ZipFile(file_path, "r") as zipobj:
            zipobj._extract_member = lambda a,b,c: zip_extract_member_new(zipobj, a,b,c)    # 修复中文乱码的问题
            zipobj.extractall(path=dest_dir)
            logger.info("Successfully extracted zip archive to {}".format(dest_dir))

    elif file_extension in [".tar", ".gz", ".bz2"]:
        try:
            with tarfile.open(file_path, "r:*") as tarobj:
                # 清理提取路径，移除任何不安全的元素
                for member in tarobj.getmembers():
                    member_path = os.path.normpath(member.name)
                    full_path = os.path.join(dest_dir, member_path)
                    full_path = os.path.abspath(full_path)
                    if member.islnk() or member.issym():
                        raise Exception(f"Attempted Symlink in {member.name}")
                    if not full_path.startswith(os.path.abspath(dest_dir) + os.sep):
                        raise Exception(f"Attempted Path Traversal in {member.name}")

                tarobj.extractall(path=dest_dir)
                logger.info("Successfully extracted tar archive to {}".format(dest_dir))
        except tarfile.ReadError as e:
            if file_extension == ".gz":
                # 一些特别奇葩的项目，是一个gz文件，里面不是tar，只有一个tex文件
                import gzip
                with gzip.open(file_path, 'rb') as f_in:
                    with open(os.path.join(dest_dir, 'main.tex'), 'wb') as f_out:
                        f_out.write(f_in.read())
            else:
                raise e

    # 第三方库，需要预先pip install rarfile
    # 此外，Windows上还需要安装winrar软件，配置其Path环境变量，如"C:\Program Files\WinRAR"才可以
    elif file_extension == ".rar":
        try:
            import rarfile  # 用来检查rarfile是否安装，不要删除
            safe_extract_rar(file_path, dest_dir)
        except:
            logger.info("Rar format requires additional dependencies to install")
            return "<br/><br/>解压失败! 需要安装pip install rarfile来解压rar文件。建议：使用zip压缩格式。"

    # 第三方库，需要预先pip install py7zr
    elif file_extension == ".7z":
        try:
            import py7zr

            with py7zr.SevenZipFile(file_path, mode="r") as f:
                f.extractall(path=dest_dir)
                logger.info("Successfully extracted 7z archive to {}".format(dest_dir))
        except:
            logger.info("7z format requires additional dependencies to install")
            return "<br/><br/>解压失败! 需要安装pip install py7zr来解压7z文件"
    else:
        return ""
    return ""




# ----------------------------------------------------------------------
# MODULE: shared_utils.map_names
# SOURCE: shared_utils/map_names.py
# ----------------------------------------------------------------------

mapping_dic = {
    # "qianfan": "qianfan（文心一言大模型）",
    # "zhipuai": "zhipuai（智谱GLM4超级模型🔥）",
    # "gpt-4-1106-preview": "gpt-4-1106-preview（新调优版本GPT-4🔥）",
    # "gpt-4-vision-preview": "gpt-4-vision-preview（识图模型GPT-4V）",
}

rev_mapping_dic = {}
for k, v in mapping_dic.items():
    rev_mapping_dic[v] = k

def map_model_to_friendly_names(m):
    if m in mapping_dic:
        return mapping_dic[m]
    return m

def map_friendly_names_to_model(m):
    if m in rev_mapping_dic:
        return rev_mapping_dic[m]
    return m

def read_one_api_model_name(model: str):
    """return real model name and max_token.
    """
    max_token_pattern = r"\(max_token=(\d+)\)"
    match = re.search(max_token_pattern, model)
    if match:
        max_token_tmp = match.group(1)  # 获取 max_token 的值
        max_token_tmp = int(max_token_tmp)
        model = re.sub(max_token_pattern, "", model)  # 从原字符串中删除 "(max_token=...)"
    else:
        max_token_tmp = 4096
    return model, max_token_tmp


# ----------------------------------------------------------------------
# MODULE: shared_utils.connect_void_terminal
# SOURCE: shared_utils/connect_void_terminal.py
# ----------------------------------------------------------------------




def get_plugin_handle(plugin_name):
    """
    e.g. plugin_name = 'crazy_functions.Markdown_Translate->Markdown翻译指定语言'
    """
    import importlib

    assert (
        "->" in plugin_name
    ), "Example of plugin_name: crazy_functions.Markdown_Translate->Markdown翻译指定语言"
    module, fn_name = plugin_name.split("->")
    f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
    return f_hot_reload


def get_chat_handle():
    """
    Get chat function
    """
    from request_llms.bridge_all import predict_no_ui_long_connection

    return predict_no_ui_long_connection


def get_plugin_default_kwargs():
    """
    Get Plugin Default Arguments
    """
    from toolbox import ChatBotWithCookies, load_chat_cookies

    cookies = load_chat_cookies()
    llm_kwargs = {
        "api_key": cookies["api_key"],
        "llm_model": cookies["llm_model"],
        "top_p": 1.0,
        "max_length": None,
        "temperature": 1.0,
    }
    chatbot = ChatBotWithCookies(llm_kwargs)

    # txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request
    DEFAULT_FN_GROUPS_kwargs = {
        "main_input": "./README.md",
        "llm_kwargs": llm_kwargs,
        "plugin_kwargs": {},
        "chatbot_with_cookie": chatbot,
        "history": [],
        "system_prompt": "You are a good AI.",
        "user_request": None,
    }
    return DEFAULT_FN_GROUPS_kwargs


def get_chat_default_kwargs():
    """
    Get Chat Default Arguments
    """
    from toolbox import load_chat_cookies

    cookies = load_chat_cookies()
    llm_kwargs = {
        "api_key": cookies["api_key"],
        "llm_model": cookies["llm_model"],
        "top_p": 1.0,
        "max_length": None,
        "temperature": 1.0,
    }
    default_chat_kwargs = {
        "inputs": "Hello there, are you ready?",
        "llm_kwargs": llm_kwargs,
        "history": [],
        "sys_prompt": "You are AI assistant",
        "observe_window": None,
        "console_silence": False,
    }

    return default_chat_kwargs



# ----------------------------------------------------------------------
# MODULE: shared_utils.context_clip_policy
# SOURCE: shared_utils/context_clip_policy.py
# ----------------------------------------------------------------------


def get_token_num(txt, tokenizer):
    return len(tokenizer.encode(txt, disallowed_special=()))

def get_model_info():
    from request_llms.bridge_all import model_info
    return model_info

def clip_history(inputs, history, tokenizer, max_token_limit):
    """
    reduce the length of history by clipping.
    this function search for the longest entries to clip, little by little,
    until the number of token of history is reduced under threshold.

    通过裁剪来缩短历史记录的长度。
    此函数逐渐地搜索最长的条目进行剪辑，
    直到历史记录的标记数量降低到阈值以下。

    被动触发裁剪
    """
    import numpy as np

    input_token_num = get_token_num(inputs)

    if max_token_limit < 5000:
        output_token_expect = 256  # 4k & 2k models
    elif max_token_limit < 9000:
        output_token_expect = 512  # 8k models
    else:
        output_token_expect = 1024  # 16k & 32k models

    if input_token_num < max_token_limit * 3 / 4:
        # 当输入部分的token占比小于限制的3/4时，裁剪时
        # 1. 把input的余量留出来
        max_token_limit = max_token_limit - input_token_num
        # 2. 把输出用的余量留出来
        max_token_limit = max_token_limit - output_token_expect
        # 3. 如果余量太小了，直接清除历史
        if max_token_limit < output_token_expect:
            history = []
            return history
    else:
        # 当输入部分的token占比 > 限制的3/4时，直接清除历史
        history = []
        return history

    everything = [""]
    everything.extend(history)
    n_token = get_token_num("\n".join(everything))
    everything_token = [get_token_num(e) for e in everything]

    # 截断时的颗粒度
    delta = max(everything_token) // 16

    while n_token > max_token_limit:
        where = np.argmax(everything_token)
        encoded = tokenizer.encode(everything[where], disallowed_special=())
        clipped_encoded = encoded[: len(encoded) - delta]
        everything[where] = tokenizer.decode(clipped_encoded)[
            :-1
        ]  # -1 to remove the may-be illegal char
        everything_token[where] = get_token_num(everything[where])
        n_token = get_token_num("\n".join(everything))

    history = everything[1:]
    return history


def auto_context_clip_each_message(current, history):
    """
    clip_history 是被动触发的

    主动触发裁剪
    """
    context = history + [current]
    trigger_clip_token_len = get_conf('AUTO_CONTEXT_CLIP_TRIGGER_TOKEN_LEN')
    model_info = get_model_info()
    tokenizer = model_info['gpt-4']['tokenizer']
    # 只保留最近的128条记录，无论token长度，防止计算token时计算过长的时间
    max_round = get_conf('AUTO_CONTEXT_MAX_ROUND')
    char_len = sum([len(h) for h in context])
    if char_len < trigger_clip_token_len*2:
        # 不需要裁剪
        history = context[:-1]
        current = context[-1]
        return current, history
    if len(context) > max_round:
        context = context[-max_round:]
    # 计算各个历史记录的token长度
    context_token_num = [get_token_num(h, tokenizer) for h in context]
    context_token_num_old = copy.copy(context_token_num)
    total_token_num = total_token_num_old = sum(context_token_num)
    if total_token_num < trigger_clip_token_len:
        # 不需要裁剪
        history = context[:-1]
        current = context[-1]
        return current, history
    clip_token_len = trigger_clip_token_len * 0.85
    # 越长越先被裁，越靠后越先被裁
    max_clip_ratio: list[float] = get_conf('AUTO_CONTEXT_MAX_CLIP_RATIO')
    max_clip_ratio = list(reversed(max_clip_ratio))
    if len(context) > len(max_clip_ratio):
        # give up the oldest context
        context = context[-len(max_clip_ratio):]
        context_token_num = context_token_num[-len(max_clip_ratio):]
    if len(context) < len(max_clip_ratio):
        # match the length of two array
        max_clip_ratio = max_clip_ratio[-len(context):]
    
    # compute rank
    clip_prior_weight = [(token_num/clip_token_len + (len(context) - index)*0.1) for index, token_num in enumerate(context_token_num)]
    # print('clip_prior_weight', clip_prior_weight)
    # get sorted index of context_token_num, from largest to smallest
    sorted_index = sorted(range(len(context_token_num)), key=lambda k: clip_prior_weight[k], reverse=True)

    # pre compute space yield
    for index in sorted_index:
        print('index', index, f'current total {total_token_num}, target {clip_token_len}')
        if total_token_num < clip_token_len:
            # no need to clip
            break
        # clip room left
        clip_room_left = total_token_num - clip_token_len
        # get the clip ratio
        allowed_token_num_this_entry = max_clip_ratio[index] * clip_token_len
        if context_token_num[index] < allowed_token_num_this_entry:
            print('index', index, '[allowed] before', context_token_num[index], 'allowed', allowed_token_num_this_entry)
            continue

        token_to_clip = context_token_num[index] - allowed_token_num_this_entry
        if token_to_clip*0.85 > clip_room_left:
            print('index', index, '[careful clip] token_to_clip', token_to_clip, 'clip_room_left', clip_room_left)
            token_to_clip = clip_room_left

        token_percent_to_clip = token_to_clip / context_token_num[index]
        char_percent_to_clip = token_percent_to_clip
        text_this_entry = context[index]
        char_num_to_clip = int(len(text_this_entry) * char_percent_to_clip)
        if char_num_to_clip < 500:
            # 如果裁剪的字符数小于500，则不裁剪
            print('index', index, 'before', context_token_num[index], 'allowed', allowed_token_num_this_entry)
            continue
        char_num_to_clip += 200 # 稍微多加一点
        char_to_preseve = len(text_this_entry) - char_num_to_clip
        _half = int(char_to_preseve / 2)
        # 前半 + ... (content clipped because token overflows) ... + 后半
        text_this_entry_clip = text_this_entry[:_half] + \
                             " ... (content clipped because token overflows) ... " \
                             + text_this_entry[-_half:]
        context[index] = text_this_entry_clip
        post_clip_token_cnt = get_token_num(text_this_entry_clip, tokenizer)
        print('index', index, 'before', context_token_num[index], 'allowed', allowed_token_num_this_entry, 'after', post_clip_token_cnt)
        context_token_num[index] = post_clip_token_cnt
        total_token_num = sum(context_token_num)
    context_token_num_final = [get_token_num(h, tokenizer) for h in context]
    print('context_token_num_old', context_token_num_old)
    print('context_token_num_final', context_token_num_final)
    print('token change from', total_token_num_old, 'to', sum(context_token_num_final), 'target', clip_token_len)
    history = context[:-1]
    current = context[-1]
    return current, history


def auto_context_clip_search_optimal(current, history, promote_latest_long_message=False):
    """
    current: 当前消息
    history: 历史消息列表
    promote_latest_long_message: 是否特别提高最后一条长message的权重，避免过度裁剪

    主动触发裁剪
    """
    context = history + [current]
    trigger_clip_token_len = get_conf('AUTO_CONTEXT_CLIP_TRIGGER_TOKEN_LEN')
    model_info = get_model_info()
    tokenizer = model_info['gpt-4']['tokenizer']
    # 只保留最近的128条记录，无论token长度，防止计算token时计算过长的时间
    max_round = get_conf('AUTO_CONTEXT_MAX_ROUND')
    char_len = sum([len(h) for h in context])
    if char_len < trigger_clip_token_len:
        # 不需要裁剪
        history = context[:-1]
        current = context[-1]
        return current, history
    if len(context) > max_round:
        context = context[-max_round:]
    # 计算各个历史记录的token长度
    context_token_num = [get_token_num(h, tokenizer) for h in context]
    context_token_num_old = copy.copy(context_token_num)
    total_token_num = total_token_num_old = sum(context_token_num)
    if total_token_num < trigger_clip_token_len:
        # 不需要裁剪
        history = context[:-1]
        current = context[-1]
        return current, history
    clip_token_len = trigger_clip_token_len * 0.90
    max_clip_ratio: list[float] = get_conf('AUTO_CONTEXT_MAX_CLIP_RATIO')
    max_clip_ratio = list(reversed(max_clip_ratio))
    if len(context) > len(max_clip_ratio):
        # give up the oldest context
        context = context[-len(max_clip_ratio):]
        context_token_num = context_token_num[-len(max_clip_ratio):]
    if len(context) < len(max_clip_ratio):
        # match the length of two array
        max_clip_ratio = max_clip_ratio[-len(context):]

    _scale = _scale_init = 1.25
    token_percent_arr = [(token_num/clip_token_len) for index, token_num in enumerate(context_token_num)]

    # promote last long message, avoid clipping it too much
    if promote_latest_long_message:
        promote_weight_constant = 1.6
        promote_index = -1
        threshold = 0.50
        for index, token_percent in enumerate(token_percent_arr):
            if token_percent > threshold:
                promote_index = index
        if promote_index >= 0:
            max_clip_ratio[promote_index] = promote_weight_constant

    max_clip_ratio_arr = max_clip_ratio
    step = 0.05
    for i in range(int(_scale_init / step) - 1):
        _take = 0
        for max_clip, token_r in zip(max_clip_ratio_arr, token_percent_arr):
            _take += min(max_clip * _scale, token_r)
        if _take < 1.0:
            break
        _scale -= 0.05

    # print('optimal scale', _scale)
    # print([_scale * max_clip for max_clip in max_clip_ratio_arr])
    # print([token_r for token_r in token_percent_arr])
    # print([min(token_r, _scale * max_clip) for token_r, max_clip in zip(token_percent_arr, max_clip_ratio_arr)])
    eps = 0.05
    max_clip_ratio = [_scale * max_clip + eps for max_clip in max_clip_ratio_arr]

    # compute rank
    # clip_prior_weight_old = [(token_num/clip_token_len + (len(context) - index)*0.1) for index, token_num in enumerate(context_token_num)]
    clip_prior_weight = [ token_r / max_clip  for max_clip, token_r in zip(max_clip_ratio_arr, token_percent_arr)]

    # sorted_index_old = sorted(range(len(context_token_num)), key=lambda k: clip_prior_weight_old[k], reverse=True)
    # print('sorted_index_old', sorted_index_old)
    sorted_index = sorted(range(len(context_token_num)), key=lambda k: clip_prior_weight[k], reverse=True)
    # print('sorted_index', sorted_index)

    # pre compute space yield
    for index in sorted_index:
        # print('index', index, f'current total {total_token_num}, target {clip_token_len}')
        if total_token_num < clip_token_len:
            # no need to clip
            break
        # clip room left
        clip_room_left = total_token_num - clip_token_len
        # get the clip ratio
        allowed_token_num_this_entry = max_clip_ratio[index] * clip_token_len
        if context_token_num[index] < allowed_token_num_this_entry:
            # print('index', index, '[allowed] before', context_token_num[index], 'allowed', allowed_token_num_this_entry)
            continue

        token_to_clip = context_token_num[index] - allowed_token_num_this_entry
        if token_to_clip*0.85 > clip_room_left:
            # print('index', index, '[careful clip] token_to_clip', token_to_clip, 'clip_room_left', clip_room_left)
            token_to_clip = clip_room_left

        token_percent_to_clip = token_to_clip / context_token_num[index]
        char_percent_to_clip = token_percent_to_clip
        text_this_entry = context[index]
        char_num_to_clip = int(len(text_this_entry) * char_percent_to_clip)
        if char_num_to_clip < 500:
            # 如果裁剪的字符数小于500，则不裁剪
            # print('index', index, 'before', context_token_num[index], 'allowed', allowed_token_num_this_entry)
            continue
        eps = 200
        char_num_to_clip = char_num_to_clip + eps # 稍微多加一点
        char_to_preseve = len(text_this_entry) - char_num_to_clip
        _half = int(char_to_preseve / 2)
        # 前半 + ... (content clipped because token overflows) ... + 后半
        text_this_entry_clip = text_this_entry[:_half] + \
                             " ... (content clipped because token overflows) ... " \
                             + text_this_entry[-_half:]
        context[index] = text_this_entry_clip
        post_clip_token_cnt = get_token_num(text_this_entry_clip, tokenizer)
        # print('index', index, 'before', context_token_num[index], 'allowed', allowed_token_num_this_entry, 'after', post_clip_token_cnt)
        context_token_num[index] = post_clip_token_cnt
        total_token_num = sum(context_token_num)
    context_token_num_final = [get_token_num(h, tokenizer) for h in context]
    # print('context_token_num_old', context_token_num_old)
    # print('context_token_num_final', context_token_num_final)
    # print('token change from', total_token_num_old, 'to', sum(context_token_num_final), 'target', clip_token_len)
    history = context[:-1]
    current = context[-1]
    return current, history



# ----------------------------------------------------------------------
# MODULE: toolbox
# SOURCE: toolbox.py
# ----------------------------------------------------------------------


pj = os.path.join
default_user_name = "default_user"

"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
第一部分
函数插件输入输出接驳区
    - ChatBotWithCookies:   带Cookies的Chatbot类，为实现更多强大的功能做基础
    - ArgsGeneralWrapper:   装饰器函数，用于重组输入参数，改变输入参数的顺序与结构
    - update_ui:            刷新界面用 yield from update_ui(chatbot, history)
    - CatchException:       将插件中出的所有问题显示在界面上
    - HotReload:            实现插件的热更新
    - trimmed_format_exc:   打印traceback，为了安全而隐藏绝对地址
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


class ChatBotWithCookies(list):
    def __init__(self, cookie):
        """
        cookies = {
            'top_p': top_p,
            'temperature': temperature,
            'lock_plugin': bool,
            "files_to_promote": ["file1", "file2"],
            "most_recent_uploaded": {
                "path": "uploaded_path",
                "time": time.time(),
                "time_str": "timestr",
            }
        }
        """
        self._cookies = cookie

    def write_list(self, list):
        for t in list:
            self.append(t)

    def get_list(self):
        return [t for t in self]

    def get_cookies(self):
        return self._cookies

    def get_user(self):
        return self._cookies.get("user_name", default_user_name)

def ArgsGeneralWrapper(f):
    """
    装饰器函数ArgsGeneralWrapper，用于重组输入参数，改变输入参数的顺序与结构。
    该装饰器是大多数功能调用的入口。
    函数示意图：https://mermaid.live/edit#pako:eNqNVFtPGkEY_StkntoEDQtLoTw0sWqapjQxVWPabmOm7AiEZZcsQ9QiiW012qixqdeqqIn10geBh6ZR8PJnmAWe-hc6l3VhrWnLEzNzzvnO953ZyYOYoSIQAWOaMR5LQBN7hvoU3UN_g5iu7imAXEyT4wUF3Pd0dT3y9KGYYUJsmK8V0GPGs0-QjkyojZgwk0Fm82C2dVghX08U8EaoOHjOfoEMU0XmADRhOksVWnNLjdpM82qFzB6S5Q_WWsUhuqCc3JtAsVR_OoMnhyZwXgHWwbS1d4gnsLVZJp-P6mfVxveqAgqC70Jz_pQCOGDKM5xFdNNPDdilF6uSU_hOYqu4a3MHYDZLDzq5fodrC3PWcEaFGPUaRiqJWK_W9g9rvRITa4dhy_0nw67SiePMp3oSR6PPn41DGgllkvkizYwsrmtaejTFd8V4yekGmT1zqrt4XGlAy8WTuiPULF01LksZvukSajfQQRAxmYi5S0D81sDcyzapVdn6sYFHkjhhGyel3frVQnvsnbR23lEjlhIlaOJiFPWzU5G4tfNJo8ejwp47-TbvJkKKZvmxA6SKo16oaazJysfG6klr9T0pbTW2ZqzlL_XaT8fYbQLXe4mSmvoCZXMaa7FePW6s7jVqK9bujvse3WFjY5_Z4KfsA4oiPY4T7Drvn1tLJTbG1to1qR79ulgk89-oJbvZzbIwJty6u20LOReWa9BvwserUd9s9MIKc3x5TUWEoAhUyJK5y85w_yG-dFu_R9waoU7K581y8W_qLle35-rG9Nxcrz8QHRsc0K-r9NViYRT36KsFvCCNzDRMqvSVyzOKAnACpZECIvSvCs2UAhS9QHEwh43BST0GItjMIS_I8e-sLwnj9A262cxA_ZVh0OUY1LJiDSJ5MAEiUijYLUtBORR6KElyQPaCSRDpksNSd8AfluSgHPaFC17wjrOlbgbzyyFf4IFPDvoD_sJvnkdK-g
    """
    def decorated(request: gradio.Request, cookies:dict, max_length:int, llm_model:str,
                  txt:str, txt2:str, top_p:float, temperature:float, chatbot:list,
                  json_history:str, system_prompt:str, plugin_advanced_arg:dict, *args):
        txt_passon = txt
        history = json.loads(json_history) if json_history else []
        if txt == "" and txt2 != "": txt_passon = txt2
        # 引入一个有cookie的chatbot
        if request.username is not None:
            user_name = request.username
        else:
            user_name = default_user_name
        embed_model = get_conf("EMBEDDING_MODEL")
        cookies.update({
            'top_p': top_p,
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'embed_model': embed_model,
            'temperature': temperature,
            'user_name': user_name,
        })
        llm_kwargs = {
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'embed_model': embed_model,
            'top_p': top_p,
            'max_length': max_length,
            'temperature': temperature,
            'client_ip': request.client.host,
            'most_recent_uploaded': cookies.get('most_recent_uploaded')
        }
        if isinstance(plugin_advanced_arg, str):
            plugin_kwargs = {"advanced_arg": plugin_advanced_arg}
        else:
            plugin_kwargs = plugin_advanced_arg
        chatbot_with_cookie = ChatBotWithCookies(cookies)
        chatbot_with_cookie.write_list(chatbot)

        if cookies.get('lock_plugin', None) is None:
            # 正常状态
            if len(args) == 0:  # 插件通道
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            else:               # 对话通道，或者基础功能通道
                # 基础对话通道，或者基础功能通道
                if get_conf('AUTO_CONTEXT_CLIP_ENABLE'):
                    txt_passon, history = auto_context_clip(txt_passon, history)
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, *args)
        else:
            # 处理少数情况下的特殊插件的锁定状态
            module, fn_name = cookies['lock_plugin'].split('->')
            f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
            yield from f_hot_reload(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            # 判断一下用户是否错误地通过对话通道进入，如果是，则进行提醒
            final_cookies = chatbot_with_cookie.get_cookies()
            # len(args) != 0 代表“提交”键对话通道，或者基础功能通道
            if len(args) != 0 and 'files_to_promote' in final_cookies and len(final_cookies['files_to_promote']) > 0:
                chatbot_with_cookie.append(
                    ["检测到**滞留的缓存文档**，请及时处理。", "请及时点击“**保存当前对话**”获取所有滞留文档。"])
                yield from update_ui(chatbot_with_cookie, final_cookies['history'], msg="检测到被滞留的缓存文档")

    return decorated


def update_ui(chatbot:ChatBotWithCookies, history:list, msg:str="正常", **kwargs):  # 刷新界面
    """
    刷新用户界面
    """
    assert isinstance(history, list), "history必须是一个list"
    assert isinstance(
        chatbot, ChatBotWithCookies
    ), "在传递chatbot的过程中不要将其丢弃。必要时, 可用clear将其清空, 然后用for+append循环重新赋值。"
    cookies = chatbot.get_cookies()
    # 备份一份History作为记录
    cookies.update({"history": history})
    # 解决插件锁定时的界面显示问题
    if cookies.get("lock_plugin", None):
        label = (
            cookies.get("llm_model", "")
            + " | "
            + "正在锁定插件"
            + cookies.get("lock_plugin", None)
        )
        chatbot_gr = gradio.update(value=chatbot, label=label)
        if cookies.get("label", "") != label:
            cookies["label"] = label  # 记住当前的label
    elif cookies.get("label", None):
        chatbot_gr = gradio.update(value=chatbot, label=cookies.get("llm_model", ""))
        cookies["label"] = None  # 清空label
    else:
        chatbot_gr = chatbot

    history = [str(history_item) for history_item in history] # ensure all items are string
    json_history = json.dumps(history, ensure_ascii=False)
    yield cookies, chatbot_gr, json_history, msg


def update_ui_latest_msg(lastmsg:str, chatbot:ChatBotWithCookies, history:list, delay:float=1, msg:str="正常"):  # 刷新界面
    """
    刷新用户界面
    """
    if len(chatbot) == 0:
        chatbot.append(["update_ui_last_msg", lastmsg])
    chatbot[-1] = list(chatbot[-1])
    chatbot[-1][-1] = lastmsg
    yield from update_ui(chatbot=chatbot, history=history, msg=msg)
    time.sleep(delay)


def trimmed_format_exc():
    import os, traceback

    str = traceback.format_exc()
    current_path = os.getcwd()
    replace_path = "."
    return str.replace(current_path, replace_path)


def trimmed_format_exc_markdown():
    return '\n\n```\n' + trimmed_format_exc() + '```'


class FriendlyException(Exception):
    def generate_error_html(self):
        return dedent(f"""
            <div class="center-div" style="color: crimson;text-align: center;">
                {"<br>".join(self.args)}
            </div>
        """)


def CatchException(f):
    """
    装饰器函数，捕捉函数f中的异常并封装到一个生成器中返回，并显示到聊天当中。
    """

    @wraps(f)
    def decorated(main_input:str, llm_kwargs:dict, plugin_kwargs:dict,
                  chatbot_with_cookie:ChatBotWithCookies, history:list, *args, **kwargs):
        try:
            yield from f(main_input, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, *args, **kwargs)
        except FriendlyException as e:
            tb_str = '```\n' + trimmed_format_exc() + '```'
            if len(chatbot_with_cookie) == 0:
                chatbot_with_cookie.clear()
                chatbot_with_cookie.append(["插件调度异常:\n" + tb_str, None])
            chatbot_with_cookie[-1] = [chatbot_with_cookie[-1][0], e.generate_error_html()]
            yield from update_ui(chatbot=chatbot_with_cookie, history=history, msg=f'异常')  # 刷新界面
        except Exception as e:
            tb_str = '```\n' + trimmed_format_exc() + '```'
            if len(chatbot_with_cookie) == 0:
                chatbot_with_cookie.clear()
                chatbot_with_cookie.append(["插件调度异常", "异常原因"])
            chatbot_with_cookie[-1] = [chatbot_with_cookie[-1][0], f"[Local Message] 插件调用出错: \n\n{tb_str} \n"]
            yield from update_ui(chatbot=chatbot_with_cookie, history=history, msg=f'异常 {e}')  # 刷新界面

    return decorated


def HotReload(f):
    """
    HotReload的装饰器函数，用于实现Python函数插件的热更新。
    函数热更新是指在不停止程序运行的情况下，更新函数代码，从而达到实时更新功能。
    在装饰器内部，使用wraps(f)来保留函数的元信息，并定义了一个名为decorated的内部函数。
    内部函数通过使用importlib模块的reload函数和inspect模块的getmodule函数来重新加载并获取函数模块，
    然后通过getattr函数获取函数名，并在新模块中重新加载函数。
    最后，使用yield from语句返回重新加载过的函数，并在被装饰的函数上执行。
    最终，装饰器函数返回内部函数。这个内部函数可以将函数的原始定义更新为最新版本，并执行函数的新版本。
    """
    if get_conf("PLUGIN_HOT_RELOAD"):

        @wraps(f)
        def decorated(*args, **kwargs):
            fn_name = f.__name__
            f_hot_reload = getattr(importlib.reload(inspect.getmodule(f)), fn_name)
            yield from f_hot_reload(*args, **kwargs)

        return decorated
    else:
        return f


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
第二部分
其他小工具:
    - write_history_to_file:    将结果写入markdown文件中
    - regular_txt_to_markdown:  将普通文本转换为Markdown格式的文本。
    - report_exception:         向chatbot中添加简单的意外错误信息
    - text_divide_paragraph:    将文本按照段落分隔符分割开，生成带有段落标签的HTML代码。
    - markdown_convertion:      用多种方式组合，将markdown转化为好看的html
    - format_io:                接管gradio默认的markdown处理方式
    - on_file_uploaded:         处理文件的上传（自动解压）
    - on_report_generated:      将生成的报告自动投射到文件上传区
    - clip_history:             当历史上下文过长时，自动截断
    - get_conf:                 获取设置
    - select_api_key:           根据当前的模型类别，抽取可用的api-key
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def get_reduce_token_percent(text:str):
    """
    * 此函数未来将被弃用
    """
    try:
        # text = "maximum context length is 4097 tokens. However, your messages resulted in 4870 tokens"
        pattern = r"(\d+)\s+tokens\b"
        match = re.findall(pattern, text)
        EXCEED_ALLO = 500  # 稍微留一点余地，否则在回复时会因余量太少出问题
        max_limit = float(match[0]) - EXCEED_ALLO
        current_tokens = float(match[1])
        ratio = max_limit / current_tokens
        assert ratio > 0 and ratio < 1
        return ratio, str(int(current_tokens - max_limit))
    except:
        return 0.5, "不详"


def write_history_to_file(
    history:list, file_basename:str=None, file_fullname:str=None, auto_caption:bool=True
):
    """
    将对话记录history以Markdown格式写入文件中。如果没有指定文件名，则使用当前时间生成文件名。
    """
    import os
    import time

    if file_fullname is None:
        if file_basename is not None:
            file_fullname = pj(get_log_folder(), file_basename)
        else:
            file_fullname = pj(get_log_folder(), f"GPT-Academic-{gen_time_str()}.md")
    os.makedirs(os.path.dirname(file_fullname), exist_ok=True)
    with open(file_fullname, "w", encoding="utf8") as f:
        f.write("# GPT-Academic Report\n")
        for i, content in enumerate(history):
            try:
                if type(content) != str:
                    content = str(content)
            except:
                continue
            if i % 2 == 0 and auto_caption:
                f.write("## ")
            try:
                f.write(content)
            except:
                # remove everything that cannot be handled by utf8
                f.write(content.encode("utf-8", "ignore").decode())
            f.write("\n\n")
    res = os.path.abspath(file_fullname)
    return res


def regular_txt_to_markdown(text:str):
    """
    将普通文本转换为Markdown格式的文本。
    """
    text = text.replace("\n", "\n\n")
    text = text.replace("\n\n\n", "\n\n")
    text = text.replace("\n\n\n", "\n\n")
    return text


def report_exception(chatbot:ChatBotWithCookies, history:list, a:str, b:str):
    """
    向chatbot中添加错误信息
    """
    chatbot.append((a, b))
    history.extend([a, b])


def find_free_port()->int:
    """
    返回当前系统中可用的未使用端口。
    """
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def find_recent_files(directory:str)->List[str]:
    """
    Find files that is created with in one minutes under a directory with python, write a function
    """
    import os
    import time

    current_time = time.time()
    one_minute_ago = current_time - 60
    recent_files = []
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    for filename in os.listdir(directory):
        file_path = pj(directory, filename)
        if file_path.endswith(".log"):
            continue
        created_time = os.path.getmtime(file_path)
        if created_time >= one_minute_ago:
            if os.path.isdir(file_path):
                continue
            recent_files.append(file_path)

    return recent_files


def file_already_in_downloadzone(file:str, user_path:str):
    try:
        parent_path = os.path.abspath(user_path)
        child_path = os.path.abspath(file)
        if os.path.samefile(os.path.commonpath([parent_path, child_path]), parent_path):
            return True
        else:
            return False
    except:
        return False


def promote_file_to_downloadzone(file:str, rename_file:str=None, chatbot:ChatBotWithCookies=None):
    # 将文件复制一份到下载区
    import shutil

    if chatbot is not None:
        user_name = get_user(chatbot)
    else:
        user_name = default_user_name
    if not os.path.exists(file):
        raise FileNotFoundError(f"文件{file}不存在")
    user_path = get_log_folder(user_name, plugin_name=None)
    if file_already_in_downloadzone(file, user_path):
        new_path = file
    else:
        user_path = get_log_folder(user_name, plugin_name="downloadzone")
        if rename_file is None:
            rename_file = f"{gen_time_str()}-{os.path.basename(file)}"
        new_path = pj(user_path, rename_file)
        # 如果已经存在，先删除
        if os.path.exists(new_path) and not os.path.samefile(new_path, file):
            os.remove(new_path)
        # 把文件复制过去
        if not os.path.exists(new_path):
            shutil.copyfile(file, new_path)
    # 将文件添加到chatbot cookie中
    if chatbot is not None:
        if "files_to_promote" in chatbot._cookies:
            current = chatbot._cookies["files_to_promote"]
        else:
            current = []
        if new_path not in current:  # 避免把同一个文件添加多次
            chatbot._cookies.update({"files_to_promote": [new_path] + current})
    return new_path


def disable_auto_promotion(chatbot:ChatBotWithCookies):
    chatbot._cookies.update({"files_to_promote": []})
    return


def del_outdated_uploads(outdate_time_seconds:float, target_path_base:str=None):
    if target_path_base is None:
        user_upload_dir = get_conf("PATH_PRIVATE_UPLOAD")
    else:
        user_upload_dir = target_path_base
    current_time = time.time()
    one_hour_ago = current_time - outdate_time_seconds
    # Get a list of all subdirectories in the user_upload_dir folder
    # Remove subdirectories that are older than one hour
    for subdirectory in glob.glob(f"{user_upload_dir}/*"):
        subdirectory_time = os.path.getmtime(subdirectory)
        if subdirectory_time < one_hour_ago:
            try:
                shutil.rmtree(subdirectory)
            except:
                pass
    return


def to_markdown_tabs(head: list, tabs: list, alignment=":---:", column=False, omit_path=None):
    """
    Args:
        head: 表头：[]
        tabs: 表值：[[列1], [列2], [列3], [列4]]
        alignment: :--- 左对齐， :---: 居中对齐， ---: 右对齐
        column: True to keep data in columns, False to keep data in rows (default).
    Returns:
        A string representation of the markdown table.
    """
    if column:
        transposed_tabs = list(map(list, zip(*tabs)))
    else:
        transposed_tabs = tabs
    # Find the maximum length among the columns
    max_len = max(len(column) for column in transposed_tabs)

    tab_format = "| %s "
    tabs_list = "".join([tab_format % i for i in head]) + "|\n"
    tabs_list += "".join([tab_format % alignment for i in head]) + "|\n"

    for i in range(max_len):
        row_data = [tab[i] if i < len(tab) else "" for tab in transposed_tabs]
        row_data = file_manifest_filter_type(row_data, filter_=None)
        # for dat in row_data:
        #     if (omit_path is not None) and os.path.exists(dat):
        #         dat = os.path.relpath(dat, omit_path)
        tabs_list += "".join([tab_format % i for i in row_data]) + "|\n"

    return tabs_list


def on_file_uploaded(
    request: gradio.Request, files:List[str], chatbot:ChatBotWithCookies,
    txt:str, txt2:str, checkboxes:List[str], cookies:dict
):
    """
    当文件被上传时的回调函数
    """
    if len(files) == 0:
        return chatbot, txt

    # 创建工作路径
    user_name = default_user_name if not request.username else request.username
    time_tag = gen_time_str()
    target_path_base = get_upload_folder(user_name, tag=time_tag)
    os.makedirs(target_path_base, exist_ok=True)

    # 移除过时的旧文件从而节省空间&保护隐私
    outdate_time_seconds = 3600  # 一小时
    del_outdated_uploads(outdate_time_seconds, get_upload_folder(user_name))

    # 逐个文件转移到目标路径
    upload_msg = ""
    for file in files:
        file_origin_name = os.path.basename(file.orig_name)
        this_file_path = pj(target_path_base, file_origin_name)
        shutil.move(file.name, this_file_path)
        upload_msg += extract_archive(
            file_path=this_file_path, dest_dir=this_file_path + ".extract"
        )

    # 整理文件集合 输出消息
    files = glob.glob(f"{target_path_base}/**/*", recursive=True)
    moved_files = [fp for fp in files]
    max_file_to_show = 10
    if len(moved_files) > max_file_to_show:
        moved_files = moved_files[:max_file_to_show//2] + [f'... ( 📌省略{len(moved_files) - max_file_to_show}个文件的显示 ) ...'] + \
                      moved_files[-max_file_to_show//2:]
    moved_files_str = to_markdown_tabs(head=["文件"], tabs=[moved_files], omit_path=target_path_base)
    chatbot.append(
        [
            "我上传了文件，请查收",
            f"[Local Message] 收到以下文件 （上传到路径：{target_path_base}）: " +
            f"\n\n{moved_files_str}" +
            f"\n\n调用路径参数已自动修正到: \n\n{txt}" +
            f"\n\n现在您点击任意函数插件时，以上文件将被作为输入参数" +
            upload_msg,
        ]
    )

    txt, txt2 = target_path_base, ""
    if "浮动输入区" in checkboxes:
        txt, txt2 = txt2, txt

    # 记录近期文件
    cookies.update(
        {
            "most_recent_uploaded": {
                "path": target_path_base,
                "time": time.time(),
                "time_str": time_tag,
            }
        }
    )
    return chatbot, txt, txt2, cookies


def generate_file_link(report_files:List[str]):
    file_links = ""
    for f in report_files:
        file_links += (
            f'<br/><a href="file={os.path.abspath(f)}" target="_blank">{f}</a>'
        )
    return file_links


def on_report_generated(cookies:dict, files:List[str], chatbot:ChatBotWithCookies):
    if "files_to_promote" in cookies:
        report_files = cookies["files_to_promote"]
        cookies.pop("files_to_promote")
    else:
        report_files = []
    if len(report_files) == 0:
        return cookies, None, chatbot
    file_links = ""
    for f in report_files:
        file_links += (
            f'<br/><a href="file={os.path.abspath(f)}" target="_blank">{f}</a>'
        )
    chatbot.append([None, f"已经添加到右侧“文件下载区”（可能处于折叠状态），请查收。您也可以点击以下链接直接下载：{file_links}"])
    return cookies, report_files, chatbot


def load_chat_cookies():
    API_KEY, LLM_MODEL, AZURE_API_KEY = get_conf(
        "API_KEY", "LLM_MODEL", "AZURE_API_KEY"
    )
    AZURE_CFG_ARRAY, NUM_CUSTOM_BASIC_BTN = get_conf(
        "AZURE_CFG_ARRAY", "NUM_CUSTOM_BASIC_BTN"
    )

    # deal with azure openai key
    if is_any_api_key(AZURE_API_KEY):
        if is_any_api_key(API_KEY):
            API_KEY = API_KEY + "," + AZURE_API_KEY
        else:
            API_KEY = AZURE_API_KEY
    if len(AZURE_CFG_ARRAY) > 0:
        for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
            if not azure_model_name.startswith("azure"):
                raise ValueError("AZURE_CFG_ARRAY中配置的模型必须以azure开头")
            AZURE_API_KEY_ = azure_cfg_dict["AZURE_API_KEY"]
            if is_any_api_key(AZURE_API_KEY_):
                if is_any_api_key(API_KEY):
                    API_KEY = API_KEY + "," + AZURE_API_KEY_
                else:
                    API_KEY = AZURE_API_KEY_

    customize_fn_overwrite_ = {}
    for k in range(NUM_CUSTOM_BASIC_BTN):
        customize_fn_overwrite_.update(
            {
                "自定义按钮"
                + str(k + 1): {
                    "Title": r"",
                    "Prefix": r"请在自定义菜单中定义提示词前缀.",
                    "Suffix": r"请在自定义菜单中定义提示词后缀",
                }
            }
        )

    EMBEDDING_MODEL = get_conf("EMBEDDING_MODEL")
    return {
        "api_key": API_KEY,
        "llm_model": LLM_MODEL,
        "embed_model": EMBEDDING_MODEL,
        "customize_fn_overwrite": customize_fn_overwrite_,
    }


def clear_line_break(txt):
    txt = txt.replace("\n", " ")
    txt = txt.replace("  ", " ")
    txt = txt.replace("  ", " ")
    return txt


class DummyWith:
    """
    这段代码定义了一个名为DummyWith的空上下文管理器，
    它的作用是……额……就是不起作用，即在代码结构不变得情况下取代其他的上下文管理器。
    上下文管理器是一种Python对象，用于与with语句一起使用，
    以确保一些资源在代码块执行期间得到正确的初始化和清理。
    上下文管理器必须实现两个方法，分别为 __enter__()和 __exit__()。
    在上下文执行开始的情况下，__enter__()方法会在代码块被执行前被调用，
    而在上下文执行结束时，__exit__()方法则会被调用。
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return


def run_gradio_in_subpath(demo, auth, port, custom_path):
    """
    把gradio的运行地址更改到指定的二次路径上
    """

    def is_path_legal(path: str) -> bool:
        """
        check path for sub url
        path: path to check
        return value: do sub url wrap
        """
        if path == "/":
            return True
        if len(path) == 0:
            logger.info(
                "illegal custom path: {}\npath must not be empty\ndeploy on root url".format(
                    path
                )
            )
            return False
        if path[0] == "/":
            if path[1] != "/":
                logger.info("deploy on sub-path {}".format(path))
                return True
            return False
        logger.info(
            "illegal custom path: {}\npath should begin with '/'\ndeploy on root url".format(
                path
            )
        )
        return False

    if not is_path_legal(custom_path):
        raise RuntimeError("Illegal custom path")
    import uvicorn
    import gradio as gr
    from fastapi import FastAPI

    app = FastAPI()
    if custom_path != "/":

        @app.get("/")
        def read_main():
            return {"message": f"Gradio is running at: {custom_path}"}

    app = gr.mount_gradio_app(app, demo, path=custom_path)
    uvicorn.run(app, host="0.0.0.0", port=port)  # , auth=auth

def auto_context_clip(current, history, policy='search_optimal'):
    if policy == 'each_message':
        return auto_context_clip_each_message(current, history)
    elif policy == 'search_optimal':
        return auto_context_clip_search_optimal(current, history)
    else:
        raise RuntimeError(f"未知的自动上下文裁剪策略: {policy}。")


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
第三部分
其他小工具:
    - zip_folder:    把某个路径下所有文件压缩，然后转移到指定的另一个路径中（gpt写的）
    - gen_time_str:  生成时间戳
    - ProxyNetworkActivate: 临时地启动代理网络（如果有）
    - objdump/objload: 快捷的调试函数
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def zip_folder(source_folder, dest_folder, zip_name):
    import zipfile
    import os

    # Make sure the source folder exists
    if not os.path.exists(source_folder):
        logger.info(f"{source_folder} does not exist")
        return

    # Make sure the destination folder exists
    if not os.path.exists(dest_folder):
        logger.info(f"{dest_folder} does not exist")
        return

    # Create the name for the zip file
    zip_file = pj(dest_folder, zip_name)

    # Create a ZipFile object
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source folder and add files to the zip file
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                filepath = pj(foldername, filename)
                zipf.write(filepath, arcname=os.path.relpath(filepath, source_folder))

    # Move the zip file to the destination folder (if it wasn't already there)
    if os.path.dirname(zip_file) != dest_folder:
        os.rename(zip_file, pj(dest_folder, os.path.basename(zip_file)))
        zip_file = pj(dest_folder, os.path.basename(zip_file))

    logger.info(f"Zip file created at {zip_file}")


def zip_result(folder):
    t = gen_time_str()
    zip_folder(folder, get_log_folder(), f"{t}-result.zip")
    return pj(get_log_folder(), f"{t}-result.zip")


def gen_time_str():
    import time

    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def get_log_folder(user=default_user_name, plugin_name="shared"):
    if user is None:
        user = default_user_name
    PATH_LOGGING = get_conf("PATH_LOGGING")
    if plugin_name is None:
        _dir = pj(PATH_LOGGING, user)
    else:
        _dir = pj(PATH_LOGGING, user, plugin_name)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir


def get_upload_folder(user=default_user_name, tag=None):
    PATH_PRIVATE_UPLOAD = get_conf("PATH_PRIVATE_UPLOAD")
    if user is None:
        user = default_user_name
    if tag is None or len(tag) == 0:
        target_path_base = pj(PATH_PRIVATE_UPLOAD, user)
    else:
        target_path_base = pj(PATH_PRIVATE_UPLOAD, user, tag)
    return target_path_base


def is_the_upload_folder(string):
    PATH_PRIVATE_UPLOAD = get_conf("PATH_PRIVATE_UPLOAD")
    pattern = r"^PATH_PRIVATE_UPLOAD[\\/][A-Za-z0-9_-]+[\\/]\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$"
    pattern = pattern.replace("PATH_PRIVATE_UPLOAD", PATH_PRIVATE_UPLOAD)
    if re.match(pattern, string):
        return True
    else:
        return False


def get_user(chatbotwithcookies:ChatBotWithCookies):
    return chatbotwithcookies._cookies.get("user_name", default_user_name)


class ProxyNetworkActivate:
    """
    这段代码定义了一个名为ProxyNetworkActivate的空上下文管理器, 用于给一小段代码上代理
    """

    def __init__(self, task=None) -> None:
        self.task = task
        if not task:
            # 不给定task, 那么我们默认代理生效
            self.valid = True
        else:
            # 给定了task, 我们检查一下
            from toolbox import get_conf

            WHEN_TO_USE_PROXY = get_conf("WHEN_TO_USE_PROXY")
            self.valid = task in WHEN_TO_USE_PROXY

    def __enter__(self):
        if not self.valid:
            return self
        from toolbox import get_conf

        proxies = get_conf("proxies")
        if "no_proxy" in os.environ:
            os.environ.pop("no_proxy")
        if proxies is not None:
            if "http" in proxies:
                os.environ["HTTP_PROXY"] = proxies["http"]
            if "https" in proxies:
                os.environ["HTTPS_PROXY"] = proxies["https"]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ["no_proxy"] = "*"
        if "HTTP_PROXY" in os.environ:
            os.environ.pop("HTTP_PROXY")
        if "HTTPS_PROXY" in os.environ:
            os.environ.pop("HTTPS_PROXY")
        return


def Singleton(cls):
    """
    一个单实例装饰器
    """
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def get_pictures_list(path):
    file_manifest = [f for f in glob.glob(f"{path}/**/*.jpg", recursive=True)]
    file_manifest += [f for f in glob.glob(f"{path}/**/*.jpeg", recursive=True)]
    file_manifest += [f for f in glob.glob(f"{path}/**/*.png", recursive=True)]
    return file_manifest


def have_any_recent_upload_image_files(chatbot:ChatBotWithCookies, pop:bool=False):
    _5min = 5 * 60
    if chatbot is None:
        return False, None  # chatbot is None
    if pop:
        most_recent_uploaded = chatbot._cookies.pop("most_recent_uploaded", None)
    else:
        most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    # most_recent_uploaded 是一个放置最新上传图像的路径
    if not most_recent_uploaded:
        return False, None  # most_recent_uploaded is None
    if time.time() - most_recent_uploaded["time"] < _5min:
        path = most_recent_uploaded["path"]
        file_manifest = get_pictures_list(path)
        if len(file_manifest) == 0:
            return False, None
        return True, file_manifest  # most_recent_uploaded is new
    else:
        return False, None  # most_recent_uploaded is too old

# Claude3 model supports graphic context dialogue, reads all images
def every_image_file_in_path(chatbot:ChatBotWithCookies):
    if chatbot is None:
        return False, []  # chatbot is None
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    if not most_recent_uploaded:
        return False, []  # most_recent_uploaded is None
    path = most_recent_uploaded["path"]
    file_manifest = get_pictures_list(path)
    if len(file_manifest) == 0:
        return False, []
    return True, file_manifest

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_max_token(llm_kwargs):
    from request_llms.bridge_all import model_info

    return model_info[llm_kwargs["llm_model"]]["max_token"]


def check_packages(packages=[]):
    import importlib.util

    for p in packages:
        spam_spec = importlib.util.find_spec(p)
        if spam_spec is None:
            raise ModuleNotFoundError


def map_file_to_sha256(file_path):
    import hashlib

    with open(file_path, 'rb') as file:
        content = file.read()

    # Calculate the SHA-256 hash of the file contents
    sha_hash = hashlib.sha256(content).hexdigest()

    return sha_hash


def check_repeat_upload(new_pdf_path, pdf_hash):
    '''
    检查历史上传的文件是否与新上传的文件相同，如果相同则返回(True, 重复文件路径)，否则返回(False，None)
    '''
    from toolbox import get_conf
    import PyPDF2

    user_upload_dir = os.path.dirname(os.path.dirname(new_pdf_path))
    file_name = os.path.basename(new_pdf_path)

    file_manifest = [f for f in glob.glob(f'{user_upload_dir}/**/{file_name}', recursive=True)]

    for saved_file in file_manifest:
        with open(new_pdf_path, 'rb') as file1, open(saved_file, 'rb') as file2:
            reader1 = PyPDF2.PdfFileReader(file1)
            reader2 = PyPDF2.PdfFileReader(file2)

            # 比较页数是否相同
            if reader1.getNumPages() != reader2.getNumPages():
                continue

            # 比较每一页的内容是否相同
            for page_num in range(reader1.getNumPages()):
                page1 = reader1.getPage(page_num).extractText()
                page2 = reader2.getPage(page_num).extractText()
                if page1 != page2:
                    continue

        maybe_project_dir = glob.glob('{}/**/{}'.format(get_log_folder(), pdf_hash + ".tag"), recursive=True)


        if len(maybe_project_dir) > 0:
            return True, os.path.dirname(maybe_project_dir[0])

    # 如果所有页的内容都相同，返回 True
    return False, None

def log_chat(llm_model: str, input_str: str, output_str: str):
    try:
        if output_str and input_str and llm_model:
            uid = str(uuid.uuid4().hex)
            input_str = input_str.rstrip('\n')
            output_str = output_str.rstrip('\n')
            logger.bind(chat_msg=True).info(dedent(
            """
            ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
            [UID]
            {uid}
            [Model]
            {llm_model}
            [Query]
            {input_str}
            [Response]
            {output_str}
            ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
            """).format(uid=uid, llm_model=llm_model, input_str=input_str, output_str=output_str))
    except:
        logger.error(trimmed_format_exc())



# ----------------------------------------------------------------------
# MODULE: shared_utils.fastapi_server
# SOURCE: shared_utils/fastapi_server.py
# ----------------------------------------------------------------------



def validate_path_safety(path_or_url, user):
    from toolbox import get_conf, default_user_name
    from toolbox import FriendlyException
    PATH_PRIVATE_UPLOAD, PATH_LOGGING = get_conf('PATH_PRIVATE_UPLOAD', 'PATH_LOGGING')
    sensitive_path = None
    path_or_url = os.path.relpath(path_or_url)
    if path_or_url.startswith(PATH_LOGGING):    # 日志文件（按用户划分）
        sensitive_path = PATH_LOGGING
    elif path_or_url.startswith(PATH_PRIVATE_UPLOAD):   # 用户的上传目录（按用户划分）
        sensitive_path = PATH_PRIVATE_UPLOAD
    elif path_or_url.startswith('tests') or path_or_url.startswith('build'):   # 一个常用的测试目录
        return True
    else:
        raise FriendlyException(f"输入文件的路径 ({path_or_url}) 存在，但位置非法。请将文件上传后再执行该任务。") # return False
    if sensitive_path:
        allowed_users = [user, 'autogen', 'arxiv_cache', default_user_name]  # three user path that can be accessed
        for user_allowed in allowed_users:
            if f"{os.sep}".join(path_or_url.split(os.sep)[:2]) == os.path.join(sensitive_path, user_allowed):
                return True
        raise FriendlyException(f"输入文件的路径 ({path_or_url}) 存在，但属于其他用户。请将文件上传后再执行该任务。") # return False
    return True

def _authorize_user(path_or_url, request, gradio_app):
    from toolbox import get_conf, default_user_name
    PATH_PRIVATE_UPLOAD, PATH_LOGGING = get_conf('PATH_PRIVATE_UPLOAD', 'PATH_LOGGING')
    sensitive_path = None
    path_or_url = os.path.relpath(path_or_url)
    if path_or_url.startswith(PATH_LOGGING):
        sensitive_path = PATH_LOGGING
    if path_or_url.startswith(PATH_PRIVATE_UPLOAD):
        sensitive_path = PATH_PRIVATE_UPLOAD
    if sensitive_path:
        token = request.cookies.get("access-token") or request.cookies.get("access-token-unsecure")
        user = gradio_app.tokens.get(token)  # get user
        allowed_users = [user, 'autogen', 'arxiv_cache', default_user_name]  # three user path that can be accessed
        for user_allowed in allowed_users:
            # exact match
            if f"{os.sep}".join(path_or_url.split(os.sep)[:2]) == os.path.join(sensitive_path, user_allowed):
                return True
        return False # "越权访问!"
    return True


class Server(uvicorn.Server):
    # A server that runs in a separate thread
    def install_signal_handlers(self):
        pass

    def run_in_thread(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        while not self.started:
            time.sleep(5e-2)

    def close(self):
        self.should_exit = True
        self.thread.join()


def start_app(app_block, CONCURRENT_COUNT, AUTHENTICATION, PORT, SSL_KEYFILE, SSL_CERTFILE):
    import uvicorn
    import fastapi
    import gradio as gr
    from fastapi import FastAPI
    from gradio.routes import App
    from toolbox import get_conf
    CUSTOM_PATH, PATH_LOGGING = get_conf('CUSTOM_PATH', 'PATH_LOGGING')

    # --- --- configurate gradio app block --- ---
    app_block:gr.Blocks
    app_block.ssl_verify = False
    app_block.auth_message = '请登录'
    app_block.favicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs/logo.png")
    app_block.auth = AUTHENTICATION if len(AUTHENTICATION) != 0 else None
    app_block.blocked_paths = ["config.py", "__pycache__", "config_private.py", "docker-compose.yml", "Dockerfile", f"{PATH_LOGGING}/admin"]
    app_block.dev_mode = False
    app_block.config = app_block.get_config_file()
    app_block.enable_queue = True
    app_block.queue(concurrency_count=CONCURRENT_COUNT)
    app_block.validate_queue_settings()
    app_block.show_api = False
    app_block.config = app_block.get_config_file()
    max_threads = 40
    app_block.max_threads = max(
        app_block._queue.max_thread_count if app_block.enable_queue else 0, max_threads
    )
    app_block.is_colab = False
    app_block.is_kaggle = False
    app_block.is_sagemaker = False

    gradio_app = App.create_app(app_block)
    for route in list(gradio_app.router.routes):
        if route.path == "/proxy={url_path:path}":
            gradio_app.router.routes.remove(route)
    # --- --- replace gradio endpoint to forbid access to sensitive files --- ---
    if len(AUTHENTICATION) > 0:
        dependencies = []
        endpoint = None
        for route in list(gradio_app.router.routes):
            if route.path == "/file/{path:path}":
                gradio_app.router.routes.remove(route)
            if route.path == "/file={path_or_url:path}":
                dependencies = route.dependencies
                endpoint = route.endpoint
                gradio_app.router.routes.remove(route)
        @gradio_app.get("/file/{path:path}", dependencies=dependencies)
        @gradio_app.head("/file={path_or_url:path}", dependencies=dependencies)
        @gradio_app.get("/file={path_or_url:path}", dependencies=dependencies)
        async def file(path_or_url: str, request: fastapi.Request):
            if not _authorize_user(path_or_url, request, gradio_app):
                return "越权访问!"
            stripped = path_or_url.lstrip().lower()
            if stripped.startswith("https://") or stripped.startswith("http://"):
                return "账户密码授权模式下, 禁止链接!"
            if '../' in stripped:
                return "非法路径!"
            return await endpoint(path_or_url, request)

        from fastapi import Request, status
        from fastapi.responses import FileResponse, RedirectResponse
        @gradio_app.get("/academic_logout")
        async def logout():
            response = RedirectResponse(url=CUSTOM_PATH, status_code=status.HTTP_302_FOUND)
            response.delete_cookie('access-token')
            response.delete_cookie('access-token-unsecure')
            return response
    else:
        dependencies = []
        endpoint = None
        for route in list(gradio_app.router.routes):
            if route.path == "/file/{path:path}":
                gradio_app.router.routes.remove(route)
            if route.path == "/file={path_or_url:path}":
                dependencies = route.dependencies
                endpoint = route.endpoint
                gradio_app.router.routes.remove(route)
        @gradio_app.get("/file/{path:path}", dependencies=dependencies)
        @gradio_app.head("/file={path_or_url:path}", dependencies=dependencies)
        @gradio_app.get("/file={path_or_url:path}", dependencies=dependencies)
        async def file(path_or_url: str, request: fastapi.Request):
            stripped = path_or_url.lstrip().lower()
            if stripped.startswith("https://") or stripped.startswith("http://"):
                return "账户密码授权模式下, 禁止链接!"
            if '../' in stripped:
                return "非法路径!"
            return await endpoint(path_or_url, request)

    # --- --- enable TTS (text-to-speech) functionality --- ---
    TTS_TYPE = get_conf("TTS_TYPE")
    if TTS_TYPE != "DISABLE":
        # audio generation functionality
        import httpx
        from fastapi import FastAPI, Request, HTTPException
        from starlette.responses import Response
        async def forward_request(request: Request, method: str) -> Response:
            async with httpx.AsyncClient() as client:
                try:
                    # Forward the request to the target service
                    if TTS_TYPE == "EDGE_TTS":
                        import tempfile
                        import edge_tts
                        import wave
                        import uuid
                        from pydub import AudioSegment
                        json = await request.json()
                        voice = get_conf("EDGE_TTS_VOICE")
                        tts = edge_tts.Communicate(text=json['text'], voice=voice)
                        temp_folder = tempfile.gettempdir()
                        temp_file_name = str(uuid.uuid4().hex)
                        temp_file = os.path.join(temp_folder, f'{temp_file_name}.mp3')
                        await tts.save(temp_file)
                        try:
                            mp3_audio = AudioSegment.from_file(temp_file, format="mp3")
                            mp3_audio.export(temp_file, format="wav")
                            with open(temp_file, 'rb') as wav_file: t = wav_file.read()
                            os.remove(temp_file)
                            return Response(content=t)
                        except:
                            raise RuntimeError("ffmpeg未安装，无法处理EdgeTTS音频。安装方法见`https://github.com/jiaaro/pydub#getting-ffmpeg-set-up`")
                    if TTS_TYPE == "LOCAL_SOVITS_API":
                        # Forward the request to the target service
                        TARGET_URL = get_conf("GPT_SOVITS_URL")
                        body = await request.body()
                        resp = await client.post(TARGET_URL, content=body, timeout=60)
                        # Return the response from the target service
                        return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
                except httpx.RequestError as e:
                    raise HTTPException(status_code=400, detail=f"Request to the target service failed: {str(e)}")
        @gradio_app.post("/vits")
        async def forward_post_request(request: Request):
            return await forward_request(request, "POST")

    # --- --- app_lifespan --- ---
    from contextlib import asynccontextmanager
    @asynccontextmanager
    async def app_lifespan(app):
        async def startup_gradio_app():
            if gradio_app.get_blocks().enable_queue:
                gradio_app.get_blocks().startup_events()
        async def shutdown_gradio_app():
            pass
        await startup_gradio_app() # startup logic here
        yield  # The application will serve requests after this point
        await shutdown_gradio_app() # cleanup/shutdown logic here

    # --- --- FastAPI --- ---
    fastapi_app = FastAPI(lifespan=app_lifespan)
    fastapi_app.mount(CUSTOM_PATH, gradio_app)

    # --- --- favicon and block fastapi api reference routes --- ---
    from starlette.responses import JSONResponse
    if CUSTOM_PATH != '/':
        from fastapi.responses import FileResponse
        @fastapi_app.get("/favicon.ico")
        async def favicon():
            return FileResponse(app_block.favicon_path)

        @fastapi_app.middleware("http")
        async def middleware(request: Request, call_next):
            if request.scope['path'] in ["/docs", "/redoc", "/openapi.json"]:
                return JSONResponse(status_code=404, content={"message": "Not Found"})
            response = await call_next(request)
            return response


    # --- --- uvicorn.Config --- ---
    ssl_keyfile = None if SSL_KEYFILE == "" else SSL_KEYFILE
    ssl_certfile = None if SSL_CERTFILE == "" else SSL_CERTFILE
    server_name = "0.0.0.0"
    config = uvicorn.Config(
        fastapi_app,
        host=server_name,
        port=PORT,
        reload=False,
        log_level="warning",
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
    )
    server = Server(config)
    url_host_name = "localhost" if server_name == "0.0.0.0" else server_name
    if ssl_keyfile is not None:
        if ssl_certfile is None:
            raise ValueError(
                "ssl_certfile must be provided if ssl_keyfile is provided."
            )
        path_to_local_server = f"https://{url_host_name}:{PORT}/"
    else:
        path_to_local_server = f"http://{url_host_name}:{PORT}/"
    if CUSTOM_PATH != '/':
        path_to_local_server += CUSTOM_PATH.lstrip('/').rstrip('/') + '/'
    # --- --- begin  --- ---
    server.run_in_thread()

    # --- --- after server launch --- ---
    app_block.server = server
    app_block.server_name = server_name
    app_block.local_url = path_to_local_server
    app_block.protocol = (
        "https"
        if app_block.local_url.startswith("https") or app_block.is_colab
        else "http"
    )

    if app_block.enable_queue:
        app_block._queue.set_url(path_to_local_server)

    forbid_proxies = {
        "http": "",
        "https": "",
    }
    requests.get(f"{app_block.local_url}startup-events", verify=app_block.ssl_verify, proxies=forbid_proxies)
    app_block.is_running = True
    app_block.block_thread()


# ----------------------------------------------------------------------
# MODULE: crazy_functions.doc_fns.content_folder
# SOURCE: crazy_functions/doc_fns/content_folder.py
# ----------------------------------------------------------------------



# 设置日志
logger = logging.getLogger(__name__)


# 自定义异常类定义
class FoldingError(Exception):
    """折叠相关的自定义异常基类"""
    pass


class FormattingError(FoldingError):
    """格式化过程中的错误"""
    pass


class MetadataError(FoldingError):
    """元数据相关的错误"""
    pass


class ValidationError(FoldingError):
    """验证错误"""
    pass


class FoldingStyle(Enum):
    """折叠样式枚举"""
    SIMPLE = auto()  # 简单折叠
    DETAILED = auto()  # 详细折叠（带有额外信息）
    NESTED = auto()  # 嵌套折叠


@dataclass
class FoldingOptions:
    """折叠选项配置"""
    style: FoldingStyle = FoldingStyle.DETAILED
    code_language: Optional[str] = None  # 代码块的语言
    show_timestamp: bool = False  # 是否显示时间戳
    indent_level: int = 0  # 缩进级别
    custom_css: Optional[str] = None  # 自定义CSS类


T = TypeVar('T')  # 用于泛型类型


class BaseMetadata(ABC):
    """元数据基类"""

    @abstractmethod
    def validate(self) -> bool:
        """验证元数据的有效性"""
        pass

    def _validate_non_empty_str(self, value: Optional[str]) -> bool:
        """验证字符串非空"""
        return bool(value and value.strip())


@dataclass
class FileMetadata(BaseMetadata):
    """文件元数据"""
    rel_path: str
    size: float
    last_modified: Optional[datetime] = None
    mime_type: Optional[str] = None
    encoding: str = 'utf-8'

    def validate(self) -> bool:
        """验证文件元数据的有效性"""
        try:
            if not self._validate_non_empty_str(self.rel_path):
                return False
            if self.size < 0:
                return False
            return True
        except Exception as e:
            logger.error(f"File metadata validation error: {str(e)}")
            return False


class ContentFormatter(ABC, Generic[T]):
    """内容格式化抽象基类

    支持泛型类型参数，可以指定具体的元数据类型。
    """

    @abstractmethod
    def format(self,
               content: str,
               metadata: T,
               options: Optional[FoldingOptions] = None) -> str:
        """格式化内容

        Args:
            content: 需要格式化的内容
            metadata: 类型化的元数据
            options: 折叠选项

        Returns:
            str: 格式化后的内容

        Raises:
            FormattingError: 格式化过程中的错误
        """
        pass

    def _create_summary(self, metadata: T) -> str:
        """创建折叠摘要，可被子类重写"""
        return str(metadata)

    def _format_content_block(self,
                              content: str,
                              options: Optional[FoldingOptions]) -> str:
        """格式化内容块，处理代码块等特殊格式"""
        if not options:
            return content

        if options.code_language:
            return f"```{options.code_language}\n{content}\n```"
        return content

    def _add_indent(self, text: str, level: int) -> str:
        """添加缩进"""
        if level <= 0:
            return text
        indent = "  " * level
        return "\n".join(indent + line for line in text.splitlines())


class FileContentFormatter(ContentFormatter[FileMetadata]):
    """文件内容格式化器"""

    def format(self,
               content: str,
               metadata: FileMetadata,
               options: Optional[FoldingOptions] = None) -> str:
        """格式化文件内容"""
        if not metadata.validate():
            raise MetadataError("Invalid file metadata")

        try:
            options = options or FoldingOptions()

            # 构建摘要信息
            summary_parts = [
                f"{metadata.rel_path} ({metadata.size:.2f}MB)",
                f"Type: {metadata.mime_type}" if metadata.mime_type else None,
                (f"Modified: {metadata.last_modified.strftime('%Y-%m-%d %H:%M:%S')}"
                 if metadata.last_modified and options.show_timestamp else None)
            ]
            summary = " | ".join(filter(None, summary_parts))

            # 构建HTML类
            css_class = f' class="{options.custom_css}"' if options.custom_css else ''

            # 格式化内容
            formatted_content = self._format_content_block(content, options)

            # 组装最终结果
            result = (
                f'<details{css_class}><summary>{summary}</summary>\n\n'
                f'{formatted_content}\n\n'
                f'</details>\n\n'
            )

            return self._add_indent(result, options.indent_level)

        except Exception as e:
            logger.error(f"Error formatting file content: {str(e)}")
            raise FormattingError(f"Failed to format file content: {str(e)}")


class ContentFoldingManager:
    """内容折叠管理器"""

    def __init__(self):
        """初始化折叠管理器"""
        self._formatters: Dict[str, ContentFormatter] = {}
        self._register_default_formatters()

    def _register_default_formatters(self) -> None:
        """注册默认的格式化器"""
        self.register_formatter('file', FileContentFormatter())

    def register_formatter(self, name: str, formatter: ContentFormatter) -> None:
        """注册新的格式化器"""
        if not isinstance(formatter, ContentFormatter):
            raise TypeError("Formatter must implement ContentFormatter interface")
        self._formatters[name] = formatter

    def _guess_language(self, extension: str) -> Optional[str]:
        """根据文件扩展名猜测编程语言"""
        extension = extension.lower().lstrip('.')
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'java': 'java',
            'cpp': 'cpp',
            'cs': 'csharp',
            'html': 'html',
            'css': 'css',
            'md': 'markdown',
            'json': 'json',
            'xml': 'xml',
            'sql': 'sql',
            'sh': 'bash',
            'yaml': 'yaml',
            'yml': 'yaml',
            'txt': None  # 纯文本不需要语言标识
        }
        return language_map.get(extension)

    def format_content(self,
                       content: str,
                       formatter_type: str,
                       metadata: Union[FileMetadata],
                       options: Optional[FoldingOptions] = None) -> str:
        """格式化内容"""
        formatter = self._formatters.get(formatter_type)
        if not formatter:
            raise KeyError(f"No formatter registered for type: {formatter_type}")

        if not isinstance(metadata, FileMetadata):
            raise TypeError("Invalid metadata type")

        return formatter.format(content, metadata, options)




# ----------------------------------------------------------------------
# MODULE: crazy_functions.doc_fns.text_content_loader
# SOURCE: crazy_functions/doc_fns/text_content_loader.py
# ----------------------------------------------------------------------


@dataclass
class FileInfo:
    """文件信息数据类"""
    path: str  # 完整路径
    rel_path: str  # 相对路径
    size: float  # 文件大小(MB)
    extension: str  # 文件扩展名
    last_modified: str  # 最后修改时间


class TextContentLoader:
    """优化版本的文本内容加载器 - 保持原有接口"""

    # 压缩文件扩展名
    COMPRESSED_EXTENSIONS: Set[str] = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'}

    # 系统配置
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 最大文件大小（100MB）
    MAX_TOTAL_SIZE: int = 100 * 1024 * 1024  # 最大总大小（100MB）
    MAX_FILES: int = 100  # 最大文件数量
    CHUNK_SIZE: int = 1024 * 1024  # 文件读取块大小（1MB）
    MAX_WORKERS: int = min(32, (os.cpu_count() or 1) * 4)  # 最大工作线程数
    BATCH_SIZE: int = 5  # 批处理大小

    def __init__(self, chatbot: List, history: List):
        """初始化加载器"""
        self.chatbot = chatbot
        self.history = history
        self.failed_files: List[Tuple[str, str]] = []
        self.processed_size: int = 0
        self.start_time: float = 0
        self.file_cache: Dict[str, str] = {}
        self._lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)
        self.results_queue = queue.Queue()
        self.folding_manager = ContentFoldingManager()

    def _create_file_info(self, entry: os.DirEntry, root_path: str) -> FileInfo:
        """优化的文件信息创建

        Args:
            entry: 目录入口对象
            root_path: 根路径

        Returns:
            FileInfo: 文件信息对象
        """
        try:
            stats = entry.stat()  # 使用缓存的文件状态
            return FileInfo(
                path=entry.path,
                rel_path=os.path.relpath(entry.path, root_path),
                size=stats.st_size / (1024 * 1024),
                extension=os.path.splitext(entry.path)[1].lower(),
                last_modified=time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.localtime(stats.st_mtime))
            )
        except (OSError, ValueError) as e:
            return None

    def _process_file_batch(self, file_batch: List[FileInfo]) -> List[Tuple[FileInfo, Optional[str]]]:
        """批量处理文件

        Args:
            file_batch: 要处理的文件信息列表

        Returns:
            List[Tuple[FileInfo, Optional[str]]]: 处理结果列表
        """
        results = []
        futures = {}

        for file_info in file_batch:
            if file_info.path in self.file_cache:
                results.append((file_info, self.file_cache[file_info.path]))
                continue

            if file_info.size * 1024 * 1024 > self.MAX_FILE_SIZE:
                with self._lock:
                    self.failed_files.append(
                        (file_info.rel_path,
                         f"文件过大（{file_info.size:.2f}MB > {self.MAX_FILE_SIZE / (1024 * 1024)}MB）")
                    )
                continue

            future = self.executor.submit(self._read_file_content, file_info)
            futures[future] = file_info

        for future in as_completed(futures):
            file_info = futures[future]
            try:
                content = future.result()
                if content:
                    with self._lock:
                        self.file_cache[file_info.path] = content
                        self.processed_size += file_info.size * 1024 * 1024
                    results.append((file_info, content))
            except Exception as e:
                with self._lock:
                    self.failed_files.append((file_info.rel_path, f"读取失败: {str(e)}"))

        return results

    def _read_file_content(self, file_info: FileInfo) -> Optional[str]:
        """读取单个文件内容

        Args:
            file_info: 文件信息对象

        Returns:
            Optional[str]: 文件内容
        """
        try:
            content = extract_text(file_info.path)
            if not content or not content.strip():
                return None
            return content
        except Exception as e:
            logger.exception(f"读取文件失败: {str(e)}")
            raise Exception(f"读取文件失败: {str(e)}")

    def _is_valid_file(self, file_path: str) -> bool:
        """检查文件是否有效

        Args:
            file_path: 文件路径

        Returns:
            bool: 是否为有效文件
        """
        if not os.path.isfile(file_path):
            return False

        extension = os.path.splitext(file_path)[1].lower()
        if (extension in self.COMPRESSED_EXTENSIONS or
            os.path.basename(file_path).startswith('.') or
            not os.access(file_path, os.R_OK)):
            return False

        # 只要文件可以访问且不在排除列表中就认为是有效的
        return True

    def _collect_files(self, path: str) -> List[FileInfo]:
        """收集文件信息

        Args:
            path: 目标路径

        Returns:
            List[FileInfo]: 有效文件信息列表
        """
        files = []
        total_size = 0

        # 处理单个文件的情况
        if os.path.isfile(path):
            if self._is_valid_file(path):
                file_info = self._create_file_info(os.DirEntry(os.path.dirname(path)), os.path.dirname(path))
                if file_info:
                    return [file_info]
            return []

        # 处理目录的情况
        try:
            # 使用os.walk来递归遍历目录
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    if len(files) >= self.MAX_FILES:
                        self.failed_files.append((filename, f"超出最大文件数限制({self.MAX_FILES})"))
                        continue

                    file_path = os.path.join(root, filename)

                    if not self._is_valid_file(file_path):
                        continue

                    try:
                        stats = os.stat(file_path)
                        file_size = stats.st_size / (1024 * 1024)  # 转换为MB

                        if file_size * 1024 * 1024 > self.MAX_FILE_SIZE:
                            self.failed_files.append((file_path,
                                f"文件过大（{file_size:.2f}MB > {self.MAX_FILE_SIZE / (1024 * 1024)}MB）"))
                            continue

                        if total_size + file_size * 1024 * 1024 > self.MAX_TOTAL_SIZE:
                            self.failed_files.append((file_path, "超出总大小限制"))
                            continue

                        file_info = FileInfo(
                            path=file_path,
                            rel_path=os.path.relpath(file_path, path),
                            size=file_size,
                            extension=os.path.splitext(file_path)[1].lower(),
                            last_modified=time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(stats.st_mtime))
                        )

                        total_size += file_size * 1024 * 1024
                        files.append(file_info)

                    except Exception as e:
                        self.failed_files.append((file_path, f"处理文件失败: {str(e)}"))
                        continue

        except Exception as e:
            self.failed_files.append(("目录扫描", f"扫描失败: {str(e)}"))
            return []

        return sorted(files, key=lambda x: x.rel_path)

    def _format_content_with_fold(self, file_info, content: str) -> str:
        """使用折叠管理器格式化文件内容"""
        try:
            metadata = FileMetadata(
                rel_path=file_info.rel_path,
                size=file_info.size,
                last_modified=datetime.fromtimestamp(
                    os.path.getmtime(file_info.path)
                ),
                mime_type=mimetypes.guess_type(file_info.path)[0]
            )

            options = FoldingOptions(
                style=FoldingStyle.DETAILED,
                code_language=self.folding_manager._guess_language(
                    os.path.splitext(file_info.path)[1]
                ),
                show_timestamp=True
            )

            return self.folding_manager.format_content(
                content=content,
                formatter_type='file',
                metadata=metadata,
                options=options
            )

        except Exception as e:
            return f"Error formatting content: {str(e)}"

    def _format_content_for_llm(self, file_infos: List[FileInfo], contents: List[str]) -> str:
        """格式化用于LLM的内容

        Args:
            file_infos: 文件信息列表
            contents: 内容列表

        Returns:
            str: 格式化后的内容
        """
        if len(file_infos) != len(contents):
            raise ValueError("文件信息和内容数量不匹配")

        result = [
            "以下是多个文件的内容集合。每个文件的内容都以 '===== 文件 {序号}: {文件名} =====' 开始，",
            "以 '===== 文件 {序号} 结束 =====' 结束。你可以根据这些分隔符来识别不同文件的内容。\n\n"
        ]

        for idx, (file_info, content) in enumerate(zip(file_infos, contents), 1):
            result.extend([
                f"===== 文件 {idx}: {file_info.rel_path} =====",
                "文件内容:",
                content.strip(),
                f"===== 文件 {idx} 结束 =====\n"
            ])

        return "\n".join(result)

    def execute(self, txt: str) -> Generator:
        """执行文本加载和显示 - 保持原有接口

        Args:
            txt: 目标路径

        Yields:
            Generator: UI更新生成器
        """
        try:
            # 首先显示正在处理的提示信息
            self.chatbot.append(["提示", "正在提取文本内容，请稍作等待..."])
            yield from update_ui(chatbot=self.chatbot, history=self.history)

            user_name = self.chatbot.get_user()
            validate_path_safety(txt, user_name)
            self.start_time = time.time()
            self.processed_size = 0
            self.failed_files.clear()
            successful_files = []
            successful_contents = []

            # 收集文件
            files = self._collect_files(txt)
            if not files:
                # 移除之前的提示信息
                self.chatbot.pop()
                self.chatbot.append(["提示", "未找到任何有效文件"])
                yield from update_ui(chatbot=self.chatbot, history=self.history)
                return

            # 批量处理文件
            content_blocks = []
            for i in range(0, len(files), self.BATCH_SIZE):
                batch = files[i:i + self.BATCH_SIZE]
                results = self._process_file_batch(batch)

                for file_info, content in results:
                    if content:
                        content_blocks.append(self._format_content_with_fold(file_info, content))
                        successful_files.append(file_info)
                        successful_contents.append(content)

            # 显示文件内容，替换之前的提示信息
            if content_blocks:
                # 移除之前的提示信息
                self.chatbot.pop()
                self.chatbot.append(["文件内容", "\n".join(content_blocks)])
                self.history.extend([
                    self._format_content_for_llm(successful_files, successful_contents),
                    "我已经接收到你上传的文件的内容，请提问"
                ])
                yield from update_ui(chatbot=self.chatbot, history=self.history)

            yield from update_ui(chatbot=self.chatbot, history=self.history)

        except Exception as e:
            # 发生错误时，移除之前的提示信息
            if len(self.chatbot) > 0 and self.chatbot[-1][0] == "提示":
                self.chatbot.pop()
            self.chatbot.append(["错误", f"处理过程中出现错误: {str(e)}"])
            yield from update_ui(chatbot=self.chatbot, history=self.history)

        finally:
            self.executor.shutdown(wait=False)
            self.file_cache.clear()

    def execute_single_file(self, file_path: str) -> Generator:
        """执行单个文件的加载和显示

        Args:
            file_path: 文件路径

        Yields:
            Generator: UI更新生成器
        """
        try:
            # 首先显示正在处理的提示信息
            self.chatbot.append(["提示", "正在提取文本内容，请稍作等待..."])
            yield from update_ui(chatbot=self.chatbot, history=self.history)

            user_name = self.chatbot.get_user()
            validate_path_safety(file_path, user_name)
            self.start_time = time.time()
            self.processed_size = 0
            self.failed_files.clear()

            # 验证文件是否存在且可读
            if not os.path.isfile(file_path):
                self.chatbot.pop()
                self.chatbot.append(["错误", f"指定路径不是文件: {file_path}"])
                yield from update_ui(chatbot=self.chatbot, history=self.history)
                return

            if not self._is_valid_file(file_path):
                self.chatbot.pop()
                self.chatbot.append(["错误", f"无效的文件类型或无法读取: {file_path}"])
                yield from update_ui(chatbot=self.chatbot, history=self.history)
                return

            # 创建文件信息
            try:
                stats = os.stat(file_path)
                file_size = stats.st_size / (1024 * 1024)  # 转换为MB

                if file_size * 1024 * 1024 > self.MAX_FILE_SIZE:
                    self.chatbot.pop()
                    self.chatbot.append(["错误", f"文件过大（{file_size:.2f}MB > {self.MAX_FILE_SIZE / (1024 * 1024)}MB）"])
                    yield from update_ui(chatbot=self.chatbot, history=self.history)
                    return

                file_info = FileInfo(
                    path=file_path,
                    rel_path=os.path.basename(file_path),
                    size=file_size,
                    extension=os.path.splitext(file_path)[1].lower(),
                    last_modified=time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(stats.st_mtime))
                )
            except Exception as e:
                self.chatbot.pop()
                self.chatbot.append(["错误", f"处理文件失败: {str(e)}"])
                yield from update_ui(chatbot=self.chatbot, history=self.history)
                return

            # 读取文件内容
            try:
                content = self._read_file_content(file_info)
                if not content:
                    self.chatbot.pop()
                    self.chatbot.append(["提示", f"文件内容为空或无法提取: {file_path}"])
                    yield from update_ui(chatbot=self.chatbot, history=self.history)
                    return
            except Exception as e:
                self.chatbot.pop()
                self.chatbot.append(["错误", f"读取文件失败: {str(e)}"])
                yield from update_ui(chatbot=self.chatbot, history=self.history)
                return

            # 格式化内容并更新UI
            formatted_content = self._format_content_with_fold(file_info, content)

            # 移除之前的提示信息
            self.chatbot.pop()
            self.chatbot.append(["文件内容", formatted_content])

            # 更新历史记录，便于LLM处理
            llm_content = self._format_content_for_llm([file_info], [content])
            self.history.extend([llm_content, "我已经接收到你上传的文件的内容，请提问"])

            yield from update_ui(chatbot=self.chatbot, history=self.history)

        except Exception as e:
            # 发生错误时，移除之前的提示信息
            if len(self.chatbot) > 0 and self.chatbot[-1][0] == "提示":
                self.chatbot.pop()
            self.chatbot.append(["错误", f"处理过程中出现错误: {str(e)}"])
            yield from update_ui(chatbot=self.chatbot, history=self.history)

    def __del__(self):
        """析构函数 - 确保资源被正确释放"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        if hasattr(self, 'file_cache'):
            self.file_cache.clear()


# ----------------------------------------------------------------------
# MODULE: crazy_functions.doc_fns.read_fns.web_reader
# SOURCE: crazy_functions/doc_fns/read_fns/web_reader.py
# ----------------------------------------------------------------------




@dataclass
class WebExtractorConfig:
    """网页内容提取器配置类

    Attributes:
        extract_comments: 是否提取评论
        extract_tables: 是否提取表格
        extract_links: 是否保留链接信息
        paragraph_separator: 段落分隔符
        timeout: 网络请求超时时间(秒)
        max_retries: 最大重试次数
        user_agent: 自定义User-Agent
        text_cleanup: 文本清理选项
    """
    extract_comments: bool = False
    extract_tables: bool = True
    extract_links: bool = False
    paragraph_separator: str = '\n\n'
    timeout: int = 10
    max_retries: int = 3
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    text_cleanup: Dict[str, bool] = field(default_factory=lambda: {
        'remove_extra_spaces': True,
        'normalize_whitespace': True,
        'remove_special_chars': False,
        'lowercase': False
    })


class WebTextExtractor:
    """网页文本内容提取器
    
    使用trafilatura库提取网页中的主要文本内容，去除广告、导航等无关内容。
    """

    def __init__(self, config: Optional[WebExtractorConfig] = None):
        """初始化提取器

        Args:
            config: 提取器配置对象，如果为None则使用默认配置
        """
        self.config = config or WebExtractorConfig()
        self._setup_logging()

    def _setup_logging(self) -> None:
        """配置日志记录器"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # 添加文件处理器
        fh = logging.FileHandler('web_extractor.log')
        fh.setLevel(logging.ERROR)
        self.logger.addHandler(fh)

    def _validate_url(self, url: str) -> bool:
        """验证URL格式是否有效

        Args:
            url: 网页URL

        Returns:
            bool: URL是否有效
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _download_webpage(self, url: str) -> Optional[str]:
        """下载网页内容

        Args:
            url: 网页URL

        Returns:
            Optional[str]: 网页HTML内容，失败返回None

        Raises:
            Exception: 下载失败时抛出异常
        """
        headers = {'User-Agent': self.config.user_agent}
        
        for attempt in range(self.config.max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=headers,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"Failed to download webpage after {self.config.max_retries} attempts: {e}")
        return None

    def _cleanup_text(self, text: str) -> str:
        """清理文本

        Args:
            text: 原始文本

        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""

        if self.config.text_cleanup['remove_extra_spaces']:
            text = ' '.join(text.split())

        if self.config.text_cleanup['normalize_whitespace']:
            text = text.replace('\t', ' ').replace('\r', '\n')

        if self.config.text_cleanup['lowercase']:
            text = text.lower()

        return text.strip()

    def extract_text(self, url: str) -> str:
        """提取网页文本内容

        Args:
            url: 网页URL

        Returns:
            str: 提取的文本内容

        Raises:
            ValueError: URL无效时抛出
            Exception: 提取失败时抛出
        """
        try:
            if not self._validate_url(url):
                raise ValueError(f"Invalid URL: {url}")

            self.logger.info(f"Processing URL: {url}")
            
            # 下载网页
            html_content = self._download_webpage(url)
            if not html_content:
                raise Exception("Failed to download webpage")

            # 配置trafilatura提取选项
            extract_config = {
                'include_comments': self.config.extract_comments,
                'include_tables': self.config.extract_tables,
                'include_links': self.config.extract_links,
                'no_fallback': False,  # 允许使用后备提取器
            }

            # 提取文本
            extracted_text = trafilatura.extract(
                html_content,
                **extract_config
            )

            if not extracted_text:
                raise Exception("No content could be extracted")

            # 清理文本
            cleaned_text = self._cleanup_text(extracted_text)
            
            return cleaned_text

        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            raise


def main():
    """主函数：演示用法"""
    # 配置
    config = WebExtractorConfig(
        extract_comments=False,
        extract_tables=True,
        extract_links=False,
        timeout=10,
        text_cleanup={
            'remove_extra_spaces': True,
            'normalize_whitespace': True,
            'remove_special_chars': False,
            'lowercase': False
        }
    )

    # 创建提取器
    extractor = WebTextExtractor(config)

    # 使用示例
    try:
        # 替换为实际的URL
        sample_url = 'https://arxiv.org/abs/2412.00036'
        text = extractor.extract_text(sample_url)
        print("提取的文本:")
        print(text)

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()



# ----------------------------------------------------------------------
# MODULE: shared_utils.doc_loader_dynamic
# SOURCE: shared_utils/doc_loader_dynamic.py
# ----------------------------------------------------------------------



def start_with_url(inputs:str):
    if not ("http://" in inputs or "https://" in inputs):
        return False
    try:
        text = text.strip(',.!?，。！？ \t\n\r')
        words = text.split()
        if len(words) != 1:
            return False
        from urllib.parse import urlparse
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except:
        return False

def load_web_content(inputs:str, chatbot_with_cookie, history:list):
    from crazy_functions.doc_fns.read_fns.web_reader import WebTextExtractor, WebExtractorConfig
    from toolbox import update_ui

    extractor = WebTextExtractor(WebExtractorConfig())
    try:
        # 添加正在处理的提示信息
        chatbot_with_cookie.append([None, "正在提取网页内容，请稍作等待..."])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)
        web_content = extractor.extract_text(inputs)
        # 移除提示信息
        chatbot_with_cookie.pop()
        # 显示提取的内容
        chatbot_with_cookie.append([None, f"网页{inputs}的文本内容如下：" + web_content])
        history.extend([f"网页{inputs}的文本内容如下：" + web_content])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)
    except Exception as e:
        # 如果出错，移除提示信息（如果存在）
        if len(chatbot_with_cookie) > 0 and chatbot_with_cookie[-1][-1] == "正在提取网页内容，请稍作等待...":
            chatbot_with_cookie.pop()
        chatbot_with_cookie.append([inputs, f"网页内容提取失败: {str(e)}"])
        yield from update_ui(chatbot=chatbot_with_cookie, history=history)

def extract_file_path(text):
    # 匹配以 private_upload 开头，包含时间戳格式的路径
    pattern = r'(private_upload/[^\s]+?/\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})'
    match = re.search(pattern, text)
    if match and os.path.exists(match.group(1)):
        return match.group(1)
    return None

def contain_uploaded_files(inputs: str):
    file_path_match = extract_file_path(inputs)
    if file_path_match:
        return True
    return False


def load_uploaded_files(inputs, method, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, stream, additional_fn):
    # load file
    from crazy_functions.doc_fns.text_content_loader import TextContentLoader
    file_path = extract_file_path(inputs)
    loader = TextContentLoader(chatbot_with_cookie, history)
    yield from loader.execute(file_path)

    # get question
    original_question = inputs.replace(file_path, '').strip()
    if not original_question:
        original_question = f"请简单分析上述文件内容"
    else:
        original_question = f"基于上述文件内容，{original_question}"

    return original_question



# ----------------------------------------------------------------------
# MODULE: request_llms.bridge_openrouter
# SOURCE: request_llms/bridge_openrouter.py
# ----------------------------------------------------------------------



# config_private.py放自己的秘密如API和代理网址
# 读取时首先看是否存在私密的config_private配置文件（不受git管控），如果有，则覆盖原config文件
proxies, TIMEOUT_SECONDS, MAX_RETRY, API_ORG, AZURE_CFG_ARRAY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'API_ORG', 'AZURE_CFG_ARRAY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  '网络错误，检查代理服务器是否可用，以及代理设置的格式是否正确，格式须是[协议]://[地址]:[端口]，缺一不可。'

def get_full_error(chunk, stream_response):
    """
        获取完整的从Openai返回的报错
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk

def make_multimodal_input(inputs, image_paths):
    image_base64_array = []
    for image_path in image_paths:
        path = os.path.abspath(image_path)
        base64 = encode_image(path)
        inputs = inputs + f'<br/><br/><div align="center"><img src="file={path}" base64="{base64}"></div>'
        image_base64_array.append(base64)
    return inputs, image_base64_array

def reverse_base64_from_input(inputs):
    # 定义一个正则表达式来匹配 Base64 字符串（假设格式为 base64="<Base64编码>"）
    # pattern = re.compile(r'base64="([^"]+)"></div>')
    pattern = re.compile(r'<br/><br/><div align="center"><img[^<>]+base64="([^"]+)"></div>')
    # 使用 findall 方法查找所有匹配的 Base64 字符串
    base64_strings = pattern.findall(inputs)
    # 返回反转后的 Base64 字符串列表
    return base64_strings

def contain_base64(inputs):
    base64_strings = reverse_base64_from_input(inputs)
    return len(base64_strings) > 0

def append_image_if_contain_base64(inputs):
    if not contain_base64(inputs):
        return inputs
    else:
        image_base64_array = reverse_base64_from_input(inputs)
        pattern = re.compile(r'<br/><br/><div align="center"><img[^><]+></div>')
        inputs = re.sub(pattern, '', inputs)
        res = []
        res.append({
            "type": "text",
            "text": inputs
        })
        for image_base64 in image_base64_array:
            res.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })
        return res

def remove_image_if_contain_base64(inputs):
    if not contain_base64(inputs):
        return inputs
    else:
        pattern = re.compile(r'<br/><br/><div align="center"><img[^><]+></div>')
        inputs = re.sub(pattern, '', inputs)
        return inputs

def decode_chunk(chunk):
    # 提前读取一些信息 （用于判断异常）
    chunk_decoded = chunk.decode()
    chunkjson = None
    has_choices = False
    choice_valid = False
    has_content = False
    has_role = False
    try:
        chunkjson = json.loads(chunk_decoded[6:])
        has_choices = 'choices' in chunkjson
        if has_choices: choice_valid = (len(chunkjson['choices']) > 0)
        if has_choices and choice_valid: has_content = ("content" in chunkjson['choices'][0]["delta"])
        if has_content: has_content = (chunkjson['choices'][0]["delta"]["content"] is not None)
        if has_choices and choice_valid: has_role = "role" in chunkjson['choices'][0]["delta"]
    except:
        pass
    return chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role

@lru_cache(maxsize=32)
def verify_endpoint(endpoint):
    """
        检查endpoint是否可用
    """
    if "你亲手写的api名称" in endpoint:
        raise ValueError("Endpoint不正确, 请检查AZURE_ENDPOINT的配置! 当前的Endpoint为:" + endpoint)
    return endpoint

def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list=[], sys_prompt:str="", observe_window:list=None, console_silence:bool=False):
    """
    发送至chatGPT，等待回复，一次性完成，不显示中间过程。但内部用stream的方法避免中途网线被掐。
    inputs：
        是本次问询的输入
    sys_prompt:
        系统静默prompt
    llm_kwargs：
        chatGPT的内部调优参数
    history：
        是之前的对话列表
    observe_window = None：
        用于负责跨越线程传递已经输出的部分，大部分时候仅仅为了fancy的视觉效果，留空即可。observe_window[0]：观测窗。observe_window[1]：看门狗
    """
    from request_llms.bridge_all import model_info

    watch_dog_patience = 5 # 看门狗的耐心, 设置5秒即可

    if model_info[llm_kwargs['llm_model']].get('openai_disable_stream', False): stream = False
    else: stream = True

    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=stream)
    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=stream, timeout=TIMEOUT_SECONDS); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: logger.error(f'请求超时，正在重试 ({retry}/{MAX_RETRY}) ……')

    if not stream:
        # 该分支仅适用于不支持stream的o1模型，其他情形一律不适用
        chunkjson = json.loads(response.content.decode())
        gpt_replying_buffer = chunkjson['choices'][0]["message"]["content"]
        return gpt_replying_buffer

    stream_response = response.iter_lines()
    result = ''
    json_data = None
    while True:
        try: chunk = next(stream_response)
        except StopIteration:
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response) # 失败了，重试一次？再失败就没办法了。
        chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)
        if len(chunk_decoded)==0 or chunk_decoded.startswith(':'): continue
        if not chunk_decoded.startswith('data:'):
            error_msg = get_full_error(chunk, stream_response).decode()
            if "reduce the length" in error_msg:
                raise ConnectionAbortedError("OpenAI拒绝了请求:" + error_msg)
            elif """type":"upstream_error","param":"307""" in error_msg:
                raise ConnectionAbortedError("正常结束，但显示Token不足，导致输出不完整，请削减单次输入的文本量。")
            else:
                raise RuntimeError("OpenAI拒绝了请求：" + error_msg)
        if ('data: [DONE]' in chunk_decoded): break # api2d 正常完成
        # 提前读取一些信息 （用于判断异常）
        json_data = chunkjson['choices'][0]
        delta = json_data["delta"]
        if len(delta) == 0: break
        if (not has_content) and has_role: continue
        if (not has_content) and (not has_role): continue # raise RuntimeError("发现不标准的第三方接口："+delta)
        if has_content: # has_role = True/False
            result += delta["content"]
            if not console_silence: print(delta["content"], end='')
            if observe_window is not None:
                # 观测窗，把已经获取的数据显示出去
                if len(observe_window) >= 1:
                    observe_window[0] += delta["content"]
                # 看门狗，如果超过期限没有喂狗，则终止
                if len(observe_window) >= 2:
                    if (time.time()-observe_window[1]) > watch_dog_patience:
                        raise RuntimeError("用户取消了程序。")
        else: raise RuntimeError("意外Json结构："+delta)
    if json_data and json_data['finish_reason'] == 'content_filter':
        raise RuntimeError("由于提问含不合规内容被Azure过滤。")
    if json_data and json_data['finish_reason'] == 'length':
        raise ConnectionAbortedError("正常结束，但显示Token不足，导致输出不完整，请削减单次输入的文本量。")
    return result


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
    发送至chatGPT，流式获取输出。
    用于基础的对话功能。
    inputs 是本次问询的输入
    top_p, temperature是chatGPT的内部调优参数
    history 是之前的对话列表（注意无论是inputs还是history，内容太长了都会触发token数量溢出的错误）
    chatbot 为WebUI中显示的对话列表，修改它，然后yield出去，可以直接修改对话界面内容
    additional_fn代表点击的哪个按钮，按钮见functional.py
    """
    from request_llms.bridge_all import model_info
    if is_any_api_key(inputs):
        chatbot._cookies['api_key'] = inputs
        chatbot.append(("输入已识别为openai的api_key", what_keys(inputs)))
        yield from update_ui(chatbot=chatbot, history=history, msg="api_key已导入") # 刷新界面
        return
    elif not is_any_api_key(chatbot._cookies['api_key']):
        chatbot.append((inputs, "缺少api_key。\n\n1. 临时解决方案：直接在输入区键入api_key，然后回车提交。\n\n2. 长效解决方案：在config.py中配置。"))
        yield from update_ui(chatbot=chatbot, history=history, msg="缺少api_key") # 刷新界面
        return

    user_input = inputs
    if additional_fn is not None:
        from core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    # 多模态模型
    has_multimodal_capacity = model_info[llm_kwargs['llm_model']].get('has_multimodal_capacity', False)
    if has_multimodal_capacity:
        has_recent_image_upload, image_paths = have_any_recent_upload_image_files(chatbot, pop=True)
    else:
        has_recent_image_upload, image_paths = False, []
    if has_recent_image_upload:
        _inputs, image_base64_array = make_multimodal_input(inputs, image_paths)
    else:
        _inputs, image_base64_array = inputs, []
    chatbot.append((_inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="等待响应") # 刷新界面

    # 禁用stream的特殊模型处理
    if model_info[llm_kwargs['llm_model']].get('openai_disable_stream', False): stream = False
    else: stream = True

    # check mis-behavior
    if is_the_upload_folder(user_input):
        chatbot[-1] = (inputs, f"[Local Message] 检测到操作错误！当您上传文档之后，需点击“**函数插件区**”按钮进行处理，请勿点击“提交”按钮或者“基础功能区”按钮。")
        yield from update_ui(chatbot=chatbot, history=history, msg="正常") # 刷新界面
        time.sleep(2)

    try:
        headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt, image_base64_array, has_multimodal_capacity, stream)
    except RuntimeError as e:
        chatbot[-1] = (inputs, f"您提供的api-key不满足要求，不包含任何可用于{llm_kwargs['llm_model']}的api-key。您可能选择了错误的模型或请求源。")
        yield from update_ui(chatbot=chatbot, history=history, msg="api-key不满足要求") # 刷新界面
        return

    # 检查endpoint是否合法
    try:
        endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
    except:
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (inputs, tb_str)
        yield from update_ui(chatbot=chatbot, history=history, msg="Endpoint不满足要求") # 刷新界面
        return

    # 加入历史
    if has_recent_image_upload:
        history.extend([_inputs, ""])
    else:
        history.extend([inputs, ""])

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=stream, timeout=TIMEOUT_SECONDS);break
        except:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], timeout_bot_msg))
            retry_msg = f"，正在重试 ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
            yield from update_ui(chatbot=chatbot, history=history, msg="请求超时"+retry_msg) # 刷新界面
            if retry > MAX_RETRY: raise TimeoutError


    if not stream:
        # 该分支仅适用于不支持stream的o1模型，其他情形一律不适用
        yield from handle_o1_model_special(response, inputs, llm_kwargs, chatbot, history)
        return

    if stream:
        gpt_replying_buffer = ""
        is_head_of_the_stream = True
        stream_response =  response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                # 非OpenAI官方接口的出现这样的报错，OpenAI和API2D不会走这里
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                # 首先排除一个one-api没有done数据包的第三方Bug情形
                if len(gpt_replying_buffer.strip()) > 0 and len(error_msg) == 0:
                    yield from update_ui(chatbot=chatbot, history=history, msg="检测到有缺陷的非OpenAI官方接口，建议选择更稳定的接口。")
                    break
                # 其他情况，直接返回报错
                chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                yield from update_ui(chatbot=chatbot, history=history, msg="非OpenAI官方接口返回了错误:" + chunk.decode()) # 刷新界面
                return

            # 提前读取一些信息 （用于判断异常）
            chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)

            if is_head_of_the_stream and (r'"object":"error"' not in chunk_decoded) and (r"content" not in chunk_decoded):
                # 数据流的第一帧不携带content
                is_head_of_the_stream = False; continue

            if chunk:
                try:
                    if (has_choices and not choice_valid) or chunk_decoded.startswith(':'):
                        continue
                    if ('data: [DONE]' not in chunk_decoded) and len(chunk_decoded) > 0 and (chunkjson is None):
                        # 传递进来一些奇怪的东西
                        raise ValueError(f'无法读取以下数据，请检查配置。\n\n{chunk_decoded}')
                    # 前者是API2D的结束条件，后者是OPENAI的结束条件
                    if ('data: [DONE]' in chunk_decoded) or (len(chunkjson['choices'][0]["delta"]) == 0):
                        # 判定为数据流的结束，gpt_replying_buffer也写完了
                        log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
                        break
                    # 处理数据流的主体
                    status_text = f"finish_reason: {chunkjson['choices'][0].get('finish_reason', 'null')}"
                    # 如果这里抛出异常，一般是文本过长，详情见get_full_error的输出
                    if has_content:
                        # 正常情况
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]
                    elif has_role:
                        # 一些第三方接口的出现这样的错误，兼容一下吧
                        continue
                    else:
                        # 至此已经超出了正常接口应该进入的范围，一些垃圾第三方接口会出现这样的错误
                        if chunkjson['choices'][0]["delta"]["content"] is None: continue # 一些垃圾第三方接口出现这样的错误，兼容一下吧
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]

                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text) # 刷新界面
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json解析不合常规") # 刷新界面
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json解析异常" + error_msg) # 刷新界面
                    logger.error(error_msg)
                    return
        return  # return from stream-branch

def handle_o1_model_special(response, inputs, llm_kwargs, chatbot, history):
    try:
        chunkjson = json.loads(response.content.decode())
        gpt_replying_buffer = chunkjson['choices'][0]["message"]["content"]
        log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
        history[-1] = gpt_replying_buffer
        chatbot[-1] = (history[-2], history[-1])
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
    except Exception as e:
        yield from update_ui(chatbot=chatbot, history=history, msg="Json解析异常" + response.text) # 刷新界面

def handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg):
    from request_llms.bridge_all import model_info
    openai_website = ' 请登录OpenAI查看详情 https://platform.openai.com/signup'
    if "reduce the length" in error_msg:
        if len(history) >= 2: history[-1] = ""; history[-2] = "" # 清除当前溢出的输入：history[-2] 是本次输入, history[-1] 是本次输出
        history = clip_history(inputs=inputs, history=history, tokenizer=model_info[llm_kwargs['llm_model']]['tokenizer'],
                                               max_token_limit=(model_info[llm_kwargs['llm_model']]['max_token'])) # history至少释放二分之一
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Reduce the length. 本次输入过长, 或历史数据过长. 历史缓存数据已部分释放, 您可以请再次尝试. (若再次失败则更可能是因为输入过长.)")
    elif "does not exist" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Model {llm_kwargs['llm_model']} does not exist. 模型不存在, 或者您没有获得体验资格.")
    elif "Incorrect API key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. OpenAI以提供了不正确的API_KEY为由, 拒绝服务. " + openai_website)
    elif "exceeded your current quota" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You exceeded your current quota. OpenAI以账户额度不足为由, 拒绝服务." + openai_website)
    elif "account is not active" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Your account is not active. OpenAI以账户失效为由, 拒绝服务." + openai_website)
    elif "associated with a deactivated account" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You are associated with a deactivated account. OpenAI以账户失效为由, 拒绝服务." + openai_website)
    elif "API key has been deactivated" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] API key has been deactivated. OpenAI以账户失效为由, 拒绝服务." + openai_website)
    elif "bad forward key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Bad forward key. API2D账户额度不足.")
    elif "Not enough point" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Not enough point. API2D账户点数不足.")
    else:
        from toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] 异常 \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history

def generate_payload(inputs:str, llm_kwargs:dict, history:list, system_prompt:str, image_base64_array:list=[], has_multimodal_capacity:bool=False, stream:bool=True):
    """
    整合所有信息，选择LLM模型，生成http请求，为发送请求做准备
    """
    from request_llms.bridge_all import model_info

    if not is_any_api_key(llm_kwargs['api_key']):
        raise AssertionError("你提供了错误的API_KEY。\n\n1. 临时解决方案：直接在输入区键入api_key，然后回车提交。\n\n2. 长效解决方案：在config.py中配置。")

    if llm_kwargs['llm_model'].startswith('vllm-'):
        api_key = 'no-api-key'
    else:
        api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if API_ORG.startswith('org-'): headers.update({"OpenAI-Organization": API_ORG})
    if llm_kwargs['llm_model'].startswith('azure-'):
        headers.update({"api-key": api_key})
        if llm_kwargs['llm_model'] in AZURE_CFG_ARRAY.keys():
            azure_api_key_unshared = AZURE_CFG_ARRAY[llm_kwargs['llm_model']]["AZURE_API_KEY"]
            headers.update({"api-key": azure_api_key_unshared})

    if has_multimodal_capacity:
        # 当以下条件满足时，启用多模态能力：
        # 1. 模型本身是多模态模型（has_multimodal_capacity）
        # 2. 输入包含图像（len(image_base64_array) > 0）
        # 3. 历史输入包含图像（ any([contain_base64(h) for h in history]) ）
        enable_multimodal_capacity = (len(image_base64_array) > 0) or any([contain_base64(h) for h in history])
    else:
        enable_multimodal_capacity = False

    conversation_cnt = len(history) // 2
    openai_disable_system_prompt = model_info[llm_kwargs['llm_model']].get('openai_disable_system_prompt', False)

    if openai_disable_system_prompt:
        messages = [{"role": "user", "content": system_prompt}]
    else:
        messages = [{"role": "system", "content": system_prompt}]

    if not enable_multimodal_capacity:
        # 不使用多模态能力
        if conversation_cnt:
            for index in range(0, 2*conversation_cnt, 2):
                what_i_have_asked = {}
                what_i_have_asked["role"] = "user"
                what_i_have_asked["content"] = remove_image_if_contain_base64(history[index])
                what_gpt_answer = {}
                what_gpt_answer["role"] = "assistant"
                what_gpt_answer["content"] = remove_image_if_contain_base64(history[index+1])
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    if what_gpt_answer["content"] == timeout_bot_msg: continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = inputs
        messages.append(what_i_ask_now)
    else:
        # 多模态能力
        if conversation_cnt:
            for index in range(0, 2*conversation_cnt, 2):
                what_i_have_asked = {}
                what_i_have_asked["role"] = "user"
                what_i_have_asked["content"] = append_image_if_contain_base64(history[index])
                what_gpt_answer = {}
                what_gpt_answer["role"] = "assistant"
                what_gpt_answer["content"] = append_image_if_contain_base64(history[index+1])
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    if what_gpt_answer["content"] == timeout_bot_msg: continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = []
        what_i_ask_now["content"].append({
            "type": "text",
            "text": inputs
        })
        for image_base64 in image_base64_array:
            what_i_ask_now["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            })
        messages.append(what_i_ask_now)


    model = llm_kwargs['llm_model']
    if llm_kwargs['llm_model'].startswith('api2d-'):
        model = llm_kwargs['llm_model'][len('api2d-'):]
    if llm_kwargs['llm_model'].startswith('one-api-'):
        model = llm_kwargs['llm_model'][len('one-api-'):]
        model, _ = read_one_api_model_name(model)
    if llm_kwargs['llm_model'].startswith('vllm-'):
        model = llm_kwargs['llm_model'][len('vllm-'):]
        model, _ = read_one_api_model_name(model)
    if llm_kwargs['llm_model'].startswith('openrouter-'):
        model = llm_kwargs['llm_model'][len('openrouter-'):]
        model, _= read_one_api_model_name(model)
    if model == "gpt-3.5-random": # 随机选择, 绕过openai访问频率限制
        model = random.choice([
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-3.5-turbo-0301",
        ])

    payload = {
        "model": model,
        "messages": messages,
        "temperature": llm_kwargs['temperature'],  # 1.0,
        "top_p": llm_kwargs['top_p'],  # 1.0,
        "n": 1,
        "stream": stream,
    }

    return headers,payload





# ----------------------------------------------------------------------
# MODULE: shared_utils.char_visual_effect
# SOURCE: shared_utils/char_visual_effect.py
# ----------------------------------------------------------------------

def is_full_width_char(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True  # 中文字符
    if '\uff01' <= ch <= '\uff5e':
        return True  # 全角符号
    if '\u3000' <= ch <= '\u303f':
        return True  # CJK标点符号
    return False

def scrolling_visual_effect(text, scroller_max_len):
    text = text.\
            replace('\n', '').replace('`', '.').replace(' ', '.').replace('<br/>', '.....').replace('$', '.')
    place_take_cnt = 0
    pointer = len(text) - 1

    if len(text) < scroller_max_len:
        return text

    while place_take_cnt < scroller_max_len and pointer > 0:
        if is_full_width_char(text[pointer]): place_take_cnt += 2
        else: place_take_cnt += 1
        pointer -= 1

    return text[pointer:]


# ----------------------------------------------------------------------
# MODULE: crazy_functions.crazy_utils
# SOURCE: crazy_functions/crazy_utils.py
# ----------------------------------------------------------------------


def input_clipping(inputs, history, max_token_limit, return_clip_flags=False):
    """
    当输入文本 + 历史文本超出最大限制时，采取措施丢弃一部分文本。
    输入：
        - inputs 本次请求
        - history 历史上下文
        - max_token_limit 最大token限制
    输出:
        - inputs 本次请求（经过clip）
        - history 历史上下文（经过clip）
    """
    import numpy as np
    from request_llms.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))


    mode = 'input-and-history'
    # 当 输入部分的token占比 小于 全文的一半时，只裁剪历史
    input_token_num = get_token_num(inputs)
    original_input_len = len(inputs)
    if input_token_num < max_token_limit//2:
        mode = 'only-history'
        max_token_limit = max_token_limit - input_token_num

    everything = [inputs] if mode == 'input-and-history' else ['']
    everything.extend(history)
    full_token_num = n_token = get_token_num('\n'.join(everything))
    everything_token = [get_token_num(e) for e in everything]
    everything_token_num = sum(everything_token)
    delta = max(everything_token) // 16 # 截断时的颗粒度

    while n_token > max_token_limit:
        where = np.argmax(everything_token)
        encoded = enc.encode(everything[where], disallowed_special=())
        clipped_encoded = encoded[:len(encoded)-delta]
        everything[where] = enc.decode(clipped_encoded)[:-1]    # -1 to remove the may-be illegal char
        everything_token[where] = get_token_num(everything[where])
        n_token = get_token_num('\n'.join(everything))

    if mode == 'input-and-history':
        inputs = everything[0]
        full_token_num = everything_token_num
    else:
        full_token_num = everything_token_num + input_token_num

    history = everything[1:]

    flags = {
        "mode": mode,
        "original_input_token_num": input_token_num,
        "original_full_token_num": full_token_num,
        "original_input_len": original_input_len,
        "clipped_input_len": len(inputs),
    }

    if not return_clip_flags:
        return inputs, history
    else:
        return inputs, history, flags

def request_gpt_model_in_new_thread_with_ui_alive(
        inputs, inputs_show_user, llm_kwargs,
        chatbot, history, sys_prompt, refresh_interval=0.2,
        handle_token_exceed=True,
        retry_times_at_unknown_error=2,
        ):
    """
    Request GPT model，请求GPT模型同时维持用户界面活跃。

    输入参数 Args （以_array结尾的输入变量都是列表，列表长度为子任务的数量，执行时，会把列表拆解，放到每个子线程中分别执行）:
        inputs (string): List of inputs （输入）
        inputs_show_user (string): List of inputs to show user（展现在报告中的输入，借助此参数，在汇总报告中隐藏啰嗦的真实输入，增强报告的可读性）
        top_p (float): Top p value for sampling from model distribution （GPT参数，浮点数）
        temperature (float): Temperature value for sampling from model distribution（GPT参数，浮点数）
        chatbot: chatbot inputs and outputs （用户界面对话窗口句柄，用于数据流可视化）
        history (list): List of chat history （历史，对话历史列表）
        sys_prompt (string): List of system prompts （系统输入，列表，用于输入给GPT的前提提示，比如你是翻译官怎样怎样）
        refresh_interval (float, optional): Refresh interval for UI (default: 0.2) （刷新时间间隔频率，建议低于1，不可高于3，仅仅服务于视觉效果）
        handle_token_exceed：是否自动处理token溢出的情况，如果选择自动处理，则会在溢出时暴力截断，默认开启
        retry_times_at_unknown_error：失败时的重试次数

    输出 Returns:
        future: 输出，GPT返回的结果
    """
    import time
    from concurrent.futures import ThreadPoolExecutor
    from request_llms.bridge_all import predict_no_ui_long_connection
    # 用户反馈
    chatbot.append([inputs_show_user, ""])
    yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
    executor = ThreadPoolExecutor(max_workers=16)
    mutable = ["", time.time(), ""]
    # 看门狗耐心
    watch_dog_patience = 5
    # 请求任务
    def _req_gpt(inputs, history, sys_prompt):
        retry_op = retry_times_at_unknown_error
        exceeded_cnt = 0
        while True:
            # watchdog error
            if len(mutable) >= 2 and (time.time()-mutable[1]) > watch_dog_patience:
                raise RuntimeError("检测到程序终止。")
            try:
                # 【第一种情况】：顺利完成
                result = predict_no_ui_long_connection(
                    inputs=inputs, llm_kwargs=llm_kwargs,
                    history=history, sys_prompt=sys_prompt, observe_window=mutable)
                return result
            except ConnectionAbortedError as token_exceeded_error:
                # 【第二种情况】：Token溢出
                if handle_token_exceed:
                    exceeded_cnt += 1
                    # 【选择处理】 尝试计算比例，尽可能多地保留文本
                    from toolbox import get_reduce_token_percent
                    p_ratio, n_exceed = get_reduce_token_percent(str(token_exceeded_error))
                    MAX_TOKEN = get_max_token(llm_kwargs)
                    EXCEED_ALLO = 512 + 512 * exceeded_cnt
                    inputs, history = input_clipping(inputs, history, max_token_limit=MAX_TOKEN-EXCEED_ALLO)
                    mutable[0] += f'[Local Message] 警告，文本过长将进行截断，Token溢出数：{n_exceed}。\n\n'
                    continue # 返回重试
                else:
                    # 【选择放弃】
                    tb_str = '```\n' + trimmed_format_exc() + '```'
                    mutable[0] += f"[Local Message] 警告，在执行过程中遭遇问题, Traceback：\n\n{tb_str}\n\n"
                    return mutable[0] # 放弃
            except:
                # 【第三种情况】：其他错误：重试几次
                tb_str = '```\n' + trimmed_format_exc() + '```'
                logger.error(tb_str)
                mutable[0] += f"[Local Message] 警告，在执行过程中遭遇问题, Traceback：\n\n{tb_str}\n\n"
                if retry_op > 0:
                    retry_op -= 1
                    mutable[0] += f"[Local Message] 重试中，请稍等 {retry_times_at_unknown_error-retry_op}/{retry_times_at_unknown_error}：\n\n"
                    if ("Rate limit reached" in tb_str) or ("Too Many Requests" in tb_str):
                        time.sleep(30)
                    time.sleep(5)
                    continue # 返回重试
                else:
                    time.sleep(5)
                    return mutable[0] # 放弃

    # 提交任务
    future = executor.submit(_req_gpt, inputs, history, sys_prompt)
    while True:
        # yield一次以刷新前端页面
        time.sleep(refresh_interval)
        # “喂狗”（看门狗）
        mutable[1] = time.time()
        if future.done():
            break
        chatbot[-1] = [chatbot[-1][0], mutable[0]]
        yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面

    final_result = future.result()
    chatbot[-1] = [chatbot[-1][0], final_result]
    yield from update_ui(chatbot=chatbot, history=[]) # 如果最后成功了，则删除报错信息
    return final_result

def can_multi_process(llm) -> bool:
    from request_llms.bridge_all import model_info

    def default_condition(llm) -> bool:
        # legacy condition
        if llm.startswith('gpt-'): return True
        if llm.startswith('chatgpt-'): return True
        if llm.startswith('api2d-'): return True
        if llm.startswith('azure-'): return True
        if llm.startswith('spark'): return True
        if llm.startswith('zhipuai') or llm.startswith('glm-'): return True
        return False

    if llm in model_info:
        if 'can_multi_thread' in model_info[llm]:
            return model_info[llm]['can_multi_thread']
        else:
            return default_condition(llm)
    else:
        return default_condition(llm)

def request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array, inputs_show_user_array, llm_kwargs,
        chatbot, history_array, sys_prompt_array,
        refresh_interval=0.2, max_workers=-1, scroller_max_len=75,
        handle_token_exceed=True, show_user_at_complete=False,
        retry_times_at_unknown_error=2,
        ):
    """
    Request GPT model using multiple threads with UI and high efficiency
    请求GPT模型的[多线程]版。
    具备以下功能：
        实时在UI上反馈远程数据流
        使用线程池，可调节线程池的大小避免openai的流量限制错误
        处理中途中止的情况
        网络等出问题时，会把traceback和已经接收的数据转入输出

    输入参数 Args （以_array结尾的输入变量都是列表，列表长度为子任务的数量，执行时，会把列表拆解，放到每个子线程中分别执行）:
        inputs_array (list): List of inputs （每个子任务的输入）
        inputs_show_user_array (list): List of inputs to show user（每个子任务展现在报告中的输入，借助此参数，在汇总报告中隐藏啰嗦的真实输入，增强报告的可读性）
        llm_kwargs: llm_kwargs参数
        chatbot: chatbot （用户界面对话窗口句柄，用于数据流可视化）
        history_array (list): List of chat history （历史对话输入，双层列表，第一层列表是子任务分解，第二层列表是对话历史）
        sys_prompt_array (list): List of system prompts （系统输入，列表，用于输入给GPT的前提提示，比如你是翻译官怎样怎样）
        refresh_interval (float, optional): Refresh interval for UI (default: 0.2) （刷新时间间隔频率，建议低于1，不可高于3，仅仅服务于视觉效果）
        max_workers (int, optional): Maximum number of threads (default: see config.py) （最大线程数，如果子任务非常多，需要用此选项防止高频地请求openai导致错误）
        scroller_max_len (int, optional): Maximum length for scroller (default: 30)（数据流的显示最后收到的多少个字符，仅仅服务于视觉效果）
        handle_token_exceed (bool, optional): （是否在输入过长时，自动缩减文本）
        handle_token_exceed：是否自动处理token溢出的情况，如果选择自动处理，则会在溢出时暴力截断，默认开启
        show_user_at_complete (bool, optional): (在结束时，把完整输入-输出结果显示在聊天框)
        retry_times_at_unknown_error：子任务失败时的重试次数

    输出 Returns:
        list: List of GPT model responses （每个子任务的输出汇总，如果某个子任务出错，response中会携带traceback报错信息，方便调试和定位问题。）
    """
    import time, random
    from concurrent.futures import ThreadPoolExecutor
    from request_llms.bridge_all import predict_no_ui_long_connection
    assert len(inputs_array) == len(history_array)
    assert len(inputs_array) == len(sys_prompt_array)
    if max_workers == -1: # 读取配置文件
        try: max_workers = get_conf('DEFAULT_WORKER_NUM')
        except: max_workers = 8
        if max_workers <= 0: max_workers = 3
    # 屏蔽掉 chatglm的多线程，可能会导致严重卡顿
    if not can_multi_process(llm_kwargs['llm_model']):
        max_workers = 1

    executor = ThreadPoolExecutor(max_workers=max_workers)
    n_frag = len(inputs_array)
    # 用户反馈
    chatbot.append(["请开始多线程操作。", ""])
    yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
    # 跨线程传递
    mutable = [["", time.time(), "等待中"] for _ in range(n_frag)]

    # 看门狗耐心
    watch_dog_patience = 5

    # 子线程任务
    def _req_gpt(index, inputs, history, sys_prompt):
        gpt_say = ""
        retry_op = retry_times_at_unknown_error
        exceeded_cnt = 0
        mutable[index][2] = "执行中"
        detect_timeout = lambda: len(mutable[index]) >= 2 and (time.time()-mutable[index][1]) > watch_dog_patience
        while True:
            # watchdog error
            if detect_timeout(): raise RuntimeError("检测到程序终止。")
            try:
                # 【第一种情况】：顺利完成
                gpt_say = predict_no_ui_long_connection(
                    inputs=inputs, llm_kwargs=llm_kwargs, history=history,
                    sys_prompt=sys_prompt, observe_window=mutable[index], console_silence=True
                )
                mutable[index][2] = "已成功"
                return gpt_say
            except ConnectionAbortedError as token_exceeded_error:
                # 【第二种情况】：Token溢出
                if handle_token_exceed:
                    exceeded_cnt += 1
                    # 【选择处理】 尝试计算比例，尽可能多地保留文本
                    from toolbox import get_reduce_token_percent
                    p_ratio, n_exceed = get_reduce_token_percent(str(token_exceeded_error))
                    MAX_TOKEN = get_max_token(llm_kwargs)
                    EXCEED_ALLO = 512 + 512 * exceeded_cnt
                    inputs, history = input_clipping(inputs, history, max_token_limit=MAX_TOKEN-EXCEED_ALLO)
                    gpt_say += f'[Local Message] 警告，文本过长将进行截断，Token溢出数：{n_exceed}。\n\n'
                    mutable[index][2] = f"截断重试"
                    continue # 返回重试
                else:
                    # 【选择放弃】
                    tb_str = '```\n' + trimmed_format_exc() + '```'
                    gpt_say += f"[Local Message] 警告，线程{index}在执行过程中遭遇问题, Traceback：\n\n{tb_str}\n\n"
                    if len(mutable[index][0]) > 0: gpt_say += "此线程失败前收到的回答：\n\n" + mutable[index][0]
                    mutable[index][2] = "输入过长已放弃"
                    return gpt_say # 放弃
            except:
                # 【第三种情况】：其他错误
                if detect_timeout(): raise RuntimeError("检测到程序终止。")
                tb_str = '```\n' + trimmed_format_exc() + '```'
                logger.error(tb_str)
                gpt_say += f"[Local Message] 警告，线程{index}在执行过程中遭遇问题, Traceback：\n\n{tb_str}\n\n"
                if len(mutable[index][0]) > 0: gpt_say += "此线程失败前收到的回答：\n\n" + mutable[index][0]
                if retry_op > 0:
                    retry_op -= 1
                    wait = random.randint(5, 20)
                    if ("Rate limit reached" in tb_str) or ("Too Many Requests" in tb_str):
                        wait = wait * 3
                        fail_info = "OpenAI绑定信用卡可解除频率限制 "
                    else:
                        fail_info = ""
                    # 也许等待十几秒后，情况会好转
                    for i in range(wait):
                        mutable[index][2] = f"{fail_info}等待重试 {wait-i}"; time.sleep(1)
                    # 开始重试
                    if detect_timeout(): raise RuntimeError("检测到程序终止。")
                    mutable[index][2] = f"重试中 {retry_times_at_unknown_error-retry_op}/{retry_times_at_unknown_error}"
                    continue # 返回重试
                else:
                    mutable[index][2] = "已失败"
                    wait = 5
                    time.sleep(5)
                    return gpt_say # 放弃

    # 异步任务开始
    futures = [executor.submit(_req_gpt, index, inputs, history, sys_prompt) for index, inputs, history, sys_prompt in zip(
        range(len(inputs_array)), inputs_array, history_array, sys_prompt_array)]
    cnt = 0


    while True:
        # yield一次以刷新前端页面
        time.sleep(refresh_interval)
        cnt += 1
        worker_done = [h.done() for h in futures]
        # 更好的UI视觉效果
        observe_win = []
        # 每个线程都要“喂狗”（看门狗）
        for thread_index, _ in enumerate(worker_done):
            mutable[thread_index][1] = time.time()
        # 在前端打印些好玩的东西
        for thread_index, _ in enumerate(worker_done):
            print_something_really_funny = f"[ ...`{scrolling_visual_effect(mutable[thread_index][0], scroller_max_len)}`... ]"
            observe_win.append(print_something_really_funny)
        # 在前端打印些好玩的东西
        stat_str = ''.join([f'`{mutable[thread_index][2]}`: {obs}\n\n'
                            if not done else f'`{mutable[thread_index][2]}`\n\n'
                            for thread_index, done, obs in zip(range(len(worker_done)), worker_done, observe_win)])
        # 在前端打印些好玩的东西
        chatbot[-1] = [chatbot[-1][0], f'多线程操作已经开始，完成情况: \n\n{stat_str}' + ''.join(['.']*(cnt % 10+1))]
        yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
        if all(worker_done):
            executor.shutdown()
            break

    # 异步任务结束
    gpt_response_collection = []
    for inputs_show_user, f in zip(inputs_show_user_array, futures):
        gpt_res = f.result()
        gpt_response_collection.extend([inputs_show_user, gpt_res])

    # 是否在结束时，在界面上显示结果
    if show_user_at_complete:
        for inputs_show_user, f in zip(inputs_show_user_array, futures):
            gpt_res = f.result()
            chatbot.append([inputs_show_user, gpt_res])
            yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
            time.sleep(0.5)
    return gpt_response_collection


def read_and_clean_pdf_text(fp):
    """
    这个函数用于分割pdf，用了很多trick，逻辑较乱，效果奇好

    **输入参数说明**
    - `fp`：需要读取和清理文本的pdf文件路径

    **输出参数说明**
    - `meta_txt`：清理后的文本内容字符串
    - `page_one_meta`：第一页清理后的文本内容列表

    **函数功能**
    读取pdf文件并清理其中的文本内容，清理规则包括：
    - 提取所有块元的文本信息，并合并为一个字符串
    - 去除短块（字符数小于100）并替换为回车符
    - 清理多余的空行
    - 合并小写字母开头的段落块并替换为空格
    - 清除重复的换行
    - 将每个换行符替换为两个换行符，使每个段落之间有两个换行符分隔
    """
    import fitz, copy
    import re
    import numpy as np
    # from shared_utils.colorful import print亮黄, print亮绿
    fc = 0  # Index 0 文本
    fs = 1  # Index 1 字体
    fb = 2  # Index 2 框框
    REMOVE_FOOT_NOTE = True # 是否丢弃掉 不是正文的内容 （比正文字体小，如参考文献、脚注、图注等）
    REMOVE_FOOT_FFSIZE_PERCENT = 0.95 # 小于正文的？时，判定为不是正文（有些文章的正文部分字体大小不是100%统一的，有肉眼不可见的小变化）
    def primary_ffsize(l):
        """
        提取文本块主字体
        """
        fsize_statistics = {}
        for wtf in l['spans']:
            if wtf['size'] not in fsize_statistics: fsize_statistics[wtf['size']] = 0
            fsize_statistics[wtf['size']] += len(wtf['text'])
        return max(fsize_statistics, key=fsize_statistics.get)

    def ffsize_same(a,b):
        """
        提取字体大小是否近似相等
        """
        return abs((a-b)/max(a,b)) < 0.02

    with fitz.open(fp) as doc:
        meta_txt = []
        meta_font = []

        meta_line = []
        meta_span = []
        ############################## <第 1 步，搜集初始信息> ##################################
        for index, page in enumerate(doc):
            # file_content += page.get_text()
            text_areas = page.get_text("dict")  # 获取页面上的文本信息
            for t in text_areas['blocks']:
                if 'lines' in t:
                    pf = 998
                    for l in t['lines']:
                        txt_line = "".join([wtf['text'] for wtf in l['spans']])
                        if len(txt_line) == 0: continue
                        pf = primary_ffsize(l)
                        meta_line.append([txt_line, pf, l['bbox'], l])
                        for wtf in l['spans']: # for l in t['lines']:
                            meta_span.append([wtf['text'], wtf['size'], len(wtf['text'])])
                    # meta_line.append(["NEW_BLOCK", pf])
            # 块元提取                           for each word segment with in line                       for each line         cross-line words                          for each block
            meta_txt.extend([" ".join(["".join([wtf['text'] for wtf in l['spans']]) for l in t['lines']]).replace(
                '- ', '') for t in text_areas['blocks'] if 'lines' in t])
            meta_font.extend([np.mean([np.mean([wtf['size'] for wtf in l['spans']])
                             for l in t['lines']]) for t in text_areas['blocks'] if 'lines' in t])
            if index == 0:
                page_one_meta = [" ".join(["".join([wtf['text'] for wtf in l['spans']]) for l in t['lines']]).replace(
                    '- ', '') for t in text_areas['blocks'] if 'lines' in t]

        ############################## <第 2 步，获取正文主字体> ##################################
        try:
            fsize_statistics = {}
            for span in meta_span:
                if span[1] not in fsize_statistics: fsize_statistics[span[1]] = 0
                fsize_statistics[span[1]] += span[2]
            main_fsize = max(fsize_statistics, key=fsize_statistics.get)
            if REMOVE_FOOT_NOTE:
                give_up_fize_threshold = main_fsize * REMOVE_FOOT_FFSIZE_PERCENT
        except:
            raise RuntimeError(f'抱歉, 我们暂时无法解析此PDF文档: {fp}。')
        ############################## <第 3 步，切分和重新整合> ##################################
        mega_sec = []
        sec = []
        for index, line in enumerate(meta_line):
            if index == 0:
                sec.append(line[fc])
                continue
            if REMOVE_FOOT_NOTE:
                if meta_line[index][fs] <= give_up_fize_threshold:
                    continue
            if ffsize_same(meta_line[index][fs], meta_line[index-1][fs]):
                # 尝试识别段落
                if meta_line[index][fc].endswith('.') and\
                    (meta_line[index-1][fc] != 'NEW_BLOCK') and \
                    (meta_line[index][fb][2] - meta_line[index][fb][0]) < (meta_line[index-1][fb][2] - meta_line[index-1][fb][0]) * 0.7:
                    sec[-1] += line[fc]
                    sec[-1] += "\n\n"
                else:
                    sec[-1] += " "
                    sec[-1] += line[fc]
            else:
                if (index+1 < len(meta_line)) and \
                    meta_line[index][fs] > main_fsize:
                    # 单行 + 字体大
                    mega_sec.append(copy.deepcopy(sec))
                    sec = []
                    sec.append("# " + line[fc])
                else:
                    # 尝试识别section
                    if meta_line[index-1][fs] > meta_line[index][fs]:
                        sec.append("\n" + line[fc])
                    else:
                        sec.append(line[fc])
        mega_sec.append(copy.deepcopy(sec))

        finals = []
        for ms in mega_sec:
            final = " ".join(ms)
            final = final.replace('- ', ' ')
            finals.append(final)
        meta_txt = finals

        ############################## <第 4 步，乱七八糟的后处理> ##################################
        def 把字符太少的块清除为回车(meta_txt):
            for index, block_txt in enumerate(meta_txt):
                if len(block_txt) < 100:
                    meta_txt[index] = '\n'
            return meta_txt
        meta_txt = 把字符太少的块清除为回车(meta_txt)

        def 清理多余的空行(meta_txt):
            for index in reversed(range(1, len(meta_txt))):
                if meta_txt[index] == '\n' and meta_txt[index-1] == '\n':
                    meta_txt.pop(index)
            return meta_txt
        meta_txt = 清理多余的空行(meta_txt)

        def 合并小写开头的段落块(meta_txt):
            def starts_with_lowercase_word(s):
                pattern = r"^[a-z]+"
                match = re.match(pattern, s)
                if match:
                    return True
                else:
                    return False
            # 对于某些PDF会有第一个段落就以小写字母开头,为了避免索引错误将其更改为大写
            if starts_with_lowercase_word(meta_txt[0]):
                meta_txt[0] = meta_txt[0].capitalize()
            for _ in range(100):
                for index, block_txt in enumerate(meta_txt):
                    if starts_with_lowercase_word(block_txt):
                        if meta_txt[index-1] != '\n':
                            meta_txt[index-1] += ' '
                        else:
                            meta_txt[index-1] = ''
                        meta_txt[index-1] += meta_txt[index]
                        meta_txt[index] = '\n'
            return meta_txt
        meta_txt = 合并小写开头的段落块(meta_txt)
        meta_txt = 清理多余的空行(meta_txt)

        meta_txt = '\n'.join(meta_txt)
        # 清除重复的换行
        for _ in range(5):
            meta_txt = meta_txt.replace('\n\n', '\n')

        # 换行 -> 双换行
        meta_txt = meta_txt.replace('\n', '\n\n')

        ############################## <第 5 步，展示分割效果> ##################################
        # for f in finals:
        #    print亮黄(f)
        #    print亮绿('***************************')

    return meta_txt, page_one_meta


def get_files_from_everything(txt, type): # type='.md'
    """
    这个函数是用来获取指定目录下所有指定类型（如.md）的文件，并且对于网络上的文件，也可以获取它。
    下面是对每个参数和返回值的说明：
    参数
    - txt: 路径或网址，表示要搜索的文件或者文件夹路径或网络上的文件。
    - type: 字符串，表示要搜索的文件类型。默认是.md。
    返回值
    - success: 布尔值，表示函数是否成功执行。
    - file_manifest: 文件路径列表，里面包含以指定类型为后缀名的所有文件的绝对路径。
    - project_folder: 字符串，表示文件所在的文件夹路径。如果是网络上的文件，就是临时文件夹的路径。
    该函数详细注释已添加，请确认是否满足您的需要。
    """
    import glob, os

    success = True
    if txt.startswith('http'):
        # 网络的远程文件
        import requests
        from toolbox import get_conf
        from toolbox import get_log_folder, gen_time_str
        proxies = get_conf('proxies')
        try:
            r = requests.get(txt, proxies=proxies)
        except:
            raise ConnectionRefusedError(f"无法下载资源{txt}，请检查。")
        path = os.path.join(get_log_folder(plugin_name='web_download'), gen_time_str()+type)
        with open(path, 'wb+') as f: f.write(r.content)
        project_folder = get_log_folder(plugin_name='web_download')
        file_manifest = [path]
    elif txt.endswith(type):
        # 直接给定文件
        file_manifest = [txt]
        project_folder = os.path.dirname(txt)
    elif os.path.exists(txt):
        # 本地路径，递归搜索
        project_folder = txt
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*'+type, recursive=True)]
        if len(file_manifest) == 0:
            success = False
    else:
        project_folder = None
        file_manifest = []
        success = False

    return success, file_manifest, project_folder


@Singleton
class nougat_interface():
    def __init__(self):
        self.threadLock = threading.Lock()

    def nougat_with_timeout(self, command, cwd, timeout=3600):
        import subprocess
        from toolbox import ProxyNetworkActivate
        logger.info(f'正在执行命令 {command}')
        with ProxyNetworkActivate("Nougat_Download"):
            process = subprocess.Popen(command, shell=False, cwd=cwd, env=os.environ)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            logger.error("Process timed out!")
            return False
        return True


    def NOUGAT_parse_pdf(self, fp, chatbot, history):
        from toolbox import update_ui_latest_msg

        yield from update_ui_latest_msg("正在解析论文, 请稍候。进度：正在排队, 等待线程锁...",
                                         chatbot=chatbot, history=history, delay=0)
        self.threadLock.acquire()
        import glob, threading, os
        from toolbox import get_log_folder, gen_time_str
        dst = os.path.join(get_log_folder(plugin_name='nougat'), gen_time_str())
        os.makedirs(dst)

        yield from update_ui_latest_msg("正在解析论文, 请稍候。进度：正在加载NOUGAT... （提示：首次运行需要花费较长时间下载NOUGAT参数）",
                                         chatbot=chatbot, history=history, delay=0)
        command = ['nougat', '--out', os.path.abspath(dst), os.path.abspath(fp)]
        self.nougat_with_timeout(command, cwd=os.getcwd(), timeout=3600)
        res = glob.glob(os.path.join(dst,'*.mmd'))
        if len(res) == 0:
            self.threadLock.release()
            raise RuntimeError("Nougat解析论文失败。")
        self.threadLock.release()
        return res[0]


def try_install_deps(deps, reload_m=[]):
    import subprocess, sys, importlib
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', dep])
    import site
    importlib.reload(site)
    for m in reload_m:
        importlib.reload(__import__(m))


def get_plugin_arg(plugin_kwargs, key, default):
    # 如果参数是空的
    if (key in plugin_kwargs) and (plugin_kwargs[key] == ""): plugin_kwargs.pop(key)
    # 正常情况
    return plugin_kwargs.get(key, default)



# ----------------------------------------------------------------------
# MODULE: request_llms.bridge_moonshot
# SOURCE: request_llms/bridge_moonshot.py
# ----------------------------------------------------------------------

# encoding: utf-8
# @Time   : 2024/3/3
# @Author : Spike
# @Descr   :


class MoonShotInit:

    def __init__(self):
        self.llm_model = None
        self.url = 'https://api.moonshot.cn/v1/chat/completions'
        self.api_key = get_conf('MOONSHOT_API_KEY')

    def __converter_file(self, user_input: str):
        what_ask = []
        for f in user_input.splitlines():
            if os.path.exists(f):
                files = []
                if os.path.isdir(f):
                    file_list = os.listdir(f)
                    files.extend([os.path.join(f, file) for file in file_list])
                else:
                    files.append(f)
                for file in files:
                    if file.split('.')[-1] in ['pdf']:
                        with open(file, 'r', encoding='utf8') as fp:
                            from crazy_functions.crazy_utils import read_and_clean_pdf_text
                            file_content, _ = read_and_clean_pdf_text(fp)
                        what_ask.append({"role": "system", "content": file_content})
        return what_ask

    def __converter_user(self, user_input: str):
        what_i_ask_now = {"role": "user", "content": user_input}
        return what_i_ask_now

    def __conversation_history(self, history):
        conversation_cnt = len(history) // 2
        messages = []
        if conversation_cnt:
            for index in range(0, 2 * conversation_cnt, 2):
                what_i_have_asked = {
                    "role": "user",
                    "content": str(history[index])
                }
                what_gpt_answer = {
                    "role": "assistant",
                    "content": str(history[index + 1])
                }
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']
        return messages

    def _analysis_content(self, chuck):
        chunk_decoded = chuck.decode("utf-8")
        chunk_json = {}
        content = ""
        try:
            chunk_json = json.loads(chunk_decoded[6:])
            content = chunk_json['choices'][0]["delta"].get("content", "")
        except:
            pass
        return chunk_decoded, chunk_json, content

    def generate_payload(self, inputs, llm_kwargs, history, system_prompt, stream):
        self.llm_model = llm_kwargs['llm_model']
        llm_kwargs.update({'use-key': self.api_key})
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(self.__converter_file(inputs))
        for i in history[0::2]:    # 历史文件继续上传
            messages.extend(self.__converter_file(i))
        messages.extend(self.__conversation_history(history))
        messages.append(self.__converter_user(inputs))
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": self.llm_model,
            "messages": messages,
            "temperature": llm_kwargs.get('temperature', 0.3),  # 1.0,
            "top_p": llm_kwargs.get('top_p', 1.0),  # 1.0,
            "n": llm_kwargs.get('n_choices', 1),
            "stream": stream
        }
        return payload, header

    def generate_messages(self, inputs, llm_kwargs, history, system_prompt, stream):
        payload, headers = self.generate_payload(inputs, llm_kwargs, history, system_prompt, stream)
        response = requests.post(self.url, headers=headers, json=payload, stream=stream)

        chunk_content = ""
        gpt_bro_result = ""
        for chuck in response.iter_lines():
            chunk_decoded, check_json, content = self._analysis_content(chuck)
            chunk_content += chunk_decoded
            if content:
                gpt_bro_result += content
                yield content, gpt_bro_result, ''
            else:
                error_msg = msg_handle_error(llm_kwargs, chunk_decoded)
                if error_msg:
                    yield error_msg, gpt_bro_result, error_msg
                    break


def msg_handle_error(llm_kwargs, chunk_decoded):
    use_ket = llm_kwargs.get('use-key', '')
    api_key_encryption = use_ket[:8] + '****' + use_ket[-5:]
    openai_website = f' 请登录OpenAI查看详情 https://platform.openai.com/signup  api-key: `{api_key_encryption}`'
    error_msg = ''
    if "does not exist" in chunk_decoded:
        error_msg = f"[Local Message] Model {llm_kwargs['llm_model']} does not exist. 模型不存在, 或者您没有获得体验资格."
    elif "Incorrect API key" in chunk_decoded:
        error_msg = f"[Local Message] Incorrect API key. OpenAI以提供了不正确的API_KEY为由, 拒绝服务." + openai_website
    elif "exceeded your current quota" in chunk_decoded:
        error_msg = "[Local Message] You exceeded your current quota. OpenAI以账户额度不足为由, 拒绝服务." + openai_website
    elif "account is not active" in chunk_decoded:
        error_msg = "[Local Message] Your account is not active. OpenAI以账户失效为由, 拒绝服务." + openai_website
    elif "associated with a deactivated account" in chunk_decoded:
        error_msg = "[Local Message] You are associated with a deactivated account. OpenAI以账户失效为由, 拒绝服务." + openai_website
    elif "API key has been deactivated" in chunk_decoded:
        error_msg = "[Local Message] API key has been deactivated. OpenAI以账户失效为由, 拒绝服务." + openai_website
    elif "bad forward key" in chunk_decoded:
        error_msg = "[Local Message] Bad forward key. API2D账户额度不足."
    elif "Not enough point" in chunk_decoded:
        error_msg = "[Local Message] Not enough point. API2D账户点数不足."
    elif 'error' in str(chunk_decoded).lower():
        try:
            error_msg = json.dumps(json.loads(chunk_decoded[:6]), indent=4, ensure_ascii=False)
        except:
            error_msg = chunk_decoded
    return error_msg


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    chatbot.append([inputs, ""])

    if additional_fn is not None:
        from core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)
    yield from update_ui(chatbot=chatbot, history=history, msg="等待响应")  # 刷新界面
    gpt_bro_init = MoonShotInit()
    history.extend([inputs, ''])
    stream_response = gpt_bro_init.generate_messages(inputs, llm_kwargs, history, system_prompt, stream)
    for content, gpt_bro_result, error_bro_meg in stream_response:
        chatbot[-1] = [inputs, gpt_bro_result]
        history[-1] = gpt_bro_result
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        if error_bro_meg:
            chatbot[-1] = [inputs, error_bro_meg]
            history = history[:-2]
            yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
            break
    log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_bro_result)

def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None,
                                  console_silence=False):
    gpt_bro_init = MoonShotInit()
    watch_dog_patience = 60  # 看门狗的耐心, 设置10秒即可
    stream_response = gpt_bro_init.generate_messages(inputs, llm_kwargs, history, sys_prompt, True)
    moonshot_bro_result = ''
    for content, moonshot_bro_result, error_bro_meg in stream_response:
        moonshot_bro_result = moonshot_bro_result
        if error_bro_meg:
            if len(observe_window) >= 3:
                observe_window[2] = error_bro_meg
            return f'{moonshot_bro_result} 对话错误'
            # 观测窗
        if len(observe_window) >= 1:
            observe_window[0] = moonshot_bro_result
        if len(observe_window) >= 2:
            if (time.time() - observe_window[1]) > watch_dog_patience:
                observe_window[2] = "请求超时，程序终止。"
                raise RuntimeError(f"{moonshot_bro_result} 程序终止。")
    return moonshot_bro_result

if __name__ == '__main__':
    moon_ai = MoonShotInit()
    for g in moon_ai.generate_messages('hello', {'llm_model': 'moonshot-v1-8k'},
                                       [], '', True):
        print(g)



# ----------------------------------------------------------------------
# MODULE: request_llms.bridge_all
# SOURCE: request_llms/bridge_all.py
# ----------------------------------------------------------------------



# from .bridge_chatgpt import predict_no_ui_long_connection as chatgpt_noui  # Relative import removed
# from .bridge_chatgpt import predict as chatgpt_ui  # Relative import removed

# from .bridge_chatgpt_vision import predict_no_ui_long_connection as chatgpt_vision_noui  # Relative import removed
# from .bridge_chatgpt_vision import predict as chatgpt_vision_ui  # Relative import removed

# from .bridge_chatglm import predict_no_ui_long_connection as chatglm_noui  # Relative import removed
# from .bridge_chatglm import predict as chatglm_ui  # Relative import removed

# from .bridge_chatglm3 import predict_no_ui_long_connection as chatglm3_noui  # Relative import removed
# from .bridge_chatglm3 import predict as chatglm3_ui  # Relative import removed

# from .bridge_chatglm4 import predict_no_ui_long_connection as chatglm4_noui  # Relative import removed
# from .bridge_chatglm4 import predict as chatglm4_ui  # Relative import removed

# from .bridge_qianfan import predict_no_ui_long_connection as qianfan_noui  # Relative import removed
# from .bridge_qianfan import predict as qianfan_ui  # Relative import removed

# from .bridge_google_gemini import predict as genai_ui  # Relative import removed
# from .bridge_google_gemini import predict_no_ui_long_connection  as genai_noui  # Relative import removed

# from .bridge_zhipu import predict_no_ui_long_connection as zhipu_noui  # Relative import removed
# from .bridge_zhipu import predict as zhipu_ui  # Relative import removed

# from .bridge_taichu import predict_no_ui_long_connection as taichu_noui  # Relative import removed
# from .bridge_taichu import predict as taichu_ui  # Relative import removed

# from .bridge_cohere import predict as cohere_ui  # Relative import removed
# from .bridge_cohere import predict_no_ui_long_connection as cohere_noui  # Relative import removed

# from .oai_std_model_template import get_predict_function  # Relative import removed

colors = ['#FF00FF', '#00FFFF', '#FF0000', '#990099', '#009999', '#990044']

class LazyloadTiktoken(object):
    def __init__(self, model):
        self.model = model

    @staticmethod
    @lru_cache(maxsize=128)
    def get_encoder(model):
        logger.info('正在加载tokenizer，如果是第一次运行，可能需要一点时间下载参数')
        tmp = tiktoken.encoding_for_model(model)
        logger.info('加载tokenizer完毕')
        return tmp

    def encode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model)
        return encoder.encode(*args, **kwargs)

    def decode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model)
        return encoder.decode(*args, **kwargs)

# Endpoint 重定向
API_URL_REDIRECT, AZURE_ENDPOINT, AZURE_ENGINE = get_conf("API_URL_REDIRECT", "AZURE_ENDPOINT", "AZURE_ENGINE")
openai_endpoint = "https://api.openai.com/v1/chat/completions"
api2d_endpoint = "https://openai.api2d.net/v1/chat/completions"
newbing_endpoint = "wss://sydney.bing.com/sydney/ChatHub"
gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
claude_endpoint = "https://api.anthropic.com/v1/messages"
cohere_endpoint = "https://api.cohere.ai/v1/chat"
ollama_endpoint = "http://localhost:11434/api/chat"
yimodel_endpoint = "https://api.lingyiwanwu.com/v1/chat/completions"
deepseekapi_endpoint = "https://api.deepseek.com/v1/chat/completions"
grok_model_endpoint = "https://api.x.ai/v1/chat/completions"
volcengine_endpoint = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

if not AZURE_ENDPOINT.endswith('/'): AZURE_ENDPOINT += '/'
azure_endpoint = AZURE_ENDPOINT + f'openai/deployments/{AZURE_ENGINE}/chat/completions?api-version=2023-05-15'
# 兼容旧版的配置
try:
    API_URL = get_conf("API_URL")
    if API_URL != "https://api.openai.com/v1/chat/completions":
        openai_endpoint = API_URL
        logger.warning("警告！API_URL配置选项将被弃用，请更换为API_URL_REDIRECT配置")
except:
    pass
# 新版配置
if openai_endpoint in API_URL_REDIRECT: openai_endpoint = API_URL_REDIRECT[openai_endpoint]
if api2d_endpoint in API_URL_REDIRECT: api2d_endpoint = API_URL_REDIRECT[api2d_endpoint]
if newbing_endpoint in API_URL_REDIRECT: newbing_endpoint = API_URL_REDIRECT[newbing_endpoint]
if gemini_endpoint in API_URL_REDIRECT: gemini_endpoint = API_URL_REDIRECT[gemini_endpoint]
if claude_endpoint in API_URL_REDIRECT: claude_endpoint = API_URL_REDIRECT[claude_endpoint]
if cohere_endpoint in API_URL_REDIRECT: cohere_endpoint = API_URL_REDIRECT[cohere_endpoint]
if ollama_endpoint in API_URL_REDIRECT: ollama_endpoint = API_URL_REDIRECT[ollama_endpoint]
if yimodel_endpoint in API_URL_REDIRECT: yimodel_endpoint = API_URL_REDIRECT[yimodel_endpoint]
if deepseekapi_endpoint in API_URL_REDIRECT: deepseekapi_endpoint = API_URL_REDIRECT[deepseekapi_endpoint]
if grok_model_endpoint in API_URL_REDIRECT: grok_model_endpoint = API_URL_REDIRECT[grok_model_endpoint]
if volcengine_endpoint in API_URL_REDIRECT: volcengine_endpoint = API_URL_REDIRECT[volcengine_endpoint]

# 获取tokenizer
tokenizer_gpt35 = LazyloadTiktoken("gpt-3.5-turbo")
tokenizer_gpt4 = LazyloadTiktoken("gpt-4")
get_token_num_gpt35 = lambda txt: len(tokenizer_gpt35.encode(txt, disallowed_special=()))
get_token_num_gpt4 = lambda txt: len(tokenizer_gpt4.encode(txt, disallowed_special=()))


# 开始初始化模型
AVAIL_LLM_MODELS, LLM_MODEL = get_conf("AVAIL_LLM_MODELS", "LLM_MODEL")
AVAIL_LLM_MODELS = AVAIL_LLM_MODELS + [LLM_MODEL]
# -=-=-=-=-=-=- 以下这部分是最早加入的最稳定的模型 -=-=-=-=-=-=-
model_info = {
    # openai
    "gpt-3.5-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "taichu": {
        "fn_with_ui": taichu_ui,
        "fn_without_ui": taichu_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-16k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-16k-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-1106": { #16k
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-0125": { #16k
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-32k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 32768,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4o": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4o-mini": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "chatgpt-4o-latest": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4o-2024-05-13": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-1106-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-0125-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "o1-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
        "openai_disable_system_prompt": True,
        "openai_disable_stream": True,
        "openai_force_temperature_one": True,
    },

    "o1-mini": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "can_multi_thread": True,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
        "openai_disable_system_prompt": True,
        "openai_disable_stream": True,
        "openai_force_temperature_one": True,
    },

    "o1-2024-12-17": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 200000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
        "openai_disable_system_prompt": True,
        "openai_disable_stream": True,
        "openai_force_temperature_one": True,
    },

    "o1": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 200000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
        "openai_disable_system_prompt": True,
        "openai_disable_stream": True,
        "openai_force_temperature_one": True,
    },

    "gpt-4.1":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 828000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4.1-mini":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 828000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "o3":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 828000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
        "openai_disable_system_prompt": True,
        "openai_disable_stream": True,
        "openai_force_temperature_one": True,
    },

    "o4-mini":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "can_multi_thread": True,
        "endpoint": openai_endpoint,
        "max_token": 828000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo-2024-04-09": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "has_multimodal_capacity": True,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-3.5-random": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-vision-preview": {
        "fn_with_ui": chatgpt_vision_ui,
        "fn_without_ui": chatgpt_vision_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },


    # azure openai
    "azure-gpt-3.5":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "azure-gpt-4":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    # 智谱AI
    "glm-4": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-0520": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-air": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-airx": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-flash": {
         "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4v": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 1000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-3-turbo": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 4,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-plus":{
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # api_2d (此后不需要在此处添加api2d的接口了，因为下面的代码会自动添加)
    "api2d-gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": api2d_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    # ChatGLM本地模型
    # 将 chatglm 直接对齐到 chatglm2
    "chatglm": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm2": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm3": {
        "fn_with_ui": chatglm3_ui,
        "fn_without_ui": chatglm3_noui,
        "endpoint": None,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm4": {
        "fn_with_ui": chatglm4_ui,
        "fn_without_ui": chatglm4_noui,
        "endpoint": None,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "qianfan": {
        "fn_with_ui": qianfan_ui,
        "fn_without_ui": qianfan_noui,
        "endpoint": None,
        "max_token": 2000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    # Gemini
    # Note: now gemini-pro is an alias of gemini-1.0-pro.
    # Warning: gemini-pro-vision has been deprecated.
    # Support for gemini-pro-vision has been removed.
    "gemini-pro": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "has_multimodal_capacity": False,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-1.0-pro": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "has_multimodal_capacity": False,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-1.5-pro": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 1024 * 204800,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-1.5-flash": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 1024 * 204800,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-2.0-flash": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "has_multimodal_capacity": True,
        "max_token": 1024 * 204800,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # cohere
    "cohere-command-r-plus": {
        "fn_with_ui": cohere_ui,
        "fn_without_ui": cohere_noui,
        "can_multi_thread": True,
        "endpoint": cohere_endpoint,
        "max_token": 1024 * 4,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

}
# -=-=-=-=-=-=- 月之暗面 -=-=-=-=-=-=-
model_info.update({
    "moonshot-v1-8k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "moonshot-v1-32k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "moonshot-v1-128k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 128,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    }
})
# -=-=-=-=-=-=- api2d 对齐支持 -=-=-=-=-=-=-
for model in AVAIL_LLM_MODELS:
    if model.startswith('api2d-') and (model.replace('api2d-','') in model_info.keys()):
        mi = copy.deepcopy(model_info[model.replace('api2d-','')])
        mi.update({"endpoint": api2d_endpoint})
        model_info.update({model: mi})

# -=-=-=-=-=-=- azure 对齐支持 -=-=-=-=-=-=-
for model in AVAIL_LLM_MODELS:
    if model.startswith('azure-') and (model.replace('azure-','') in model_info.keys()):
        mi = copy.deepcopy(model_info[model.replace('azure-','')])
        mi.update({"endpoint": azure_endpoint})
        model_info.update({model: mi})

# -=-=-=-=-=-=- 以下部分是新加入的模型，可能附带额外依赖 -=-=-=-=-=-=-
# claude家族
claude_models = ["claude-instant-1.2","claude-2.0","claude-2.1","claude-3-haiku-20240307","claude-3-sonnet-20240229","claude-3-opus-20240229","claude-3-5-sonnet-20240620"]
if any(item in claude_models for item in AVAIL_LLM_MODELS):
    from .bridge_claude import predict_no_ui_long_connection as claude_noui
    from .bridge_claude import predict as claude_ui
    model_info.update({
        "claude-instant-1.2": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 100000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-2.0": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 100000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-2.1": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-haiku-20240307": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-sonnet-20240229": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-opus-20240229": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-5-sonnet-20240620": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_rwkv" in AVAIL_LLM_MODELS:
    from .bridge_jittorllms_rwkv import predict_no_ui_long_connection as rwkv_noui
    from .bridge_jittorllms_rwkv import predict as rwkv_ui
    model_info.update({
        "jittorllms_rwkv": {
            "fn_with_ui": rwkv_ui,
            "fn_without_ui": rwkv_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_llama" in AVAIL_LLM_MODELS:
    from .bridge_jittorllms_llama import predict_no_ui_long_connection as llama_noui
    from .bridge_jittorllms_llama import predict as llama_ui
    model_info.update({
        "jittorllms_llama": {
            "fn_with_ui": llama_ui,
            "fn_without_ui": llama_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_pangualpha" in AVAIL_LLM_MODELS:
    from .bridge_jittorllms_pangualpha import predict_no_ui_long_connection as pangualpha_noui
    from .bridge_jittorllms_pangualpha import predict as pangualpha_ui
    model_info.update({
        "jittorllms_pangualpha": {
            "fn_with_ui": pangualpha_ui,
            "fn_without_ui": pangualpha_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "moss" in AVAIL_LLM_MODELS:
    from .bridge_moss import predict_no_ui_long_connection as moss_noui
    from .bridge_moss import predict as moss_ui
    model_info.update({
        "moss": {
            "fn_with_ui": moss_ui,
            "fn_without_ui": moss_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "stack-claude" in AVAIL_LLM_MODELS:
    from .bridge_stackclaude import predict_no_ui_long_connection as claude_noui
    from .bridge_stackclaude import predict as claude_ui
    model_info.update({
        "stack-claude": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": None,
            "max_token": 8192,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        }
    })
if "newbing" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from .bridge_newbingfree import predict_no_ui_long_connection as newbingfree_noui
        from .bridge_newbingfree import predict as newbingfree_ui
        model_info.update({
            "newbing": {
                "fn_with_ui": newbingfree_ui,
                "fn_without_ui": newbingfree_noui,
                "endpoint": newbing_endpoint,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
if "chatglmft" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from .bridge_chatglmft import predict_no_ui_long_connection as chatglmft_noui
        from .bridge_chatglmft import predict as chatglmft_ui
        model_info.update({
            "chatglmft": {
                "fn_with_ui": chatglmft_ui,
                "fn_without_ui": chatglmft_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
# -=-=-=-=-=-=- 上海AI-LAB书生大模型 -=-=-=-=-=-=-
if "internlm" in AVAIL_LLM_MODELS:
    try:
        from .bridge_internlm import predict_no_ui_long_connection as internlm_noui
        from .bridge_internlm import predict as internlm_ui
        model_info.update({
            "internlm": {
                "fn_with_ui": internlm_ui,
                "fn_without_ui": internlm_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
if "chatglm_onnx" in AVAIL_LLM_MODELS:
    try:
        from .bridge_chatglmonnx import predict_no_ui_long_connection as chatglm_onnx_noui
        from .bridge_chatglmonnx import predict as chatglm_onnx_ui
        model_info.update({
            "chatglm_onnx": {
                "fn_with_ui": chatglm_onnx_ui,
                "fn_without_ui": chatglm_onnx_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
# -=-=-=-=-=-=- 通义-本地模型 -=-=-=-=-=-=-
if "qwen-local" in AVAIL_LLM_MODELS:
    try:
        from .bridge_qwen_local import predict_no_ui_long_connection as qwen_local_noui
        from .bridge_qwen_local import predict as qwen_local_ui
        model_info.update({
            "qwen-local": {
                "fn_with_ui": qwen_local_ui,
                "fn_without_ui": qwen_local_noui,
                "can_multi_thread": False,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())

# -=-=-=-=-=-=- 阿里云百炼（通义）-在线模型 -=-=-=-=-=-=-
qwen_models = ["qwen-max-latest", "qwen-max-2025-01-25","qwen-max","qwen-turbo","qwen-plus",
               "dashscope-deepseek-r1","dashscope-deepseek-v3",
               "dashscope-qwen3-14b", "dashscope-qwen3-235b-a22b", "dashscope-qwen3-qwen3-32b",
               ]
if any(item in qwen_models for item in AVAIL_LLM_MODELS):
    try:
        from .bridge_qwen import predict_no_ui_long_connection as qwen_noui
        from .bridge_qwen import predict as qwen_ui
        model_info.update({
            "qwen-turbo": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 100000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-plus": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 129024,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-max": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 30720,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-max-latest": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 30720,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-max-2025-01-25": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 30720,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "dashscope-deepseek-r1": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "enable_reasoning": True,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 57344,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "dashscope-deepseek-v3": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 57344,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "dashscope-qwen3-14b": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "enable_reasoning": True,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 129024,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "dashscope-qwen3-235b-a22b": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 129024,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "dashscope-qwen3-32b": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 129024,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())

# -=-=-=-=-=-=- 零一万物模型 -=-=-=-=-=-=-
yi_models = ["yi-34b-chat-0205","yi-34b-chat-200k","yi-large","yi-medium","yi-spark","yi-large-turbo","yi-large-preview"]
if any(item in yi_models for item in AVAIL_LLM_MODELS):
    try:
        yimodel_4k_noui, yimodel_4k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=600, disable_proxy=False
            )
        yimodel_16k_noui, yimodel_16k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=4000, disable_proxy=False
            )
        yimodel_200k_noui, yimodel_200k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=4096, disable_proxy=False
            )
        model_info.update({
            "yi-34b-chat-0205": {
                "fn_with_ui": yimodel_4k_ui,
                "fn_without_ui": yimodel_4k_noui,
                "can_multi_thread": False,  # 目前来说，默认情况下并发量极低，因此禁用
                "endpoint": yimodel_endpoint,
                "max_token": 4000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-34b-chat-200k": {
                "fn_with_ui": yimodel_200k_ui,
                "fn_without_ui": yimodel_200k_noui,
                "can_multi_thread": False,  # 目前来说，默认情况下并发量极低，因此禁用
                "endpoint": yimodel_endpoint,
                "max_token": 200000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # 目前来说，默认情况下并发量极低，因此禁用
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-medium": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": True,  # 这个并发量稍微大一点
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-spark": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": True,  # 这个并发量稍微大一点
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large-turbo": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # 目前来说，默认情况下并发量极低，因此禁用
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large-preview": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # 目前来说，默认情况下并发量极低，因此禁用
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
        })
    except:
        logger.error(trimmed_format_exc())


# -=-=-=-=-=-=- Grok model from x.ai -=-=-=-=-=-=-
grok_models = ["grok-beta"]
if any(item in grok_models for item in AVAIL_LLM_MODELS):
    try:
        grok_beta_128k_noui, grok_beta_128k_ui = get_predict_function(
            api_key_conf_name="GROK_API_KEY", max_output_token=8192, disable_proxy=False
        )

        model_info.update({
            "grok-beta": {
                "fn_with_ui": grok_beta_128k_ui,
                "fn_without_ui": grok_beta_128k_noui,
                "can_multi_thread": True,
                "endpoint": grok_model_endpoint,
                "max_token": 128000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },

        })
    except:
        logger.error(trimmed_format_exc())

# -=-=-=-=-=-=- 讯飞星火认知大模型 -=-=-=-=-=-=-
if "spark" in AVAIL_LLM_MODELS:
    try:
        from .bridge_spark import predict_no_ui_long_connection as spark_noui
        from .bridge_spark import predict as spark_ui
        model_info.update({
            "spark": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
if "sparkv2" in AVAIL_LLM_MODELS:   # 讯飞星火认知大模型
    try:
        from .bridge_spark import predict_no_ui_long_connection as spark_noui
        from .bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv2": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
if any(x in AVAIL_LLM_MODELS for x in ("sparkv3", "sparkv3.5", "sparkv4")):   # 讯飞星火认知大模型
    try:
        from .bridge_spark import predict_no_ui_long_connection as spark_noui
        from .bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv3": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "sparkv3.5": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "sparkv4":{
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
if "llama2" in AVAIL_LLM_MODELS:   # llama2
    try:
        from .bridge_llama2 import predict_no_ui_long_connection as llama2_noui
        from .bridge_llama2 import predict as llama2_ui
        model_info.update({
            "llama2": {
                "fn_with_ui": llama2_ui,
                "fn_without_ui": llama2_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())
# -=-=-=-=-=-=- 智谱 -=-=-=-=-=-=-
if "zhipuai" in AVAIL_LLM_MODELS:   # zhipuai 是glm-4的别名，向后兼容配置
    try:
        model_info.update({
            "zhipuai": {
                "fn_with_ui": zhipu_ui,
                "fn_without_ui": zhipu_noui,
                "endpoint": None,
                "max_token": 10124 * 8,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
        })
    except:
        logger.error(trimmed_format_exc())
# -=-=-=-=-=-=- 幻方-深度求索本地大模型 -=-=-=-=-=-=-
if "deepseekcoder" in AVAIL_LLM_MODELS:   # deepseekcoder
    try:
        from .bridge_deepseekcoder import predict_no_ui_long_connection as deepseekcoder_noui
        from .bridge_deepseekcoder import predict as deepseekcoder_ui
        model_info.update({
            "deepseekcoder": {
                "fn_with_ui": deepseekcoder_ui,
                "fn_without_ui": deepseekcoder_noui,
                "endpoint": None,
                "max_token": 2048,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        logger.error(trimmed_format_exc())

# -=-=-=-=-=-=- 幻方-深度求索大模型在线API -=-=-=-=-=-=-
claude_models = ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]
if any(item in claude_models for item in AVAIL_LLM_MODELS):
    try:
        deepseekapi_noui, deepseekapi_ui = get_predict_function(
            api_key_conf_name="DEEPSEEK_API_KEY", max_output_token=4096, disable_proxy=False
        )
        model_info.update({
            "deepseek-chat":{
                "fn_with_ui": deepseekapi_ui,
                "fn_without_ui": deepseekapi_noui,
                "endpoint": deepseekapi_endpoint,
                "can_multi_thread": True,
                "max_token": 64000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "deepseek-coder":{
                "fn_with_ui": deepseekapi_ui,
                "fn_without_ui": deepseekapi_noui,
                "endpoint": deepseekapi_endpoint,
                "can_multi_thread": True,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "deepseek-reasoner":{
                "fn_with_ui": deepseekapi_ui,
                "fn_without_ui": deepseekapi_noui,
                "endpoint": deepseekapi_endpoint,
                "can_multi_thread": True,
                "max_token": 64000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
                "enable_reasoning": True
            },
        })
    except:
        logger.error(trimmed_format_exc())

# -=-=-=-=-=-=- 火山引擎 对齐支持 -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("volcengine-")]:
    # 为了更灵活地接入volcengine多模型管理界面，设计了此接口，例子：AVAIL_LLM_MODELS = ["volcengine-deepseek-r1-250120(max_token=6666)"]
    # 其中
    #   "volcengine-"          是前缀（必要）
    #   "deepseek-r1-250120"   是模型名（必要）
    #   "(max_token=6666)"     是配置（非必要）
    model_info_extend = model_info
    model_info_extend.update({
        "deepseek-r1-250120": {
            "max_token": 16384,
            "enable_reasoning": True,
            "can_multi_thread": True,
            "endpoint": volcengine_endpoint,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
        "deepseek-v3-241226": {
            "max_token": 16384,
            "enable_reasoning": False,
            "can_multi_thread": True,
            "endpoint": volcengine_endpoint,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    try:
        origin_model_name, max_token_tmp = read_one_api_model_name(model)
        # 如果是已知模型，则尝试获取其信息
        original_model_info = model_info_extend.get(origin_model_name.replace("volcengine-", "", 1), None)
    except:
        logger.error(f"volcengine模型 {model} 的 max_token 配置不是整数，请检查配置文件。")
        continue

    volcengine_noui, volcengine_ui = get_predict_function(api_key_conf_name="ARK_API_KEY", max_output_token=8192, disable_proxy=True, model_remove_prefix = ["volcengine-"])

    this_model_info = {
        "fn_with_ui": volcengine_ui,
        "fn_without_ui": volcengine_noui,
        "endpoint": volcengine_endpoint,
        "can_multi_thread": True,
        "max_token": 64000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    }

    # 同步已知模型的其他信息
    attribute = "has_multimodal_capacity"
    if original_model_info is not None and original_model_info.get(attribute, None) is not None: this_model_info.update({attribute: original_model_info.get(attribute, None)})
    attribute = "enable_reasoning"
    if original_model_info is not None and original_model_info.get(attribute, None) is not None: this_model_info.update({attribute: original_model_info.get(attribute, None)})
    model_info.update({model: this_model_info})

# -=-=-=-=-=-=- one-api 对齐支持 -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("one-api-")]:
    # 为了更灵活地接入one-api多模型管理界面，设计了此接口，例子：AVAIL_LLM_MODELS = ["one-api-mixtral-8x7b(max_token=6666)"]
    # 其中
    #   "one-api-"          是前缀（必要）
    #   "mixtral-8x7b"      是模型名（必要）
    #   "(max_token=6666)"  是配置（非必要）
    try:
        origin_model_name, max_token_tmp = read_one_api_model_name(model)
        # 如果是已知模型，则尝试获取其信息
        original_model_info = model_info.get(origin_model_name.replace("one-api-", "", 1), None)
    except:
        logger.error(f"one-api模型 {model} 的 max_token 配置不是整数，请检查配置文件。")
        continue
    this_model_info = {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "can_multi_thread": True,
        "endpoint": openai_endpoint,
        "max_token": max_token_tmp,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    }

    # 同步已知模型的其他信息
    attribute = "has_multimodal_capacity"
    if original_model_info is not None and original_model_info.get(attribute, None) is not None: this_model_info.update({attribute: original_model_info.get(attribute, None)})
    # attribute = "attribute2"
    # if original_model_info is not None and original_model_info.get(attribute, None) is not None: this_model_info.update({attribute: original_model_info.get(attribute, None)})
    # attribute = "attribute3"
    # if original_model_info is not None and original_model_info.get(attribute, None) is not None: this_model_info.update({attribute: original_model_info.get(attribute, None)})
    model_info.update({model: this_model_info})

# -=-=-=-=-=-=- vllm 对齐支持 -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("vllm-")]:
    # 为了更灵活地接入vllm多模型管理界面，设计了此接口，例子：AVAIL_LLM_MODELS = ["vllm-/home/hmp/llm/cache/Qwen1___5-32B-Chat(max_token=6666)"]
    # 其中
    #   "vllm-"             是前缀（必要）
    #   "mixtral-8x7b"      是模型名（必要）
    #   "(max_token=6666)"  是配置（非必要）
    try:
        _, max_token_tmp = read_one_api_model_name(model)
    except:
        logger.error(f"vllm模型 {model} 的 max_token 配置不是整数，请检查配置文件。")
        continue
    model_info.update({
        model: {
            "fn_with_ui": chatgpt_ui,
            "fn_without_ui": chatgpt_noui,
            "can_multi_thread": True,
            "endpoint": openai_endpoint,
            "max_token": max_token_tmp,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
# -=-=-=-=-=-=- ollama 对齐支持 -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("ollama-")]:
    from .bridge_ollama import predict_no_ui_long_connection as ollama_noui
    from .bridge_ollama import predict as ollama_ui
    break
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("ollama-")]:
    # 为了更灵活地接入ollama多模型管理界面，设计了此接口，例子：AVAIL_LLM_MODELS = ["ollama-phi3(max_token=6666)"]
    # 其中
    #   "ollama-"           是前缀（必要）
    #   "phi3"            是模型名（必要）
    #   "(max_token=6666)"  是配置（非必要）
    try:
        _, max_token_tmp = read_one_api_model_name(model)
    except:
        logger.error(f"ollama模型 {model} 的 max_token 配置不是整数，请检查配置文件。")
        continue
    model_info.update({
        model: {
            "fn_with_ui": ollama_ui,
            "fn_without_ui": ollama_noui,
            "endpoint": ollama_endpoint,
            "max_token": max_token_tmp,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })

# -=-=-=-=-=-=- azure模型对齐支持 -=-=-=-=-=-=-
AZURE_CFG_ARRAY = get_conf("AZURE_CFG_ARRAY") # <-- 用于定义和切换多个azure模型 -->
if len(AZURE_CFG_ARRAY) > 0:
    for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
        # 可能会覆盖之前的配置，但这是意料之中的
        if not azure_model_name.startswith('azure'):
            raise ValueError("AZURE_CFG_ARRAY中配置的模型必须以azure开头")
        endpoint_ = azure_cfg_dict["AZURE_ENDPOINT"] + \
            f'openai/deployments/{azure_cfg_dict["AZURE_ENGINE"]}/chat/completions?api-version=2023-05-15'
        model_info.update({
            azure_model_name: {
                "fn_with_ui": chatgpt_ui,
                "fn_without_ui": chatgpt_noui,
                "endpoint": endpoint_,
                "azure_api_key": azure_cfg_dict["AZURE_API_KEY"],
                "max_token": azure_cfg_dict["AZURE_MODEL_MAX_TOKEN"],
                "tokenizer": tokenizer_gpt35,   # tokenizer只用于粗估token数量
                "token_cnt": get_token_num_gpt35,
            }
        })
        if azure_model_name not in AVAIL_LLM_MODELS:
            AVAIL_LLM_MODELS += [azure_model_name]

# -=-=-=-=-=-=- Openrouter模型对齐支持 -=-=-=-=-=-=-
# 为了更灵活地接入Openrouter路由，设计了此接口
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("openrouter-")]:
    from request_llms.bridge_openrouter import predict_no_ui_long_connection as openrouter_noui
    from request_llms.bridge_openrouter import predict as openrouter_ui
    model_info.update({
        model: {
            "fn_with_ui": openrouter_ui,
            "fn_without_ui": openrouter_noui,
            # 以下参数参考gpt-4o-mini的配置, 请根据实际情况修改
            "endpoint": openai_endpoint,
            "has_multimodal_capacity": True,
            "max_token": 128000,
            "tokenizer": tokenizer_gpt4,
            "token_cnt": get_token_num_gpt4,
        },
    })


# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=- ☝️ 以上是模型路由 -=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=

# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-= 👇 以下是多模型路由切换函数 -=-=-=-=-=-=-=
# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=


def LLM_CATCH_EXCEPTION(f):
    """
    装饰器函数，将错误显示出来
    """
    def decorated(inputs:str, llm_kwargs:dict, history:list, sys_prompt:str, observe_window:list, console_silence:bool):
        try:
            return f(inputs, llm_kwargs, history, sys_prompt, observe_window, console_silence)
        except Exception as e:
            tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
            observe_window[0] = tb_str
            return tb_str
    return decorated


def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list, sys_prompt:str, observe_window:list=[], console_silence:bool=False):
    """
    发送至LLM，等待回复，一次性完成，不显示中间过程。但内部（尽可能地）用stream的方法避免中途网线被掐。
    inputs：
        是本次问询的输入
    sys_prompt:
        系统静默prompt
    llm_kwargs：
        LLM的内部调优参数
    history：
        是之前的对话列表
    observe_window = None：
        用于负责跨越线程传递已经输出的部分，大部分时候仅仅为了fancy的视觉效果，留空即可。observe_window[0]：观测窗。observe_window[1]：看门狗
    """
    import threading, time, copy

    inputs = apply_gpt_academic_string_mask(inputs, mode="show_llm")
    model = llm_kwargs['llm_model']
    n_model = 1
    if '&' not in model:
        # 如果只询问“一个”大语言模型（多数情况）：
        method = model_info[model]["fn_without_ui"]
        return method(inputs, llm_kwargs, history, sys_prompt, observe_window, console_silence)
    else:
        # 如果同时询问“多个”大语言模型，这个稍微啰嗦一点，但思路相同，您不必读这个else分支
        executor = ThreadPoolExecutor(max_workers=4)
        models = model.split('&')
        n_model = len(models)

        window_len = len(observe_window)
        assert window_len==3
        window_mutex = [["", time.time(), ""] for _ in range(n_model)] + [True]

        futures = []
        for i in range(n_model):
            model = models[i]
            method = model_info[model]["fn_without_ui"]
            llm_kwargs_feedin = copy.deepcopy(llm_kwargs)
            llm_kwargs_feedin['llm_model'] = model
            future = executor.submit(LLM_CATCH_EXCEPTION(method), inputs, llm_kwargs_feedin, history, sys_prompt, window_mutex[i], console_silence)
            futures.append(future)

        def mutex_manager(window_mutex, observe_window):
            while True:
                time.sleep(0.25)
                if not window_mutex[-1]: break
                # 看门狗（watchdog）
                for i in range(n_model):
                    window_mutex[i][1] = observe_window[1]
                # 观察窗（window）
                chat_string = []
                for i in range(n_model):
                    color = colors[i%len(colors)]
                    chat_string.append( f"【{str(models[i])} 说】: <font color=\"{color}\"> {window_mutex[i][0]} </font>" )
                res = '<br/><br/>\n\n---\n\n'.join(chat_string)
                # # # # # # # # # # #
                observe_window[0] = res

        t_model = threading.Thread(target=mutex_manager, args=(window_mutex, observe_window), daemon=True)
        t_model.start()

        return_string_collect = []
        while True:
            worker_done = [h.done() for h in futures]
            if all(worker_done):
                executor.shutdown()
                break
            time.sleep(1)

        for i, future in enumerate(futures):  # wait and get
            color = colors[i%len(colors)]
            return_string_collect.append( f"【{str(models[i])} 说】: <font color=\"{color}\"> {future.result()} </font>" )

        window_mutex[-1] = False # stop mutex thread
        res = '<br/><br/>\n\n---\n\n'.join(return_string_collect)
        return res

# 根据基础功能区 ModelOverride 参数调整模型类型，用于 `predict` 中

def execute_model_override(llm_kwargs, additional_fn, method):
    functional = core_functional.get_core_functions()
    if (additional_fn in functional) and 'ModelOverride' in functional[additional_fn]:
        # 热更新Prompt & ModelOverride
        importlib.reload(core_functional)
        functional = core_functional.get_core_functions()
        model_override = functional[additional_fn]['ModelOverride']
        if model_override not in model_info:
            raise ValueError(f"模型覆盖参数 '{model_override}' 指向一个暂不支持的模型，请检查配置文件。")
        method = model_info[model_override]["fn_with_ui"]
        llm_kwargs['llm_model'] = model_override
        return llm_kwargs, additional_fn, method
    # 默认返回原参数
    return llm_kwargs, additional_fn, method

def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
    发送至LLM，流式获取输出。
    用于基础的对话功能。

    完整参数列表：
        predict(
            inputs:str,                     # 是本次问询的输入
            llm_kwargs:dict,                # 是LLM的内部调优参数
            plugin_kwargs:dict,             # 是插件的内部参数
            chatbot:ChatBotWithCookies,     # 原样传递，负责向用户前端展示对话，兼顾前端状态的功能
            history:list=[],                # 是之前的对话列表
            system_prompt:str='',           # 系统静默prompt
            stream:bool=True,               # 是否流式输出（已弃用）
            additional_fn:str=None          # 基础功能区按钮的附加功能
        ):
    """

    inputs = apply_gpt_academic_string_mask(inputs, mode="show_llm")

    if llm_kwargs['llm_model'] not in model_info:
        from toolbox import update_ui
        chatbot.append([inputs, f"很抱歉，模型 '{llm_kwargs['llm_model']}' 暂不支持<br/>(1) 检查config中的AVAIL_LLM_MODELS选项<br/>(2) 检查request_llms/bridge_all.py中的模型路由"])
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    method = model_info[llm_kwargs['llm_model']]["fn_with_ui"]  # 如果这里报错，检查config中的AVAIL_LLM_MODELS选项

    if additional_fn: # 根据基础功能区 ModelOverride 参数调整模型类型
        llm_kwargs, additional_fn, method = execute_model_override(llm_kwargs, additional_fn, method)

    if start_with_url(inputs):
        yield from load_web_content(inputs, chatbot, history)
        return

    if contain_uploaded_files(inputs):
        inputs = yield from load_uploaded_files(inputs, method, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, stream, additional_fn)

    # 更新一下llm_kwargs的参数，否则会出现参数不匹配的问题
    yield from method(inputs, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, stream, additional_fn)



# ----------------------------------------------------------------------
# MODULE: shared_utils.nltk_downloader
# SOURCE: shared_utils/nltk_downloader.py
# ----------------------------------------------------------------------

# Natural Language Toolkit: Corpus & Model Downloader
#
# Copyright (C) 2001-2023 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

# ----------------------------------------------------------------------

"""

  0     1  2    3
[label][----][label][----]
[column  ][column     ]

Notes
=====
Handling data files..  Some questions:

* Should the data files be kept zipped or unzipped?  I say zipped.

* Should the data files be kept in svn at all?  Advantages: history;
  automatic version numbers; 'svn up' could be used rather than the
  downloader to update the corpora.  Disadvantages: they're big,
  which makes working from svn a bit of a pain.  And we're planning
  to potentially make them much bigger.  I don't think we want
  people to have to download 400MB corpora just to use nltk from svn.

* Compromise: keep the data files in trunk/data rather than in
  trunk/nltk.  That way you can check them out in svn if you want
  to; but you don't need to, and you can use the downloader instead.

* Also: keep models in mind.  When we change the code, we'd
  potentially like the models to get updated.  This could require a
  little thought.

* So.. let's assume we have a trunk/data directory, containing a bunch
  of packages.  The packages should be kept as zip files, because we
  really shouldn't be editing them much (well -- we may edit models
  more, but they tend to be binary-ish files anyway, where diffs
  aren't that helpful).  So we'll have trunk/data, with a bunch of
  files like abc.zip and treebank.zip and propbank.zip.  For each
  package we could also have eg treebank.xml and propbank.xml,
  describing the contents of the package (name, copyright, license,
  etc).  Collections would also have .xml files.  Finally, we would
  pull all these together to form a single index.xml file.  Some
  directory structure wouldn't hurt.  So how about::

    /trunk/data/ ....................... root of data svn
      index.xml ........................ main index file
      src/ ............................. python scripts
      packages/ ........................ dir for packages
        corpora/ ....................... zip & xml files for corpora
        grammars/ ...................... zip & xml files for grammars
        taggers/ ....................... zip & xml files for taggers
        tokenizers/ .................... zip & xml files for tokenizers
        etc.
      collections/ ..................... xml files for collections

  Where the root (/trunk/data) would contain a makefile; and src/
  would contain a script to update the info.xml file.  It could also
  contain scripts to rebuild some of the various model files.  The
  script that builds index.xml should probably check that each zip
  file expands entirely into a single subdir, whose name matches the
  package's uid.

Changes I need to make:
  - in index: change "size" to "filesize" or "compressed-size"
  - in index: add "unzipped-size"
  - when checking status: check both compressed & uncompressed size.
    uncompressed size is important to make sure we detect a problem
    if something got partially unzipped.  define new status values
    to differentiate stale vs corrupt vs corruptly-uncompressed??
    (we shouldn't need to re-download the file if the zip file is ok
    but it didn't get uncompressed fully.)
  - add other fields to the index: author, license, copyright, contact,
    etc.

the current grammars/ package would become a single new package (eg
toy-grammars or book-grammars).

xml file should have:
  - authorship info
  - license info
  - copyright info
  - contact info
  - info about what type of data/annotation it contains?
  - recommended corpus reader?

collections can contain other collections.  they can also contain
multiple package types (corpora & models).  Have a single 'basics'
package that includes everything we talk about in the book?

n.b.: there will have to be a fallback to the punkt tokenizer, in case
they didn't download that model.

default: unzip or not?

"""

try:
    TKINTER = True
    from tkinter import Button, Canvas, Entry, Frame, IntVar, Label, Menu, TclError, Tk
    from tkinter.messagebox import showerror

    from nltk.draw.table import Table
    from nltk.draw.util import ShowText
except ImportError:
    TKINTER = False
    TclError = ValueError


# urllib2 = nltk.internals.import_from_stdlib('urllib2')


######################################################################
# Directory entry objects (from the data server's index file)
######################################################################


class Package:
    """
    A directory entry for a downloadable package.  These entries are
    extracted from the XML index file that is downloaded by
    ``Downloader``.  Each package consists of a single file; but if
    that file is a zip file, then it can be automatically decompressed
    when the package is installed.
    """

    def __init__(
        self,
        id,
        url,
        name=None,
        subdir="",
        size=None,
        unzipped_size=None,
        checksum=None,
        svn_revision=None,
        copyright="Unknown",
        contact="Unknown",
        license="Unknown",
        author="Unknown",
        unzip=True,
        **kw,
    ):
        self.id = id
        """A unique identifier for this package."""

        self.name = name or id
        """A string name for this package."""

        self.subdir = subdir
        """The subdirectory where this package should be installed.
           E.g., ``'corpora'`` or ``'taggers'``."""

        self.url = url
        """A URL that can be used to download this package's file."""

        self.size = int(size)
        """The filesize (in bytes) of the package file."""

        self.unzipped_size = int(unzipped_size)
        """The total filesize of the files contained in the package's
           zipfile."""

        self.checksum = checksum
        """The MD-5 checksum of the package file."""

        self.svn_revision = svn_revision
        """A subversion revision number for this package."""

        self.copyright = copyright
        """Copyright holder for this package."""

        self.contact = contact
        """Name & email of the person who should be contacted with
           questions about this package."""

        self.license = license
        """License information for this package."""

        self.author = author
        """Author of this package."""

        ext = os.path.splitext(url.split("/")[-1])[1]
        self.filename = os.path.join(subdir, id + ext)
        """The filename that should be used for this package's file.  It
           is formed by joining ``self.subdir`` with ``self.id``, and
           using the same extension as ``url``."""

        self.unzip = bool(int(unzip))  # '0' or '1'
        """A flag indicating whether this corpus should be unzipped by
           default."""

        # Include any other attributes provided by the XML file.
        self.__dict__.update(kw)

    @staticmethod
    def fromxml(xml):
        if isinstance(xml, str):
            xml = ElementTree.parse(xml)
        for key in xml.attrib:
            xml.attrib[key] = str(xml.attrib[key])
        return Package(**xml.attrib)

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "<Package %s>" % self.id


class Collection:
    """
    A directory entry for a collection of downloadable packages.
    These entries are extracted from the XML index file that is
    downloaded by ``Downloader``.
    """

    def __init__(self, id, children, name=None, **kw):
        self.id = id
        """A unique identifier for this collection."""

        self.name = name or id
        """A string name for this collection."""

        self.children = children
        """A list of the ``Collections`` or ``Packages`` directly
           contained by this collection."""

        self.packages = None
        """A list of ``Packages`` contained by this collection or any
           collections it recursively contains."""

        # Include any other attributes provided by the XML file.
        self.__dict__.update(kw)

    @staticmethod
    def fromxml(xml):
        if isinstance(xml, str):
            xml = ElementTree.parse(xml)
        for key in xml.attrib:
            xml.attrib[key] = str(xml.attrib[key])
        children = [child.get("ref") for child in xml.findall("item")]
        return Collection(children=children, **xml.attrib)

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "<Collection %s>" % self.id


######################################################################
# Message Passing Objects
######################################################################


class DownloaderMessage:
    """A status message object, used by ``incr_download`` to
    communicate its progress."""


class StartCollectionMessage(DownloaderMessage):
    """Data server has started working on a collection of packages."""

    def __init__(self, collection):
        self.collection = collection


class FinishCollectionMessage(DownloaderMessage):
    """Data server has finished working on a collection of packages."""

    def __init__(self, collection):
        self.collection = collection


class StartPackageMessage(DownloaderMessage):
    """Data server has started working on a package."""

    def __init__(self, package):
        self.package = package


class FinishPackageMessage(DownloaderMessage):
    """Data server has finished working on a package."""

    def __init__(self, package):
        self.package = package


class StartDownloadMessage(DownloaderMessage):
    """Data server has started downloading a package."""

    def __init__(self, package):
        self.package = package


class FinishDownloadMessage(DownloaderMessage):
    """Data server has finished downloading a package."""

    def __init__(self, package):
        self.package = package


class StartUnzipMessage(DownloaderMessage):
    """Data server has started unzipping a package."""

    def __init__(self, package):
        self.package = package


class FinishUnzipMessage(DownloaderMessage):
    """Data server has finished unzipping a package."""

    def __init__(self, package):
        self.package = package


class UpToDateMessage(DownloaderMessage):
    """The package download file is already up-to-date"""

    def __init__(self, package):
        self.package = package


class StaleMessage(DownloaderMessage):
    """The package download file is out-of-date or corrupt"""

    def __init__(self, package):
        self.package = package


class ErrorMessage(DownloaderMessage):
    """Data server encountered an error"""

    def __init__(self, package, message):
        self.package = package
        if isinstance(message, Exception):
            self.message = str(message)
        else:
            self.message = message


class ProgressMessage(DownloaderMessage):
    """Indicates how much progress the data server has made"""

    def __init__(self, progress):
        self.progress = progress


class SelectDownloadDirMessage(DownloaderMessage):
    """Indicates what download directory the data server is using"""

    def __init__(self, download_dir):
        self.download_dir = download_dir


######################################################################
# NLTK Data Server
######################################################################


class Downloader:
    """
    A class used to access the NLTK data server, which can be used to
    download corpora and other data packages.
    """

    # /////////////////////////////////////////////////////////////////
    # Configuration
    # /////////////////////////////////////////////////////////////////

    INDEX_TIMEOUT = 60 * 60  # 1 hour
    """The amount of time after which the cached copy of the data
       server index will be considered 'stale,' and will be
       re-downloaded."""

    DEFAULT_URL = "https://public.agent-matrix.com/publish/nltk/index.xml"
    """The default URL for the NLTK data server's index.  An
       alternative URL can be specified when creating a new
       ``Downloader`` object."""

    # /////////////////////////////////////////////////////////////////
    # Status Constants
    # /////////////////////////////////////////////////////////////////

    INSTALLED = "installed"
    """A status string indicating that a package or collection is
       installed and up-to-date."""
    NOT_INSTALLED = "not installed"
    """A status string indicating that a package or collection is
       not installed."""
    STALE = "out of date"
    """A status string indicating that a package or collection is
       corrupt or out-of-date."""
    PARTIAL = "partial"
    """A status string indicating that a collection is partially
       installed (i.e., only some of its packages are installed.)"""

    # /////////////////////////////////////////////////////////////////
    # Constructor
    # /////////////////////////////////////////////////////////////////

    def __init__(self, server_index_url=None, download_dir=None):
        self._url = server_index_url or self.DEFAULT_URL
        """The URL for the data server's index file."""

        self._collections = {}
        """Dictionary from collection identifier to ``Collection``"""

        self._packages = {}
        """Dictionary from package identifier to ``Package``"""

        self._download_dir = download_dir
        """The default directory to which packages will be downloaded."""

        self._index = None
        """The XML index file downloaded from the data server"""

        self._index_timestamp = None
        """Time at which ``self._index`` was downloaded.  If it is more
           than ``INDEX_TIMEOUT`` seconds old, it will be re-downloaded."""

        self._status_cache = {}
        """Dictionary from package/collection identifier to status
           string (``INSTALLED``, ``NOT_INSTALLED``, ``STALE``, or
           ``PARTIAL``).  Cache is used for packages only, not
           collections."""

        self._errors = None
        """Flag for telling if all packages got successfully downloaded or not."""

        # decide where we're going to save things to.
        if self._download_dir is None:
            self._download_dir = self.default_download_dir()

    # /////////////////////////////////////////////////////////////////
    # Information
    # /////////////////////////////////////////////////////////////////

    def list(
        self,
        download_dir=None,
        show_packages=True,
        show_collections=True,
        header=True,
        more_prompt=False,
        skip_installed=False,
    ):
        lines = 0  # for more_prompt
        if download_dir is None:
            download_dir = self._download_dir
            print("Using default data directory (%s)" % download_dir)
        if header:
            print("=" * (26 + len(self._url)))
            print(" Data server index for <%s>" % self._url)
            print("=" * (26 + len(self._url)))
            lines += 3  # for more_prompt
        stale = partial = False

        categories = []
        if show_packages:
            categories.append("packages")
        if show_collections:
            categories.append("collections")
        for category in categories:
            print("%s:" % category.capitalize())
            lines += 1  # for more_prompt
            for info in sorted(getattr(self, category)(), key=str):
                status = self.status(info, download_dir)
                if status == self.INSTALLED and skip_installed:
                    continue
                if status == self.STALE:
                    stale = True
                if status == self.PARTIAL:
                    partial = True
                prefix = {
                    self.INSTALLED: "*",
                    self.STALE: "-",
                    self.PARTIAL: "P",
                    self.NOT_INSTALLED: " ",
                }[status]
                name = textwrap.fill(
                    "-" * 27 + (info.name or info.id), 75, subsequent_indent=27 * " "
                )[27:]
                print("  [{}] {} {}".format(prefix, info.id.ljust(20, "."), name))
                lines += len(name.split("\n"))  # for more_prompt
                if more_prompt and lines > 20:
                    user_input = input("Hit Enter to continue: ")
                    if user_input.lower() in ("x", "q"):
                        return
                    lines = 0
            print()
        msg = "([*] marks installed packages"
        if stale:
            msg += "; [-] marks out-of-date or corrupt packages"
        if partial:
            msg += "; [P] marks partially installed collections"
        print(textwrap.fill(msg + ")", subsequent_indent=" ", width=76))

    def packages(self):
        self._update_index()
        return self._packages.values()

    def corpora(self):
        self._update_index()
        return [pkg for (id, pkg) in self._packages.items() if pkg.subdir == "corpora"]

    def models(self):
        self._update_index()
        return [pkg for (id, pkg) in self._packages.items() if pkg.subdir != "corpora"]

    def collections(self):
        self._update_index()
        return self._collections.values()

    # /////////////////////////////////////////////////////////////////
    # Downloading
    # /////////////////////////////////////////////////////////////////

    def _info_or_id(self, info_or_id):
        if isinstance(info_or_id, str):
            return self.info(info_or_id)
        else:
            return info_or_id

    # [xx] When during downloading is it 'safe' to abort?  Only unsafe
    # time is *during* an unzip -- we don't want to leave a
    # partially-unzipped corpus in place because we wouldn't notice
    # it.  But if we had the exact total size of the unzipped corpus,
    # then that would be fine.  Then we could abort anytime we want!
    # So this is really what we should do.  That way the threaded
    # downloader in the gui can just kill the download thread anytime
    # it wants.

    def incr_download(self, info_or_id, download_dir=None, force=False):
        # If they didn't specify a download_dir, then use the default one.
        if download_dir is None:
            download_dir = self._download_dir
            yield SelectDownloadDirMessage(download_dir)

        # If they gave us a list of ids, then download each one.
        if isinstance(info_or_id, (list, tuple)):
            yield from self._download_list(info_or_id, download_dir, force)
            return

        # Look up the requested collection or package.
        try:
            info = self._info_or_id(info_or_id)
        except (OSError, ValueError) as e:
            yield ErrorMessage(None, f"Error loading {info_or_id}: {e}")
            return

        # Handle collections.
        if isinstance(info, Collection):
            yield StartCollectionMessage(info)
            yield from self.incr_download(info.children, download_dir, force)
            yield FinishCollectionMessage(info)

        # Handle Packages (delegate to a helper function).
        else:
            yield from self._download_package(info, download_dir, force)

    def _num_packages(self, item):
        if isinstance(item, Package):
            return 1
        else:
            return len(item.packages)

    def _download_list(self, items, download_dir, force):
        # Look up the requested items.
        for i in range(len(items)):
            try:
                items[i] = self._info_or_id(items[i])
            except (OSError, ValueError) as e:
                yield ErrorMessage(items[i], e)
                return

        # Download each item, re-scaling their progress.
        num_packages = sum(self._num_packages(item) for item in items)
        progress = 0
        for i, item in enumerate(items):
            if isinstance(item, Package):
                delta = 1.0 / num_packages
            else:
                delta = len(item.packages) / num_packages
            for msg in self.incr_download(item, download_dir, force):
                if isinstance(msg, ProgressMessage):
                    yield ProgressMessage(progress + msg.progress * delta)
                else:
                    yield msg

            progress += 100 * delta

    def _download_package(self, info, download_dir, force):
        yield StartPackageMessage(info)
        yield ProgressMessage(0)

        # Do we already have the current version?
        status = self.status(info, download_dir)
        if not force and status == self.INSTALLED:
            yield UpToDateMessage(info)
            yield ProgressMessage(100)
            yield FinishPackageMessage(info)
            return

        # Remove the package from our status cache
        self._status_cache.pop(info.id, None)

        # Check for (and remove) any old/stale version.
        filepath = os.path.join(download_dir, info.filename)
        if os.path.exists(filepath):
            if status == self.STALE:
                yield StaleMessage(info)
            os.remove(filepath)

        # Ensure the download_dir exists
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        if not os.path.exists(os.path.join(download_dir, info.subdir)):
            os.makedirs(os.path.join(download_dir, info.subdir))

        # Download the file.  This will raise an IOError if the url
        # is not found.
        yield StartDownloadMessage(info)
        yield ProgressMessage(5)
        try:
            # logger.info('+++====' + info.url)
            infile = urlopen(info.url)
            with open(filepath, "wb") as outfile:
                num_blocks = max(1, info.size / (1024 * 16))
                for block in itertools.count():
                    s = infile.read(1024 * 16)  # 16k blocks.
                    outfile.write(s)
                    if not s:
                        break
                    if block % 2 == 0:  # how often?
                        yield ProgressMessage(min(80, 5 + 75 * (block / num_blocks)))
            infile.close()
        except OSError as e:
            yield ErrorMessage(
                info,
                "Error downloading %r from <%s>:" "\n  %s" % (info.id, info.url, e),
            )
            return
        yield FinishDownloadMessage(info)
        yield ProgressMessage(80)

        # If it's a zipfile, uncompress it.
        if info.filename.endswith(".zip"):
            zipdir = os.path.join(download_dir, info.subdir)
            # Unzip if we're unzipping by default; *or* if it's already
            # been unzipped (presumably a previous version).
            if info.unzip or os.path.exists(os.path.join(zipdir, info.id)):
                yield StartUnzipMessage(info)
                for msg in _unzip_iter(filepath, zipdir, verbose=False):
                    # Somewhat of a hack, but we need a proper package reference
                    msg.package = info
                    yield msg
                yield FinishUnzipMessage(info)

        yield FinishPackageMessage(info)

    def download(
        self,
        info_or_id=None,
        download_dir=None,
        quiet=False,
        force=False,
        prefix="[nltk_data] ",
        halt_on_error=True,
        raise_on_error=False,
        print_error_to=sys.stderr,
    ):

        print_to = functools.partial(print, file=print_error_to)
        # If no info or id is given, then use the interactive shell.
        if info_or_id is None:
            # [xx] hmm -- changing self._download_dir here seems like
            # the wrong thing to do.  Maybe the _interactive_download
            # function should make a new copy of self to use?
            if download_dir is not None:
                self._download_dir = download_dir
            self._interactive_download()
            return True

        else:
            # Define a helper function for displaying output:
            def show(s, prefix2=""):
                print_to(
                    textwrap.fill(
                        s,
                        initial_indent=prefix + prefix2,
                        subsequent_indent=prefix + prefix2 + " " * 4,
                    )
                )

            for msg in self.incr_download(info_or_id, download_dir, force):
                # Error messages
                if isinstance(msg, ErrorMessage):
                    show(msg.message)
                    if raise_on_error:
                        raise ValueError(msg.message)
                    if halt_on_error:
                        return False
                    self._errors = True
                    if not quiet:
                        print_to("Error installing package. Retry? [n/y/e]")
                        choice = input().strip()
                        if choice in ["y", "Y"]:
                            if not self.download(
                                msg.package.id,
                                download_dir,
                                quiet,
                                force,
                                prefix,
                                halt_on_error,
                                raise_on_error,
                            ):
                                return False
                        elif choice in ["e", "E"]:
                            return False

                # All other messages
                if not quiet:
                    # Collection downloading messages:
                    if isinstance(msg, StartCollectionMessage):
                        show("Downloading collection %r" % msg.collection.id)
                        prefix += "   | "
                        print_to(prefix)
                    elif isinstance(msg, FinishCollectionMessage):
                        print_to(prefix)
                        prefix = prefix[:-4]
                        if self._errors:
                            show(
                                "Downloaded collection %r with errors"
                                % msg.collection.id
                            )
                        else:
                            show("Done downloading collection %s" % msg.collection.id)

                    # Package downloading messages:
                    elif isinstance(msg, StartPackageMessage):
                        show(
                            "Downloading package %s to %s..."
                            % (msg.package.id, download_dir)
                        )
                    elif isinstance(msg, UpToDateMessage):
                        show("Package %s is already up-to-date!" % msg.package.id, "  ")
                    # elif isinstance(msg, StaleMessage):
                    #    show('Package %s is out-of-date or corrupt' %
                    #         msg.package.id, '  ')
                    elif isinstance(msg, StartUnzipMessage):
                        show("Unzipping %s." % msg.package.filename, "  ")

                    # Data directory message:
                    elif isinstance(msg, SelectDownloadDirMessage):
                        download_dir = msg.download_dir
        return True

    def is_stale(self, info_or_id, download_dir=None):
        return self.status(info_or_id, download_dir) == self.STALE

    def is_installed(self, info_or_id, download_dir=None):
        return self.status(info_or_id, download_dir) == self.INSTALLED

    def clear_status_cache(self, id=None):
        if id is None:
            self._status_cache.clear()
        else:
            self._status_cache.pop(id, None)

    def status(self, info_or_id, download_dir=None):
        """
        Return a constant describing the status of the given package
        or collection.  Status can be one of ``INSTALLED``,
        ``NOT_INSTALLED``, ``STALE``, or ``PARTIAL``.
        """
        if download_dir is None:
            download_dir = self._download_dir
        info = self._info_or_id(info_or_id)

        # Handle collections:
        if isinstance(info, Collection):
            pkg_status = [self.status(pkg.id) for pkg in info.packages]
            if self.STALE in pkg_status:
                return self.STALE
            elif self.PARTIAL in pkg_status:
                return self.PARTIAL
            elif self.INSTALLED in pkg_status and self.NOT_INSTALLED in pkg_status:
                return self.PARTIAL
            elif self.NOT_INSTALLED in pkg_status:
                return self.NOT_INSTALLED
            else:
                return self.INSTALLED

        # Handle packages:
        else:
            filepath = os.path.join(download_dir, info.filename)
            if download_dir != self._download_dir:
                return self._pkg_status(info, filepath)
            else:
                if info.id not in self._status_cache:
                    self._status_cache[info.id] = self._pkg_status(info, filepath)
                return self._status_cache[info.id]

    def _pkg_status(self, info, filepath):
        if not os.path.exists(filepath):
            return self.NOT_INSTALLED

        # Check if the file has the correct size.
        try:
            filestat = os.stat(filepath)
        except OSError:
            return self.NOT_INSTALLED
        if filestat.st_size != int(info.size):
            return self.STALE

        # Check if the file's checksum matches
        if md5_hexdigest(filepath) != info.checksum:
            return self.STALE

        # If it's a zipfile, and it's been at least partially
        # unzipped, then check if it's been fully unzipped.
        if filepath.endswith(".zip"):
            unzipdir = filepath[:-4]
            if not os.path.exists(unzipdir):
                return self.INSTALLED  # but not unzipped -- ok!
            if not os.path.isdir(unzipdir):
                return self.STALE

            unzipped_size = sum(
                os.stat(os.path.join(d, f)).st_size
                for d, _, files in os.walk(unzipdir)
                for f in files
            )
            if unzipped_size != info.unzipped_size:
                return self.STALE

        # Otherwise, everything looks good.
        return self.INSTALLED

    def update(self, quiet=False, prefix="[nltk_data] "):
        """
        Re-download any packages whose status is STALE.
        """
        self.clear_status_cache()
        for pkg in self.packages():
            if self.status(pkg) == self.STALE:
                self.download(pkg, quiet=quiet, prefix=prefix)

    # /////////////////////////////////////////////////////////////////
    # Index
    # /////////////////////////////////////////////////////////////////

    def _update_index(self, url=None):
        """A helper function that ensures that self._index is
        up-to-date.  If the index is older than self.INDEX_TIMEOUT,
        then download it again."""
        # Check if the index is already up-to-date.  If so, do nothing.
        if not (
            self._index is None
            or url is not None
            or time.time() - self._index_timestamp > self.INDEX_TIMEOUT
        ):
            return

        # If a URL was specified, then update our URL.
        self._url = url or self._url

        # Download the index file.
        # logger.info('+++====' + self._url)
        self._index = nltk.internals.ElementWrapper(
            ElementTree.parse(urlopen(self._url)).getroot()
        )
        self._index_timestamp = time.time()

        # Build a dictionary of packages.
        packages = [Package.fromxml(p) for p in self._index.findall("packages/package")]
        self._packages = {p.id: p for p in packages}

        # Build a dictionary of collections.
        collections = [
            Collection.fromxml(c) for c in self._index.findall("collections/collection")
        ]
        self._collections = {c.id: c for c in collections}

        # Replace identifiers with actual children in collection.children.
        for collection in self._collections.values():
            for i, child_id in enumerate(collection.children):
                if child_id in self._packages:
                    collection.children[i] = self._packages[child_id]
                elif child_id in self._collections:
                    collection.children[i] = self._collections[child_id]
                else:
                    print(
                        "removing collection member with no package: {}".format(
                            child_id
                        )
                    )
                    del collection.children[i]

        # Fill in collection.packages for each collection.
        for collection in self._collections.values():
            packages = {}
            queue = [collection]
            for child in queue:
                if isinstance(child, Collection):
                    queue.extend(child.children)
                elif isinstance(child, Package):
                    packages[child.id] = child
                else:
                    pass
            collection.packages = packages.values()

        # Flush the status cache
        self._status_cache.clear()

    def index(self):
        """
        Return the XML index describing the packages available from
        the data server.  If necessary, this index will be downloaded
        from the data server.
        """
        self._update_index()
        return self._index

    def info(self, id):
        """Return the ``Package`` or ``Collection`` record for the
        given item."""
        self._update_index()
        if id in self._packages:
            return self._packages[id]
        if id in self._collections:
            return self._collections[id]
        raise ValueError("Package %r not found in index" % id)

    def xmlinfo(self, id):
        """Return the XML info record for the given item"""
        self._update_index()
        for package in self._index.findall("packages/package"):
            if package.get("id") == id:
                return package
        for collection in self._index.findall("collections/collection"):
            if collection.get("id") == id:
                return collection
        raise ValueError("Package %r not found in index" % id)

    # /////////////////////////////////////////////////////////////////
    # URL & Data Directory
    # /////////////////////////////////////////////////////////////////

    def _get_url(self):
        """The URL for the data server's index file."""
        return self._url

    def _set_url(self, url):
        """
        Set a new URL for the data server. If we're unable to contact
        the given url, then the original url is kept.
        """
        original_url = self._url
        try:
            self._update_index(url)
        except:
            self._url = original_url
            raise

    url = property(_get_url, _set_url)

    def default_download_dir(self):
        """
        Return the directory to which packages will be downloaded by
        default.  This value can be overridden using the constructor,
        or on a case-by-case basis using the ``download_dir`` argument when
        calling ``download()``.

        On Windows, the default download directory is
        ``PYTHONHOME/lib/nltk``, where *PYTHONHOME* is the
        directory containing Python, e.g. ``C:\\Python25``.

        On all other platforms, the default directory is the first of
        the following which exists or which can be created with write
        permission: ``/usr/share/nltk_data``, ``/usr/local/share/nltk_data``,
        ``/usr/lib/nltk_data``, ``/usr/local/lib/nltk_data``, ``~/nltk_data``.
        """
        # Check if we are on GAE where we cannot write into filesystem.
        if "APPENGINE_RUNTIME" in os.environ:
            return

        # Check if we have sufficient permissions to install in a
        # variety of system-wide locations.
        for nltkdir in nltk.data.path:
            if os.path.exists(nltkdir) and nltk.internals.is_writable(nltkdir):
                return nltkdir

        # On Windows, use %APPDATA%
        if sys.platform == "win32" and "APPDATA" in os.environ:
            homedir = os.environ["APPDATA"]

        # Otherwise, install in the user's home directory.
        else:
            homedir = os.path.expanduser("~/")
            if homedir == "~/":
                raise ValueError("Could not find a default download directory")

        # append "nltk_data" to the home directory
        return os.path.join(homedir, "nltk_data")

    def _get_download_dir(self):
        """
        The default directory to which packages will be downloaded.
        This defaults to the value returned by ``default_download_dir()``.
        To override this default on a case-by-case basis, use the
        ``download_dir`` argument when calling ``download()``.
        """
        return self._download_dir

    def _set_download_dir(self, download_dir):
        self._download_dir = download_dir
        # Clear the status cache.
        self._status_cache.clear()

    download_dir = property(_get_download_dir, _set_download_dir)

    # /////////////////////////////////////////////////////////////////
    # Interactive Shell
    # /////////////////////////////////////////////////////////////////

    def _interactive_download(self):
        # Try the GUI first; if that doesn't work, try the simple
        # interactive shell.
        if TKINTER:
            try:
                DownloaderGUI(self).mainloop()
            except TclError:
                DownloaderShell(self).run()
        else:
            DownloaderShell(self).run()


class DownloaderShell:
    def __init__(self, dataserver):
        self._ds = dataserver

    def _simple_interactive_menu(self, *options):
        print("-" * 75)
        spc = (68 - sum(len(o) for o in options)) // (len(options) - 1) * " "
        print("    " + spc.join(options))
        print("-" * 75)

    def run(self):
        print("NLTK Downloader")
        while True:
            self._simple_interactive_menu(
                "d) Download",
                "l) List",
                " u) Update",
                "c) Config",
                "h) Help",
                "q) Quit",
            )
            user_input = input("Downloader> ").strip()
            if not user_input:
                print()
                continue
            command = user_input.lower().split()[0]
            args = user_input.split()[1:]
            try:
                if command == "l":
                    print()
                    self._ds.list(self._ds.download_dir, header=False, more_prompt=True)
                elif command == "h":
                    self._simple_interactive_help()
                elif command == "c":
                    self._simple_interactive_config()
                elif command in ("q", "x"):
                    return
                elif command == "d":
                    self._simple_interactive_download(args)
                elif command == "u":
                    self._simple_interactive_update()
                else:
                    print("Command %r unrecognized" % user_input)
            except HTTPError as e:
                print("Error reading from server: %s" % e)
            except URLError as e:
                print("Error connecting to server: %s" % e.reason)
            # try checking if user_input is a package name, &
            # downloading it?
            print()

    def _simple_interactive_download(self, args):
        if args:
            for arg in args:
                try:
                    self._ds.download(arg, prefix="    ")
                except (OSError, ValueError) as e:
                    print(e)
        else:
            while True:
                print()
                print("Download which package (l=list; x=cancel)?")
                user_input = input("  Identifier> ")
                if user_input.lower() == "l":
                    self._ds.list(
                        self._ds.download_dir,
                        header=False,
                        more_prompt=True,
                        skip_installed=True,
                    )
                    continue
                elif user_input.lower() in ("x", "q", ""):
                    return
                elif user_input:
                    for id in user_input.split():
                        try:
                            self._ds.download(id, prefix="    ")
                        except (OSError, ValueError) as e:
                            print(e)
                    break

    def _simple_interactive_update(self):
        while True:
            stale_packages = []
            stale = partial = False
            for info in sorted(getattr(self._ds, "packages")(), key=str):
                if self._ds.status(info) == self._ds.STALE:
                    stale_packages.append((info.id, info.name))

            print()
            if stale_packages:
                print("Will update following packages (o=ok; x=cancel)")
                for pid, pname in stale_packages:
                    name = textwrap.fill(
                        "-" * 27 + (pname), 75, subsequent_indent=27 * " "
                    )[27:]
                    print("  [ ] {} {}".format(pid.ljust(20, "."), name))
                print()

                user_input = input("  Identifier> ")
                if user_input.lower() == "o":
                    for pid, pname in stale_packages:
                        try:
                            self._ds.download(pid, prefix="    ")
                        except (OSError, ValueError) as e:
                            print(e)
                    break
                elif user_input.lower() in ("x", "q", ""):
                    return
            else:
                print("Nothing to update.")
                return

    def _simple_interactive_help(self):
        print()
        print("Commands:")
        print(
            "  d) Download a package or collection     u) Update out of date packages"
        )
        print("  l) List packages & collections          h) Help")
        print("  c) View & Modify Configuration          q) Quit")

    def _show_config(self):
        print()
        print("Data Server:")
        print("  - URL: <%s>" % self._ds.url)
        print("  - %d Package Collections Available" % len(self._ds.collections()))
        print("  - %d Individual Packages Available" % len(self._ds.packages()))
        print()
        print("Local Machine:")
        print("  - Data directory: %s" % self._ds.download_dir)

    def _simple_interactive_config(self):
        self._show_config()
        while True:
            print()
            self._simple_interactive_menu(
                "s) Show Config", "u) Set Server URL", "d) Set Data Dir", "m) Main Menu"
            )
            user_input = input("Config> ").strip().lower()
            if user_input == "s":
                self._show_config()
            elif user_input == "d":
                new_dl_dir = input("  New Directory> ").strip()
                if new_dl_dir in ("", "x", "q", "X", "Q"):
                    print("  Cancelled!")
                elif os.path.isdir(new_dl_dir):
                    self._ds.download_dir = new_dl_dir
                else:
                    print("Directory %r not found!  Create it first." % new_dl_dir)
            elif user_input == "u":
                new_url = input("  New URL> ").strip()
                if new_url in ("", "x", "q", "X", "Q"):
                    print("  Cancelled!")
                else:
                    if not new_url.startswith(("http://", "https://")):
                        new_url = "http://" + new_url
                    try:
                        self._ds.url = new_url
                    except Exception as e:
                        print(f"Error reading <{new_url!r}>:\n  {e}")
            elif user_input == "m":
                break


class DownloaderGUI:
    """
    Graphical interface for downloading packages from the NLTK data
    server.
    """

    # /////////////////////////////////////////////////////////////////
    # Column Configuration
    # /////////////////////////////////////////////////////////////////

    COLUMNS = [
        "",
        "Identifier",
        "Name",
        "Size",
        "Status",
        "Unzipped Size",
        "Copyright",
        "Contact",
        "License",
        "Author",
        "Subdir",
        "Checksum",
    ]
    """A list of the names of columns.  This controls the order in
       which the columns will appear.  If this is edited, then
       ``_package_to_columns()`` may need to be edited to match."""

    COLUMN_WEIGHTS = {"": 0, "Name": 5, "Size": 0, "Status": 0}
    """A dictionary specifying how columns should be resized when the
       table is resized.  Columns with weight 0 will not be resized at
       all; and columns with high weight will be resized more.
       Default weight (for columns not explicitly listed) is 1."""

    COLUMN_WIDTHS = {
        "": 1,
        "Identifier": 20,
        "Name": 45,
        "Size": 10,
        "Unzipped Size": 10,
        "Status": 12,
    }
    """A dictionary specifying how wide each column should be, in
       characters.  The default width (for columns not explicitly
       listed) is specified by ``DEFAULT_COLUMN_WIDTH``."""

    DEFAULT_COLUMN_WIDTH = 30
    """The default width for columns that are not explicitly listed
       in ``COLUMN_WIDTHS``."""

    INITIAL_COLUMNS = ["", "Identifier", "Name", "Size", "Status"]
    """The set of columns that should be displayed by default."""

    # Perform a few import-time sanity checks to make sure that the
    # column configuration variables are defined consistently:
    for c in COLUMN_WEIGHTS:
        assert c in COLUMNS
    for c in COLUMN_WIDTHS:
        assert c in COLUMNS
    for c in INITIAL_COLUMNS:
        assert c in COLUMNS

    # /////////////////////////////////////////////////////////////////
    # Color Configuration
    # /////////////////////////////////////////////////////////////////

    _BACKDROP_COLOR = ("#000", "#ccc")

    _ROW_COLOR = {
        Downloader.INSTALLED: ("#afa", "#080"),
        Downloader.PARTIAL: ("#ffa", "#880"),
        Downloader.STALE: ("#faa", "#800"),
        Downloader.NOT_INSTALLED: ("#fff", "#888"),
    }

    _MARK_COLOR = ("#000", "#ccc")

    # _FRONT_TAB_COLOR = ('#ccf', '#008')
    # _BACK_TAB_COLOR = ('#88a', '#448')
    _FRONT_TAB_COLOR = ("#fff", "#45c")
    _BACK_TAB_COLOR = ("#aaa", "#67a")

    _PROGRESS_COLOR = ("#f00", "#aaa")

    _TAB_FONT = "helvetica -16 bold"

    # /////////////////////////////////////////////////////////////////
    # Constructor
    # /////////////////////////////////////////////////////////////////

    def __init__(self, dataserver, use_threads=True):
        self._ds = dataserver
        self._use_threads = use_threads

        # For the threaded downloader:
        self._download_lock = threading.Lock()
        self._download_msg_queue = []
        self._download_abort_queue = []
        self._downloading = False

        # For tkinter after callbacks:
        self._afterid = {}

        # A message log.
        self._log_messages = []
        self._log_indent = 0
        self._log("NLTK Downloader Started!")

        # Create the main window.
        top = self.top = Tk()
        top.geometry("+50+50")
        top.title("NLTK Downloader")
        top.configure(background=self._BACKDROP_COLOR[1])

        # Set up some bindings now, in case anything goes wrong.
        top.bind("<Control-q>", self.destroy)
        top.bind("<Control-x>", self.destroy)
        self._destroyed = False

        self._column_vars = {}

        # Initialize the GUI.
        self._init_widgets()
        self._init_menu()
        try:
            self._fill_table()
        except HTTPError as e:
            showerror("Error reading from server", e)
        except URLError as e:
            showerror("Error connecting to server", e.reason)

        self._show_info()
        self._select_columns()
        self._table.select(0)

        # Make sure we get notified when we're destroyed, so we can
        # cancel any download in progress.
        self._table.bind("<Destroy>", self._destroy)

    def _log(self, msg):
        self._log_messages.append(
            "{} {}{}".format(time.ctime(), " | " * self._log_indent, msg)
        )

    # /////////////////////////////////////////////////////////////////
    # Internals
    # /////////////////////////////////////////////////////////////////

    def _init_widgets(self):
        # Create the top-level frame structures
        f1 = Frame(self.top, relief="raised", border=2, padx=8, pady=0)
        f1.pack(sid="top", expand=True, fill="both")
        f1.grid_rowconfigure(2, weight=1)
        f1.grid_columnconfigure(0, weight=1)
        Frame(f1, height=8).grid(column=0, row=0)  # spacer
        tabframe = Frame(f1)
        tabframe.grid(column=0, row=1, sticky="news")
        tableframe = Frame(f1)
        tableframe.grid(column=0, row=2, sticky="news")
        buttonframe = Frame(f1)
        buttonframe.grid(column=0, row=3, sticky="news")
        Frame(f1, height=8).grid(column=0, row=4)  # spacer
        infoframe = Frame(f1)
        infoframe.grid(column=0, row=5, sticky="news")
        Frame(f1, height=8).grid(column=0, row=6)  # spacer
        progressframe = Frame(
            self.top, padx=3, pady=3, background=self._BACKDROP_COLOR[1]
        )
        progressframe.pack(side="bottom", fill="x")
        self.top["border"] = 0
        self.top["highlightthickness"] = 0

        # Create the tabs
        self._tab_names = ["Collections", "Corpora", "Models", "All Packages"]
        self._tabs = {}
        for i, tab in enumerate(self._tab_names):
            label = Label(tabframe, text=tab, font=self._TAB_FONT)
            label.pack(side="left", padx=((i + 1) % 2) * 10)
            label.bind("<Button-1>", self._select_tab)
            self._tabs[tab.lower()] = label

        # Create the table.
        column_weights = [self.COLUMN_WEIGHTS.get(column, 1) for column in self.COLUMNS]
        self._table = Table(
            tableframe,
            self.COLUMNS,
            column_weights=column_weights,
            highlightthickness=0,
            listbox_height=16,
            reprfunc=self._table_reprfunc,
        )
        self._table.columnconfig(0, foreground=self._MARK_COLOR[0])  # marked
        for i, column in enumerate(self.COLUMNS):
            width = self.COLUMN_WIDTHS.get(column, self.DEFAULT_COLUMN_WIDTH)
            self._table.columnconfig(i, width=width)
        self._table.pack(expand=True, fill="both")
        self._table.focus()
        self._table.bind_to_listboxes("<Double-Button-1>", self._download)
        self._table.bind("<space>", self._table_mark)
        self._table.bind("<Return>", self._download)
        self._table.bind("<Left>", self._prev_tab)
        self._table.bind("<Right>", self._next_tab)
        self._table.bind("<Control-a>", self._mark_all)

        # Create entry boxes for URL & download_dir
        infoframe.grid_columnconfigure(1, weight=1)

        info = [
            ("url", "Server Index:", self._set_url),
            ("download_dir", "Download Directory:", self._set_download_dir),
        ]
        self._info = {}
        for (i, (key, label, callback)) in enumerate(info):
            Label(infoframe, text=label).grid(column=0, row=i, sticky="e")
            entry = Entry(
                infoframe,
                font="courier",
                relief="groove",
                disabledforeground="#007aff",
                foreground="#007aff",
            )
            self._info[key] = (entry, callback)
            entry.bind("<Return>", self._info_save)
            entry.bind("<Button-1>", lambda e, key=key: self._info_edit(key))
            entry.grid(column=1, row=i, sticky="ew")

        # If the user edits url or download_dir, and then clicks outside
        # the entry box, then save their results.
        self.top.bind("<Button-1>", self._info_save)

        # Create Download & Refresh buttons.
        self._download_button = Button(
            buttonframe, text="Download", command=self._download, width=8
        )
        self._download_button.pack(side="left")
        self._refresh_button = Button(
            buttonframe, text="Refresh", command=self._refresh, width=8
        )
        self._refresh_button.pack(side="right")

        # Create Progress bar
        self._progresslabel = Label(
            progressframe,
            text="",
            foreground=self._BACKDROP_COLOR[0],
            background=self._BACKDROP_COLOR[1],
        )
        self._progressbar = Canvas(
            progressframe,
            width=200,
            height=16,
            background=self._PROGRESS_COLOR[1],
            relief="sunken",
            border=1,
        )
        self._init_progressbar()
        self._progressbar.pack(side="right")
        self._progresslabel.pack(side="left")

    def _init_menu(self):
        menubar = Menu(self.top)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Download", underline=0, command=self._download, accelerator="Return"
        )
        filemenu.add_separator()
        filemenu.add_command(
            label="Change Server Index",
            underline=7,
            command=lambda: self._info_edit("url"),
        )
        filemenu.add_command(
            label="Change Download Directory",
            underline=0,
            command=lambda: self._info_edit("download_dir"),
        )
        filemenu.add_separator()
        filemenu.add_command(label="Show Log", underline=5, command=self._show_log)
        filemenu.add_separator()
        filemenu.add_command(
            label="Exit", underline=1, command=self.destroy, accelerator="Ctrl-x"
        )
        menubar.add_cascade(label="File", underline=0, menu=filemenu)

        # Create a menu to control which columns of the table are
        # shown.  n.b.: we never hide the first two columns (mark and
        # identifier).
        viewmenu = Menu(menubar, tearoff=0)
        for column in self._table.column_names[2:]:
            var = IntVar(self.top)
            assert column not in self._column_vars
            self._column_vars[column] = var
            if column in self.INITIAL_COLUMNS:
                var.set(1)
            viewmenu.add_checkbutton(
                label=column, underline=0, variable=var, command=self._select_columns
            )
        menubar.add_cascade(label="View", underline=0, menu=viewmenu)

        # Create a sort menu
        # [xx] this should be selectbuttons; and it should include
        # reversed sorts as options.
        sortmenu = Menu(menubar, tearoff=0)
        for column in self._table.column_names[1:]:
            sortmenu.add_command(
                label="Sort by %s" % column,
                command=(lambda c=column: self._table.sort_by(c, "ascending")),
            )
        sortmenu.add_separator()
        # sortmenu.add_command(label='Descending Sort:')
        for column in self._table.column_names[1:]:
            sortmenu.add_command(
                label="Reverse sort by %s" % column,
                command=(lambda c=column: self._table.sort_by(c, "descending")),
            )
        menubar.add_cascade(label="Sort", underline=0, menu=sortmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", underline=0, command=self.about)
        helpmenu.add_command(
            label="Instructions", underline=0, command=self.help, accelerator="F1"
        )
        menubar.add_cascade(label="Help", underline=0, menu=helpmenu)
        self.top.bind("<F1>", self.help)

        self.top.config(menu=menubar)

    def _select_columns(self):
        for (column, var) in self._column_vars.items():
            if var.get():
                self._table.show_column(column)
            else:
                self._table.hide_column(column)

    def _refresh(self):
        self._ds.clear_status_cache()
        try:
            self._fill_table()
        except HTTPError as e:
            showerror("Error reading from server", e)
        except URLError as e:
            showerror("Error connecting to server", e.reason)
        self._table.select(0)

    def _info_edit(self, info_key):
        self._info_save()  # just in case.
        (entry, callback) = self._info[info_key]
        entry["state"] = "normal"
        entry["relief"] = "sunken"
        entry.focus()

    def _info_save(self, e=None):
        focus = self._table
        for entry, callback in self._info.values():
            if entry["state"] == "disabled":
                continue
            if e is not None and e.widget is entry and e.keysym != "Return":
                focus = entry
            else:
                entry["state"] = "disabled"
                entry["relief"] = "groove"
                callback(entry.get())
        focus.focus()

    def _table_reprfunc(self, row, col, val):
        if self._table.column_names[col].endswith("Size"):
            if isinstance(val, str):
                return "  %s" % val
            elif val < 1024**2:
                return "  %.1f KB" % (val / 1024.0**1)
            elif val < 1024**3:
                return "  %.1f MB" % (val / 1024.0**2)
            else:
                return "  %.1f GB" % (val / 1024.0**3)

        if col in (0, ""):
            return str(val)
        else:
            return "  %s" % val

    def _set_url(self, url):
        if url == self._ds.url:
            return
        try:
            self._ds.url = url
            self._fill_table()
        except OSError as e:
            showerror("Error Setting Server Index", str(e))
        self._show_info()

    def _set_download_dir(self, download_dir):
        if self._ds.download_dir == download_dir:
            return
        # check if the dir exists, and if not, ask if we should create it?

        # Clear our status cache, & re-check what's installed
        self._ds.download_dir = download_dir
        try:
            self._fill_table()
        except HTTPError as e:
            showerror("Error reading from server", e)
        except URLError as e:
            showerror("Error connecting to server", e.reason)
        self._show_info()

    def _show_info(self):
        print("showing info", self._ds.url)
        for entry, cb in self._info.values():
            entry["state"] = "normal"
            entry.delete(0, "end")
        self._info["url"][0].insert(0, self._ds.url)
        self._info["download_dir"][0].insert(0, self._ds.download_dir)
        for entry, cb in self._info.values():
            entry["state"] = "disabled"

    def _prev_tab(self, *e):
        for i, tab in enumerate(self._tab_names):
            if tab.lower() == self._tab and i > 0:
                self._tab = self._tab_names[i - 1].lower()
                try:
                    return self._fill_table()
                except HTTPError as e:
                    showerror("Error reading from server", e)
                except URLError as e:
                    showerror("Error connecting to server", e.reason)

    def _next_tab(self, *e):
        for i, tab in enumerate(self._tab_names):
            if tab.lower() == self._tab and i < (len(self._tabs) - 1):
                self._tab = self._tab_names[i + 1].lower()
                try:
                    return self._fill_table()
                except HTTPError as e:
                    showerror("Error reading from server", e)
                except URLError as e:
                    showerror("Error connecting to server", e.reason)

    def _select_tab(self, event):
        self._tab = event.widget["text"].lower()
        try:
            self._fill_table()
        except HTTPError as e:
            showerror("Error reading from server", e)
        except URLError as e:
            showerror("Error connecting to server", e.reason)

    _tab = "collections"
    # _tab = 'corpora'
    _rows = None

    def _fill_table(self):
        selected_row = self._table.selected_row()
        self._table.clear()
        if self._tab == "all packages":
            items = self._ds.packages()
        elif self._tab == "corpora":
            items = self._ds.corpora()
        elif self._tab == "models":
            items = self._ds.models()
        elif self._tab == "collections":
            items = self._ds.collections()
        else:
            assert 0, "bad tab value %r" % self._tab
        rows = [self._package_to_columns(item) for item in items]
        self._table.extend(rows)

        # Highlight the active tab.
        for tab, label in self._tabs.items():
            if tab == self._tab:
                label.configure(
                    foreground=self._FRONT_TAB_COLOR[0],
                    background=self._FRONT_TAB_COLOR[1],
                )
            else:
                label.configure(
                    foreground=self._BACK_TAB_COLOR[0],
                    background=self._BACK_TAB_COLOR[1],
                )

        self._table.sort_by("Identifier", order="ascending")
        self._color_table()
        self._table.select(selected_row)

        # This is a hack, because the scrollbar isn't updating its
        # position right -- I'm not sure what the underlying cause is
        # though.  (This is on OS X w/ python 2.5)  The length of
        # delay that's necessary seems to depend on how fast the
        # comptuer is. :-/
        self.top.after(150, self._table._scrollbar.set, *self._table._mlb.yview())
        self.top.after(300, self._table._scrollbar.set, *self._table._mlb.yview())

    def _update_table_status(self):
        for row_num in range(len(self._table)):
            status = self._ds.status(self._table[row_num, "Identifier"])
            self._table[row_num, "Status"] = status
        self._color_table()

    def _download(self, *e):
        # If we're using threads, then delegate to the threaded
        # downloader instead.
        if self._use_threads:
            return self._download_threaded(*e)

        marked = [
            self._table[row, "Identifier"]
            for row in range(len(self._table))
            if self._table[row, 0] != ""
        ]
        selection = self._table.selected_row()
        if not marked and selection is not None:
            marked = [self._table[selection, "Identifier"]]

        download_iter = self._ds.incr_download(marked, self._ds.download_dir)
        self._log_indent = 0
        self._download_cb(download_iter, marked)

    _DL_DELAY = 10

    def _download_cb(self, download_iter, ids):
        try:
            msg = next(download_iter)
        except StopIteration:
            # self._fill_table(sort=False)
            self._update_table_status()
            afterid = self.top.after(10, self._show_progress, 0)
            self._afterid["_download_cb"] = afterid
            return

        def show(s):
            self._progresslabel["text"] = s
            self._log(s)

        if isinstance(msg, ProgressMessage):
            self._show_progress(msg.progress)
        elif isinstance(msg, ErrorMessage):
            show(msg.message)
            if msg.package is not None:
                self._select(msg.package.id)
            self._show_progress(None)
            return  # halt progress.
        elif isinstance(msg, StartCollectionMessage):
            show("Downloading collection %s" % msg.collection.id)
            self._log_indent += 1
        elif isinstance(msg, StartPackageMessage):
            show("Downloading package %s" % msg.package.id)
        elif isinstance(msg, UpToDateMessage):
            show("Package %s is up-to-date!" % msg.package.id)
        # elif isinstance(msg, StaleMessage):
        #    show('Package %s is out-of-date or corrupt' % msg.package.id)
        elif isinstance(msg, FinishDownloadMessage):
            show("Finished downloading %r." % msg.package.id)
        elif isinstance(msg, StartUnzipMessage):
            show("Unzipping %s" % msg.package.filename)
        elif isinstance(msg, FinishCollectionMessage):
            self._log_indent -= 1
            show("Finished downloading collection %r." % msg.collection.id)
            self._clear_mark(msg.collection.id)
        elif isinstance(msg, FinishPackageMessage):
            self._clear_mark(msg.package.id)
        afterid = self.top.after(self._DL_DELAY, self._download_cb, download_iter, ids)
        self._afterid["_download_cb"] = afterid

    def _select(self, id):
        for row in range(len(self._table)):
            if self._table[row, "Identifier"] == id:
                self._table.select(row)
                return

    def _color_table(self):
        # Color rows according to status.
        for row in range(len(self._table)):
            bg, sbg = self._ROW_COLOR[self._table[row, "Status"]]
            fg, sfg = ("black", "white")
            self._table.rowconfig(
                row,
                foreground=fg,
                selectforeground=sfg,
                background=bg,
                selectbackground=sbg,
            )
            # Color the marked column
            self._table.itemconfigure(
                row, 0, foreground=self._MARK_COLOR[0], background=self._MARK_COLOR[1]
            )

    def _clear_mark(self, id):
        for row in range(len(self._table)):
            if self._table[row, "Identifier"] == id:
                self._table[row, 0] = ""

    def _mark_all(self, *e):
        for row in range(len(self._table)):
            self._table[row, 0] = "X"

    def _table_mark(self, *e):
        selection = self._table.selected_row()
        if selection >= 0:
            if self._table[selection][0] != "":
                self._table[selection, 0] = ""
            else:
                self._table[selection, 0] = "X"
        self._table.select(delta=1)

    def _show_log(self):
        text = "\n".join(self._log_messages)
        ShowText(self.top, "NLTK Downloader Log", text)

    def _package_to_columns(self, pkg):
        """
        Given a package, return a list of values describing that
        package, one for each column in ``self.COLUMNS``.
        """
        row = []
        for column_index, column_name in enumerate(self.COLUMNS):
            if column_index == 0:  # Mark:
                row.append("")
            elif column_name == "Identifier":
                row.append(pkg.id)
            elif column_name == "Status":
                row.append(self._ds.status(pkg))
            else:
                attr = column_name.lower().replace(" ", "_")
                row.append(getattr(pkg, attr, "n/a"))
        return row

    # /////////////////////////////////////////////////////////////////
    # External Interface
    # /////////////////////////////////////////////////////////////////

    def destroy(self, *e):
        if self._destroyed:
            return
        self.top.destroy()
        self._destroyed = True

    def _destroy(self, *e):
        if self.top is not None:
            for afterid in self._afterid.values():
                self.top.after_cancel(afterid)

        # Abort any download in progress.
        if self._downloading and self._use_threads:
            self._abort_download()

        # Make sure the garbage collector destroys these now;
        # otherwise, they may get destroyed when we're not in the main
        # thread, which would make Tkinter unhappy.
        self._column_vars.clear()

    def mainloop(self, *args, **kwargs):
        self.top.mainloop(*args, **kwargs)

    # /////////////////////////////////////////////////////////////////
    # HELP
    # /////////////////////////////////////////////////////////////////

    HELP = textwrap.dedent(
        """\
    This tool can be used to download a variety of corpora and models
    that can be used with NLTK.  Each corpus or model is distributed
    in a single zip file, known as a \"package file.\"  You can
    download packages individually, or you can download pre-defined
    collections of packages.

    When you download a package, it will be saved to the \"download
    directory.\"  A default download directory is chosen when you run

    the downloader; but you may also select a different download
    directory.  On Windows, the default download directory is


    \"package.\"

    The NLTK downloader can be used to download a variety of corpora,
    models, and other data packages.

    Keyboard shortcuts::
      [return]\t Download
      [up]\t Select previous package
      [down]\t Select next package
      [left]\t Select previous tab
      [right]\t Select next tab
    """
    )

    def help(self, *e):
        # The default font's not very legible; try using 'fixed' instead.
        try:
            ShowText(
                self.top,
                "Help: NLTK Downloader",
                self.HELP.strip(),
                width=75,
                font="fixed",
            )
        except:
            ShowText(self.top, "Help: NLTK Downloader", self.HELP.strip(), width=75)

    def about(self, *e):
        ABOUT = "NLTK Downloader\n" + "Written by Edward Loper"
        TITLE = "About: NLTK Downloader"
        try:
            from tkinter.messagebox import Message

            Message(message=ABOUT, title=TITLE).show()
        except ImportError:
            ShowText(self.top, TITLE, ABOUT)

    # /////////////////////////////////////////////////////////////////
    # Progress Bar
    # /////////////////////////////////////////////////////////////////

    _gradient_width = 5

    def _init_progressbar(self):
        c = self._progressbar
        width, height = int(c["width"]), int(c["height"])
        for i in range(0, (int(c["width"]) * 2) // self._gradient_width):
            c.create_line(
                i * self._gradient_width + 20,
                -20,
                i * self._gradient_width - height - 20,
                height + 20,
                width=self._gradient_width,
                fill="#%02x0000" % (80 + abs(i % 6 - 3) * 12),
            )
        c.addtag_all("gradient")
        c.itemconfig("gradient", state="hidden")

        # This is used to display progress
        c.addtag_withtag(
            "redbox", c.create_rectangle(0, 0, 0, 0, fill=self._PROGRESS_COLOR[0])
        )

    def _show_progress(self, percent):
        c = self._progressbar
        if percent is None:
            c.coords("redbox", 0, 0, 0, 0)
            c.itemconfig("gradient", state="hidden")
        else:
            width, height = int(c["width"]), int(c["height"])
            x = percent * int(width) // 100 + 1
            c.coords("redbox", 0, 0, x, height + 1)

    def _progress_alive(self):
        c = self._progressbar
        if not self._downloading:
            c.itemconfig("gradient", state="hidden")
        else:
            c.itemconfig("gradient", state="normal")
            x1, y1, x2, y2 = c.bbox("gradient")
            if x1 <= -100:
                c.move("gradient", (self._gradient_width * 6) - 4, 0)
            else:
                c.move("gradient", -4, 0)
            afterid = self.top.after(200, self._progress_alive)
            self._afterid["_progress_alive"] = afterid

    # /////////////////////////////////////////////////////////////////
    # Threaded downloader
    # /////////////////////////////////////////////////////////////////

    def _download_threaded(self, *e):
        # If the user tries to start a new download while we're already
        # downloading something, then abort the current download instead.
        if self._downloading:
            self._abort_download()
            return

        # Change the 'download' button to an 'abort' button.
        self._download_button["text"] = "Cancel"

        marked = [
            self._table[row, "Identifier"]
            for row in range(len(self._table))
            if self._table[row, 0] != ""
        ]
        selection = self._table.selected_row()
        if not marked and selection is not None:
            marked = [self._table[selection, "Identifier"]]

        # Create a new data server object for the download operation,
        # just in case the user modifies our data server during the
        # download (e.g., clicking 'refresh' or editing the index url).
        ds = Downloader(self._ds.url, self._ds.download_dir)

        # Start downloading in a separate thread.
        assert self._download_msg_queue == []
        assert self._download_abort_queue == []
        self._DownloadThread(
            ds,
            marked,
            self._download_lock,
            self._download_msg_queue,
            self._download_abort_queue,
        ).start()

        # Monitor the download message queue & display its progress.
        self._log_indent = 0
        self._downloading = True
        self._monitor_message_queue()

        # Display an indication that we're still alive and well by
        # cycling the progress bar.
        self._progress_alive()

    def _abort_download(self):
        if self._downloading:
            self._download_lock.acquire()
            self._download_abort_queue.append("abort")
            self._download_lock.release()

    class _DownloadThread(threading.Thread):
        def __init__(self, data_server, items, lock, message_queue, abort):
            self.data_server = data_server
            self.items = items
            self.lock = lock
            self.message_queue = message_queue
            self.abort = abort
            threading.Thread.__init__(self)

        def run(self):
            for msg in self.data_server.incr_download(self.items):
                self.lock.acquire()
                self.message_queue.append(msg)
                # Check if we've been told to kill ourselves:
                if self.abort:
                    self.message_queue.append("aborted")
                    self.lock.release()
                    return
                self.lock.release()
            self.lock.acquire()
            self.message_queue.append("finished")
            self.lock.release()

    _MONITOR_QUEUE_DELAY = 100

    def _monitor_message_queue(self):
        def show(s):
            self._progresslabel["text"] = s
            self._log(s)

        # Try to acquire the lock; if it's busy, then just try again later.
        if not self._download_lock.acquire():
            return
        for msg in self._download_msg_queue:

            # Done downloading?
            if msg == "finished" or msg == "aborted":
                # self._fill_table(sort=False)
                self._update_table_status()
                self._downloading = False
                self._download_button["text"] = "Download"
                del self._download_msg_queue[:]
                del self._download_abort_queue[:]
                self._download_lock.release()
                if msg == "aborted":
                    show("Download aborted!")
                    self._show_progress(None)
                else:
                    afterid = self.top.after(100, self._show_progress, None)
                    self._afterid["_monitor_message_queue"] = afterid
                return

            # All other messages
            elif isinstance(msg, ProgressMessage):
                self._show_progress(msg.progress)
            elif isinstance(msg, ErrorMessage):
                show(msg.message)
                if msg.package is not None:
                    self._select(msg.package.id)
                self._show_progress(None)
                self._downloading = False
                return  # halt progress.
            elif isinstance(msg, StartCollectionMessage):
                show("Downloading collection %r" % msg.collection.id)
                self._log_indent += 1
            elif isinstance(msg, StartPackageMessage):
                self._ds.clear_status_cache(msg.package.id)
                show("Downloading package %r" % msg.package.id)
            elif isinstance(msg, UpToDateMessage):
                show("Package %s is up-to-date!" % msg.package.id)
            # elif isinstance(msg, StaleMessage):
            #    show('Package %s is out-of-date or corrupt; updating it' %
            #         msg.package.id)
            elif isinstance(msg, FinishDownloadMessage):
                show("Finished downloading %r." % msg.package.id)
            elif isinstance(msg, StartUnzipMessage):
                show("Unzipping %s" % msg.package.filename)
            elif isinstance(msg, FinishUnzipMessage):
                show("Finished installing %s" % msg.package.id)
            elif isinstance(msg, FinishCollectionMessage):
                self._log_indent -= 1
                show("Finished downloading collection %r." % msg.collection.id)
                self._clear_mark(msg.collection.id)
            elif isinstance(msg, FinishPackageMessage):
                self._update_table_status()
                self._clear_mark(msg.package.id)

        # Let the user know when we're aborting a download (but
        # waiting for a good point to abort it, so we don't end up
        # with a partially unzipped package or anything like that).
        if self._download_abort_queue:
            self._progresslabel["text"] = "Aborting download..."

        # Clear the message queue and then release the lock
        del self._download_msg_queue[:]
        self._download_lock.release()

        # Check the queue again after MONITOR_QUEUE_DELAY msec.
        afterid = self.top.after(self._MONITOR_QUEUE_DELAY, self._monitor_message_queue)
        self._afterid["_monitor_message_queue"] = afterid


######################################################################
# Helper Functions
######################################################################
# [xx] It may make sense to move these to nltk.internals.


def md5_hexdigest(file):
    """
    Calculate and return the MD5 checksum for a given file.
    ``file`` may either be a filename or an open stream.
    """
    if isinstance(file, str):
        with open(file, "rb") as infile:
            return _md5_hexdigest(infile)
    return _md5_hexdigest(file)


def _md5_hexdigest(fp):
    md5_digest = md5()
    while True:
        block = fp.read(1024 * 16)  # 16k blocks
        if not block:
            break
        md5_digest.update(block)
    return md5_digest.hexdigest()


# change this to periodically yield progress messages?
# [xx] get rid of topdir parameter -- we should be checking
# this when we build the index, anyway.
def unzip(filename, root, verbose=True):
    """
    Extract the contents of the zip file ``filename`` into the
    directory ``root``.
    """
    for message in _unzip_iter(filename, root, verbose):
        if isinstance(message, ErrorMessage):
            raise Exception(message)


def _unzip_iter(filename, root, verbose=True):
    if verbose:
        sys.stdout.write("Unzipping %s" % os.path.split(filename)[1])
        sys.stdout.flush()

    try:
        zf = zipfile.ZipFile(filename)
    except zipfile.error as e:
        yield ErrorMessage(filename, "Error with downloaded zip file")
        return
    except Exception as e:
        yield ErrorMessage(filename, e)
        return

    zf.extractall(root)

    if verbose:
        print()


######################################################################
# Index Builder
######################################################################
# This may move to a different file sometime.


def build_index(root, base_url):
    """
    Create a new data.xml index file, by combining the xml description
    files for various packages and collections.  ``root`` should be the
    path to a directory containing the package xml and zip files; and
    the collection xml files.  The ``root`` directory is expected to
    have the following subdirectories::

      root/
        packages/ .................. subdirectory for packages
          corpora/ ................. zip & xml files for corpora
          grammars/ ................ zip & xml files for grammars
          taggers/ ................. zip & xml files for taggers
          tokenizers/ .............. zip & xml files for tokenizers
          etc.
        collections/ ............... xml files for collections

    For each package, there should be two files: ``package.zip``
    (where *package* is the package name)
    which contains the package itself as a compressed zip file; and
    ``package.xml``, which is an xml description of the package.  The
    zipfile ``package.zip`` should expand to a single subdirectory
    named ``package/``.  The base filename ``package`` must match
    the identifier given in the package's xml file.

    For each collection, there should be a single file ``collection.zip``
    describing the collection, where *collection* is the name of the collection.

    All identifiers (for both packages and collections) must be unique.
    """
    # Find all packages.
    packages = []
    for pkg_xml, zf, subdir in _find_packages(os.path.join(root, "packages")):
        zipstat = os.stat(zf.filename)
        url = f"{base_url}/{subdir}/{os.path.split(zf.filename)[1]}"
        unzipped_size = sum(zf_info.file_size for zf_info in zf.infolist())

        # Fill in several fields of the package xml with calculated values.
        pkg_xml.set("unzipped_size", "%s" % unzipped_size)
        pkg_xml.set("size", "%s" % zipstat.st_size)
        pkg_xml.set("checksum", "%s" % md5_hexdigest(zf.filename))
        pkg_xml.set("subdir", subdir)
        # pkg_xml.set('svn_revision', _svn_revision(zf.filename))
        if not pkg_xml.get("url"):
            pkg_xml.set("url", url)

        # Record the package.
        packages.append(pkg_xml)

    # Find all collections
    collections = list(_find_collections(os.path.join(root, "collections")))

    # Check that all UIDs are unique
    uids = set()
    for item in packages + collections:
        if item.get("id") in uids:
            raise ValueError("Duplicate UID: %s" % item.get("id"))
        uids.add(item.get("id"))

    # Put it all together
    top_elt = ElementTree.Element("nltk_data")
    top_elt.append(ElementTree.Element("packages"))
    top_elt[0].extend(sorted(packages, key=lambda package: package.get("id")))
    top_elt.append(ElementTree.Element("collections"))
    top_elt[1].extend(sorted(collections, key=lambda collection: collection.get("id")))

    _indent_xml(top_elt)
    return top_elt


def _indent_xml(xml, prefix=""):
    """
    Helper for ``build_index()``: Given an XML ``ElementTree``, modify it
    (and its descendents) ``text`` and ``tail`` attributes to generate
    an indented tree, where each nested element is indented by 2
    spaces with respect to its parent.
    """
    if len(xml) > 0:
        xml.text = (xml.text or "").strip() + "\n" + prefix + "  "
        for child in xml:
            _indent_xml(child, prefix + "  ")
        for child in xml[:-1]:
            child.tail = (child.tail or "").strip() + "\n" + prefix + "  "
        xml[-1].tail = (xml[-1].tail or "").strip() + "\n" + prefix


def _check_package(pkg_xml, zipfilename, zf):
    """
    Helper for ``build_index()``: Perform some checks to make sure that
    the given package is consistent.
    """
    # The filename must patch the id given in the XML file.
    uid = os.path.splitext(os.path.split(zipfilename)[1])[0]
    if pkg_xml.get("id") != uid:
        raise ValueError(
            "package identifier mismatch ({} vs {})".format(pkg_xml.get("id"), uid)
        )

    # Zip file must expand to a subdir whose name matches uid.
    if sum((name != uid and not name.startswith(uid + "/")) for name in zf.namelist()):
        raise ValueError(
            "Zipfile %s.zip does not expand to a single "
            "subdirectory %s/" % (uid, uid)
        )


# update for git?
def _svn_revision(filename):
    """
    Helper for ``build_index()``: Calculate the subversion revision
    number for a given file (by using ``subprocess`` to run ``svn``).
    """
    p = subprocess.Popen(
        ["svn", "status", "-v", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate()
    if p.returncode != 0 or stderr or not stdout:
        raise ValueError(
            "Error determining svn_revision for %s: %s"
            % (os.path.split(filename)[1], textwrap.fill(stderr))
        )
    return stdout.split()[2]


def _find_collections(root):
    """
    Helper for ``build_index()``: Yield a list of ElementTree.Element
    objects, each holding the xml for a single package collection.
    """
    for dirname, _subdirs, files in os.walk(root):
        for filename in files:
            if filename.endswith(".xml"):
                xmlfile = os.path.join(dirname, filename)
                yield ElementTree.parse(xmlfile).getroot()


def _find_packages(root):
    """
    Helper for ``build_index()``: Yield a list of tuples
    ``(pkg_xml, zf, subdir)``, where:
      - ``pkg_xml`` is an ``ElementTree.Element`` holding the xml for a
        package
      - ``zf`` is a ``zipfile.ZipFile`` for the package's contents.
      - ``subdir`` is the subdirectory (relative to ``root``) where
        the package was found (e.g. 'corpora' or 'grammars').
    """
    from nltk.corpus.reader.util import _path_from

    # Find all packages.
    packages = []
    for dirname, subdirs, files in os.walk(root):
        relpath = "/".join(_path_from(root, dirname))
        for filename in files:
            if filename.endswith(".xml"):
                xmlfilename = os.path.join(dirname, filename)
                zipfilename = xmlfilename[:-4] + ".zip"
                try:
                    zf = zipfile.ZipFile(zipfilename)
                except Exception as e:
                    raise ValueError(f"Error reading file {zipfilename!r}!\n{e}") from e
                try:
                    pkg_xml = ElementTree.parse(xmlfilename).getroot()
                except Exception as e:
                    raise ValueError(f"Error reading file {xmlfilename!r}!\n{e}") from e

                # Check that the UID matches the filename
                uid = os.path.split(xmlfilename[:-4])[1]
                if pkg_xml.get("id") != uid:
                    raise ValueError(
                        "package identifier mismatch (%s "
                        "vs %s)" % (pkg_xml.get("id"), uid)
                    )

                # Check that the zipfile expands to a subdir whose
                # name matches the uid.
                if sum(
                    (name != uid and not name.startswith(uid + "/"))
                    for name in zf.namelist()
                ):
                    raise ValueError(
                        "Zipfile %s.zip does not expand to a "
                        "single subdirectory %s/" % (uid, uid)
                    )

                yield pkg_xml, zf, relpath

            elif filename.endswith(".zip"):
                # Warn user in case a .xml does not exist for a .zip
                resourcename = os.path.splitext(filename)[0]
                xmlfilename = os.path.join(dirname, resourcename + ".xml")
                if not os.path.exists(xmlfilename):
                    warnings.warn(
                        f"{filename} exists, but {resourcename + '.xml'} cannot be found! "
                        f"This could mean that {resourcename} can not be downloaded.",
                        stacklevel=2,
                    )

        # Don't recurse into svn subdirectories:
        try:
            subdirs.remove(".svn")
        except ValueError:
            pass


######################################################################
# Main:
######################################################################

# There should be a command-line interface

# Aliases
_downloader = Downloader()
download = _downloader.download


def download_shell():
    DownloaderShell(_downloader).run()


def download_gui():
    DownloaderGUI(_downloader).mainloop()


def update():
    _downloader.update()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
        "-d",
        "--dir",
        dest="dir",
        help="download package to directory DIR",
        metavar="DIR",
    )
    parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="work quietly",
    )
    parser.add_option(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        default=False,
        help="download even if already installed",
    )
    parser.add_option(
        "-e",
        "--exit-on-error",
        dest="halt_on_error",
        action="store_true",
        default=False,
        help="exit if an error occurs",
    )
    parser.add_option(
        "-u",
        "--url",
        dest="server_index_url",
        default=os.environ.get("NLTK_DOWNLOAD_URL"),
        help="download server index url",
    )

    (options, args) = parser.parse_args()

    downloader = Downloader(server_index_url=options.server_index_url)

    if args:
        for pkg_id in args:
            rv = downloader.download(
                info_or_id=pkg_id,
                download_dir=options.dir,
                quiet=options.quiet,
                force=options.force,
                halt_on_error=options.halt_on_error,
            )
            if rv == False and options.halt_on_error:
                break
    else:
        downloader.download(
            download_dir=options.dir,
            quiet=options.quiet,
            force=options.force,
            halt_on_error=options.halt_on_error,
        )



# ----------------------------------------------------------------------
# MODULE: check_proxy
# SOURCE: check_proxy.py
# ----------------------------------------------------------------------


def check_proxy(proxies, return_ip=False):
    """
    检查代理配置并返回结果。

    Args:
        proxies (dict): 包含http和https代理配置的字典。
        return_ip (bool, optional): 是否返回代理的IP地址。默认为False。

    Returns:
        str or None: 检查的结果信息或代理的IP地址（如果`return_ip`为True）。
    """
    import requests
    proxies_https = proxies['https'] if proxies is not None else '无'
    ip = None
    try:
        response = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=4)  # ⭐ 执行GET请求以获取代理信息
        data = response.json()
        if 'country_name' in data:
            country = data['country_name']
            result = f"代理配置 {proxies_https}, 代理所在地：{country}"
            if 'ip' in data:
                ip = data['ip']
        elif 'error' in data:
            alternative, ip = _check_with_backup_source(proxies)  # ⭐ 调用备用方法检查代理配置
            if alternative is None:
                result = f"代理配置 {proxies_https}, 代理所在地：未知，IP查询频率受限"
            else:
                result = f"代理配置 {proxies_https}, 代理所在地：{alternative}"
        else:
            result = f"代理配置 {proxies_https}, 代理数据解析失败：{data}"

        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip
    except:
        result = f"代理配置 {proxies_https}, 代理所在地查询超时，代理可能无效"
        if not return_ip:
            logger.warning(result)
            return result
        else:
            return ip

def _check_with_backup_source(proxies):
    """
    通过备份源检查代理，并获取相应信息。

    Args:
        proxies (dict): 包含代理信息的字典。

    Returns:
        tuple: 代理信息(geo)和IP地址(ip)的元组。
    """
    import random, string, requests
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    try:
        res_json = requests.get(f"http://{random_string}.edns.ip-api.com/json", proxies=proxies, timeout=4).json()  # ⭐ 执行代理检查和备份源请求
        return res_json['dns']['geo'], res_json['dns']['ip']
    except:
        return None, None

def backup_and_download(current_version, remote_version):
    """
    一键更新协议：备份当前版本，下载远程版本并解压缩。

    Args:
        current_version (str): 当前版本号。
        remote_version (str): 远程版本号。

    Returns:
        str: 新版本目录的路径。
    """
    from toolbox import get_conf
    import shutil
    import os
    import requests
    import zipfile
    os.makedirs(f'./history', exist_ok=True)
    backup_dir = f'./history/backup-{current_version}/'
    new_version_dir = f'./history/new-version-{remote_version}/'
    if os.path.exists(new_version_dir):
        return new_version_dir
    os.makedirs(new_version_dir)
    shutil.copytree('./', backup_dir, ignore=lambda x, y: ['history'])
    proxies = get_conf('proxies')
    try:    r = requests.get('https://github.com/binary-husky/chatgpt_academic/archive/refs/heads/master.zip', proxies=proxies, stream=True)
    except: r = requests.get('https://public.agent-matrix.com/publish/master.zip', proxies=proxies, stream=True)
    zip_file_path = backup_dir+'/master.zip'  # ⭐ 保存备份文件的路径
    with open(zip_file_path, 'wb+') as f:
        f.write(r.content)
    dst_path = new_version_dir
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            dst_file_path = os.path.join(dst_path, zip_info.filename)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            zip_ref.extract(zip_info, dst_path)
    return new_version_dir


def patch_and_restart(path):
    """
    一键更新协议：覆盖和重启

    Args:
        path (str): 新版本代码所在的路径

    注意事项:
        如果您的程序没有使用config_private.py私密配置文件，则会将config.py重命名为config_private.py以避免配置丢失。

    更新流程:
        - 复制最新版本代码到当前目录
        - 更新pip包依赖
        - 如果更新失败，则提示手动安装依赖库并重启
    """
    from distutils import dir_util
    import shutil
    import os
    import sys
    import time
    import glob
    from shared_utils.colorful import log亮黄, log亮绿, log亮红

    if not os.path.exists('config_private.py'):
        log亮黄('由于您没有设置config_private.py私密配置，现将您的现有配置移动至config_private.py以防止配置丢失，',
              '另外您可以随时在history子文件夹下找回旧版的程序。')
        shutil.copyfile('config.py', 'config_private.py')

    path_new_version = glob.glob(path + '/*-master')[0]
    dir_util.copy_tree(path_new_version, './')  # ⭐ 将最新版本代码复制到当前目录

    log亮绿('代码已经更新，即将更新pip包依赖……')
    for i in reversed(range(5)): time.sleep(1); log亮绿(i)

    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except:
        log亮红('pip包依赖安装出现问题，需要手动安装新增的依赖库 `python -m pip install -r requirements.txt`，然后在用常规的`python main.py`的方式启动。')

    log亮绿('更新完成，您可以随时在history子文件夹下找回旧版的程序，5s之后重启')
    log亮红('假如重启失败，您可能需要手动安装新增的依赖库 `python -m pip install -r requirements.txt`，然后在用常规的`python main.py`的方式启动。')
    log亮绿(' ------------------------------ -----------------------------------')

    for i in reversed(range(8)): time.sleep(1); log亮绿(i)
    os.execl(sys.executable, sys.executable, *sys.argv)  # 重启程序


def get_current_version():
    """
    获取当前的版本号。

    Returns:
        str: 当前的版本号。如果无法获取版本号，则返回空字符串。
    """
    import json
    try:
        with open('./version', 'r', encoding='utf8') as f:
            current_version = json.loads(f.read())['version']  # ⭐ 从读取的json数据中提取版本号
    except:
        current_version = ""
    return current_version


def auto_update(raise_error=False):
    """
    一键更新协议：查询版本和用户意见

    Args:
        raise_error (bool, optional): 是否在出错时抛出错误。默认为 False。

    Returns:
        None
    """
    try:
        from toolbox import get_conf
        import requests
        import json
        proxies = get_conf('proxies')
        try:    response = requests.get("https://raw.githubusercontent.com/binary-husky/chatgpt_academic/master/version", proxies=proxies, timeout=5)
        except: response = requests.get("https://public.agent-matrix.com/publish/version", proxies=proxies, timeout=5)
        remote_json_data = json.loads(response.text)
        remote_version = remote_json_data['version']
        if remote_json_data["show_feature"]:
            new_feature = "新功能：" + remote_json_data["new_feature"]
        else:
            new_feature = ""
        with open('./version', 'r', encoding='utf8') as f:
            current_version = f.read()
            current_version = json.loads(current_version)['version']
        if (remote_version - current_version) >= 0.01-1e-5:
            from shared_utils.colorful import log亮黄
            log亮黄(f'\n新版本可用。新版本:{remote_version}，当前版本:{current_version}。{new_feature}')  # ⭐ 在控制台打印新版本信息
            logger.info('（1）Github更新地址:\nhttps://github.com/binary-husky/chatgpt_academic\n')
            user_instruction = input('（2）是否一键更新代码（Y+回车=确认，输入其他/无输入+回车=不更新）？')
            if user_instruction in ['Y', 'y']:
                path = backup_and_download(current_version, remote_version)  # ⭐ 备份并下载文件
                try:
                    patch_and_restart(path)  # ⭐ 执行覆盖并重启操作
                except:
                    msg = '更新失败。'
                    if raise_error:
                        from toolbox import trimmed_format_exc
                        msg += trimmed_format_exc()
                    logger.warning(msg)
            else:
                logger.info('自动更新程序：已禁用')
                return
        else:
            return
    except:
        msg = '自动更新程序：已禁用。建议排查：代理网络配置。'
        if raise_error:
            from toolbox import trimmed_format_exc
            msg += trimmed_format_exc()
        logger.info(msg)

def warm_up_modules():
    """
    预热模块，加载特定模块并执行预热操作。
    """
    logger.info('正在执行一些模块的预热 ...')
    from toolbox import ProxyNetworkActivate
    from request_llms.bridge_all import model_info
    with ProxyNetworkActivate("Warmup_Modules"):
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        enc.encode("模块预热", disallowed_special=())
        enc = model_info["gpt-4"]['tokenizer']
        enc.encode("模块预热", disallowed_special=())
        try_warm_up_vectordb()


# def try_warm_up_vectordb():
#     try:
#         import os
#         import nltk
#         target = os.path.expanduser('~/nltk_data')
#         logger.info(f'模块预热: nltk punkt (从Github下载部分文件到 {target})')
#         nltk.data.path.append(target)
#         nltk.download('punkt', download_dir=target)
#         logger.info('模块预热完成: nltk punkt')
#     except:
#         logger.exception('模块预热: nltk punkt 失败，可能需要手动安装 nltk punkt')
#         logger.error('模块预热: nltk punkt 失败，可能需要手动安装 nltk punkt')


def try_warm_up_vectordb():
    import os
    import nltk
    target = os.path.expanduser('~/nltk_data')
    nltk.data.path.append(target)
    try:
        # 尝试加载 punkt
        logger.info(f'nltk模块预热')
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
        logger.info('nltk模块预热完成（读取本地缓存）')
    except:
        # 如果找不到，则尝试下载
        try:
            logger.info(f'模块预热: nltk punkt (从 Github 下载部分文件到 {target})')
            from shared_utils.nltk_downloader import Downloader
            _downloader = Downloader()
            _downloader.download('punkt', download_dir=target)
            _downloader.download('punkt_tab', download_dir=target)
            _downloader.download('averaged_perceptron_tagger_eng', download_dir=target)
            logger.info('nltk模块预热完成')
        except Exception:
            logger.exception('模块预热: nltk punkt 失败，可能需要手动安装 nltk punkt')


def warm_up_vectordb():
    """
    执行一些模块的预热操作。

    本函数主要用于执行一些模块的预热操作，确保在后续的流程中能够顺利运行。

    ⭐ 关键作用：预热模块

    Returns:
        None
    """
    logger.info('正在执行一些模块的预热 ...')
    from toolbox import ProxyNetworkActivate
    with ProxyNetworkActivate("Warmup_Modules"):
        import nltk
        with ProxyNetworkActivate("Warmup_Modules"): nltk.download("punkt")


if __name__ == '__main__':
    import os
    os.environ['no_proxy'] = '*'  # 避免代理网络产生意外污染
    from toolbox import get_conf
    proxies = get_conf('proxies')
    check_proxy(proxies)


# ----------------------------------------------------------------------
# MODULE: crazy_functions.prompts.internet
# SOURCE: crazy_functions/prompts/internet.py
# ----------------------------------------------------------------------

SearchOptimizerPrompt="""作为一个网页搜索助手，你的任务是结合历史记录，从不同角度，为“原问题”生成个不同版本的“检索词”，从而提高网页检索的精度。生成的问题要求指向对象清晰明确，并与“原问题语言相同”。例如：
历史记录: 
"
Q: 对话背景。
A: 当前对话是关于 Nginx 的介绍和在Ubuntu上的使用等。
"
原问题: 怎么下载
检索词: ["Nginx 下载","Ubuntu Nginx","Ubuntu安装Nginx"]
----------------
历史记录: 
"
Q: 对话背景。
A: 当前对话是关于 Nginx 的介绍和使用等。
Q: 报错 "no connection"
A: 报错"no connection"可能是因为……
"
原问题: 怎么解决
检索词: ["Nginx报错"no connection" 解决","Nginx'no connection'报错 原因","Nginx提示'no connection'"]
----------------
历史记录:
"

"
原问题: 你知道 Python 么？
检索词: ["Python","Python 使用教程。","Python 特点和优势"]
----------------
历史记录:
"
Q: 列出Java的三种特点？
A: 1. Java 是一种编译型语言。
   2. Java 是一种面向对象的编程语言。
   3. Java 是一种跨平台的编程语言。
"
原问题: 介绍下第2点。
检索词: ["Java 面向对象特点","Java 面向对象编程优势。","Java 面向对象编程"]
----------------
现在有历史记录:
"
{history}
"
有其原问题: {query}
直接给出最多{num}个检索词，必须以json形式给出，不得有多余字符:
"""

SearchAcademicOptimizerPrompt="""作为一个学术论文搜索助手，你的任务是结合历史记录，从不同角度，为“原问题”生成个不同版本的“检索词”，从而提高学术论文检索的精度。生成的问题要求指向对象清晰明确，并与“原问题语言相同”。例如：
历史记录: 
"
Q: 对话背景。
A: 当前对话是关于深度学习的介绍和在图像识别中的应用等。
"
原问题: 怎么下载相关论文
检索词: ["深度学习 图像识别 论文下载","图像识别 深度学习 研究论文","深度学习 图像识别 论文资源","Deep Learning Image Recognition Paper Download","Image Recognition Deep Learning Research Paper"]
----------------
历史记录: 
"
Q: 对话背景。
A: 当前对话是关于深度学习的介绍和应用等。
Q: 报错 "模型不收敛"
A: 报错"模型不收敛"可能是因为……
"
原问题: 怎么解决
检索词: ["深度学习 模型不收敛 解决方案 论文","深度学习 模型不收敛 原因 研究","深度学习 模型不收敛 论文","Deep Learning Model Convergence Issue Solution Paper","Deep Learning Model Convergence Problem Research"]
----------------
历史记录:
"

"
原问题: 你知道 GAN 么？
检索词: ["生成对抗网络 论文","GAN 使用教程 论文","GAN 特点和优势 研究","Generative Adversarial Network Paper","GAN Usage Tutorial Paper"]
----------------
历史记录:
"
Q: 列出机器学习的三种应用？
A: 1. 机器学习在图像识别中的应用。
   2. 机器学习在自然语言处理中的应用。
   3. 机器学习在推荐系统中的应用。
"
原问题: 介绍下第2点。
检索词: ["机器学习 自然语言处理 应用 论文","机器学习 自然语言处理 研究","机器学习 NLP 应用 论文","Machine Learning Natural Language Processing Application Paper","Machine Learning NLP Research"]
----------------
现在有历史记录:
"
{history}
"
有其原问题: {query}
直接给出最多{num}个检索词，必须以json形式给出，不得有多余字符:
"""


# ----------------------------------------------------------------------
# MODULE: crazy_functions.Internet_GPT
# SOURCE: crazy_functions/Internet_GPT.py
# ----------------------------------------------------------------------


def search_optimizer(
    query,
    proxies,
    history,
    llm_kwargs,
    optimizer=1,
    categories="general",
    searxng_url=None,
    engines=None,
):
    # ------------- < 第1步：尝试进行搜索优化 > -------------
    # * 增强优化，会尝试结合历史记录进行搜索优化
    if optimizer == 2:
        his = " "
        if len(history) == 0:
            pass
        else:
            for i, h in enumerate(history):
                if i % 2 == 0:
                    his += f"Q: {h}\n"
                else:
                    his += f"A: {h}\n"
        if categories == "general":
            sys_prompt = SearchOptimizerPrompt.format(query=query, history=his, num=4)
        elif categories == "science":
            sys_prompt = SearchAcademicOptimizerPrompt.format(query=query, history=his, num=4)
    else:
        his = " "
        if categories == "general":
            sys_prompt = SearchOptimizerPrompt.format(query=query, history=his, num=3)
        elif categories == "science":
            sys_prompt = SearchAcademicOptimizerPrompt.format(query=query, history=his, num=3)
    
    mutable = ["", time.time(), ""]
    llm_kwargs["temperature"] = 0.8
    try:
        query_json = predict_no_ui_long_connection(
            inputs=query,
            llm_kwargs=llm_kwargs,
            history=[],
            sys_prompt=sys_prompt,
            observe_window=mutable,
        )
    except Exception:
        query_json = "null"
    #* 尝试解码优化后的搜索结果
    query_json = re.sub(r"```json|```", "", query_json)
    try:
        queries = json.loads(query_json)
    except Exception:
        #* 如果解码失败,降低温度再试一次
        try:
            llm_kwargs["temperature"] = 0.4
            query_json = predict_no_ui_long_connection(
                inputs=query,
                llm_kwargs=llm_kwargs,
                history=[],
                sys_prompt=sys_prompt,
                observe_window=mutable,
            )
            query_json = re.sub(r"```json|```", "", query_json)
            queries = json.loads(query_json)
        except Exception:
            #* 如果再次失败，直接返回原始问题
            queries = [query]
    links = []
    success = 0
    Exceptions = ""
    for q in queries:
        try:
            link = searxng_request(q, proxies, categories, searxng_url, engines=engines)
            if len(link) > 0:
                links.append(link[:-5])
                success += 1
        except Exception:
            Exceptions = Exception
            pass
    if success == 0:
        raise ValueError(f"在线搜索失败！\n{Exceptions}")
    # * 清洗搜索结果，依次放入每组第一，第二个搜索结果，并清洗重复的搜索结果
    seen_links = set()
    result = []
    for tuple in zip_longest(*links, fillvalue=None):
        for item in tuple:
            if item is not None:
                link = item["link"]
                if link not in seen_links:
                    seen_links.add(link)
                    result.append(item)
    return result


@lru_cache
def get_auth_ip():
    ip = check_proxy(None, return_ip=True)
    if ip is None:
        return '114.114.114.' + str(random.randint(1, 10))
    return ip


def searxng_request(query, proxies, categories='general', searxng_url=None, engines=None):
    if searxng_url is None:
        urls = get_conf("SEARXNG_URLS")
        url = random.choice(urls)
    else:
        url = searxng_url

    if engines == "Mixed":
        engines = None

    if categories == 'general':
        params = {
            'q': query,         # 搜索查询
            'format': 'json',   # 输出格式为JSON
            'language': 'zh',   # 搜索语言
            'engines': engines,
        }
    elif categories == 'science':
        params = {
            'q': query,         # 搜索查询
            'format': 'json',   # 输出格式为JSON
            'language': 'zh',   # 搜索语言
            'categories': 'science'
        }
    else:
        raise ValueError('不支持的检索类型')

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Forwarded-For': get_auth_ip(),
        'X-Real-IP': get_auth_ip()
    }
    results = []
    response = requests.post(url, params=params, headers=headers, proxies=proxies, timeout=30)
    if response.status_code == 200:
        json_result = response.json()
        for result in json_result['results']:
            item = {
                "title": result.get("title", ""),
                "source": result.get("engines", "unknown"),
                "content": result.get("content", ""),
                "link": result["url"],
            }
            results.append(item)
        return results
    else:
        if response.status_code == 429:
            raise ValueError("Searxng（在线搜索服务）当前使用人数太多，请稍后。")
        else:
            raise ValueError("在线搜索失败，状态码: " + str(response.status_code) + '\t' + response.content.decode('utf-8'))


def scrape_text(url, proxies) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    from loguru import logger
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'text/plain',
    }

    # 首先采用Jina进行文本提取
    if get_conf("JINA_API_KEY"):
        try: return jina_scrape_text(url)
        except: logger.debug("Jina API 请求失败，回到旧方法")

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=8)
        if response.encoding == "ISO-8859-1": response.encoding = response.apparent_encoding
    except:
        return "无法连接到该网页"
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


def jina_scrape_text(url) -> str:
    "jina_39727421c8fa4e4fa9bd698e5211feaaDyGeVFESNrRaepWiLT0wmHYJSh-d"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'text/plain',
        "X-Retain-Images": "none",
        "Authorization": f'Bearer {get_conf("JINA_API_KEY")}'
    }
    response = requests.get("https://r.jina.ai/" + url, headers=headers, proxies=None, timeout=8)
    if response.status_code != 200:
        raise ValueError("Jina API 请求失败，开始尝试旧方法！" + response.text)
    if response.encoding == "ISO-8859-1": response.encoding = response.apparent_encoding
    result = response.text
    result = result.replace("\\[", "[").replace("\\]", "]").replace("\\(", "(").replace("\\)", ")")
    return response.text


def internet_search_with_analysis_prompt(prompt, analysis_prompt, llm_kwargs, chatbot):
    from toolbox import get_conf
    proxies = get_conf('proxies')
    categories = 'general'
    searxng_url = None  # 使用默认的searxng_url
    engines = None  # 使用默认的搜索引擎
    yield from update_ui_latest_msg(lastmsg=f"检索中: {prompt} ...", chatbot=chatbot, history=[], delay=1)
    urls = searxng_request(prompt, proxies, categories, searxng_url, engines=engines)
    yield from update_ui_latest_msg(lastmsg=f"依次访问搜索到的网站 ...", chatbot=chatbot, history=[], delay=1)
    if len(urls) == 0:
        return None
    max_search_result = 5   # 最多收纳多少个网页的结果
    history = []
    for index, url in enumerate(urls[:max_search_result]):
        yield from update_ui_latest_msg(lastmsg=f"依次访问搜索到的网站: {url['link']} ...", chatbot=chatbot, history=[], delay=1)
        res = scrape_text(url['link'], proxies)
        prefix = f"第{index}份搜索结果 [源自{url['source'][0]}搜索] （{url['title'][:25]}）："
        history.extend([prefix, res])
    i_say = f"从以上搜索结果中抽取信息，然后回答问题：{prompt} {analysis_prompt}"
    i_say, history = input_clipping( # 裁剪输入，从最长的条目开始裁剪，防止爆token
        inputs=i_say,
        history=history,
        max_token_limit=8192
    )
    gpt_say = predict_no_ui_long_connection(
        inputs=i_say,
        llm_kwargs=llm_kwargs,
        history=history,
        sys_prompt="请从搜索结果中抽取信息，对最相关的两个搜索结果进行总结，然后回答问题。",
        console_silence=False,
    )
    return gpt_say

@CatchException
def 连接网络回答问题(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    optimizer_history = history[:-8]
    history = []    # 清空历史，以免输入溢出
    chatbot.append((f"请结合互联网信息回答以下问题：{txt}", "检索中..."))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # ------------- < 第1步：爬取搜索引擎的结果 > -------------
    from toolbox import get_conf
    proxies = get_conf('proxies')
    categories = plugin_kwargs.get('categories', 'general')
    searxng_url = plugin_kwargs.get('searxng_url', None)
    engines = plugin_kwargs.get('engine', None)
    optimizer = plugin_kwargs.get('optimizer', "关闭")
    if optimizer == "关闭":
        urls = searxng_request(txt, proxies, categories, searxng_url, engines=engines)
    else:
        urls = search_optimizer(txt, proxies, optimizer_history, llm_kwargs, optimizer, categories, searxng_url, engines)
    history = []
    if len(urls) == 0:
        chatbot.append((f"结论：{txt}", "[Local Message] 受到限制，无法从searxng获取信息！请尝试更换搜索引擎。"))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # ------------- < 第2步：依次访问网页 > -------------
    from concurrent.futures import ThreadPoolExecutor
    from textwrap import dedent
    max_search_result = 5   # 最多收纳多少个网页的结果
    if optimizer == "开启(增强)":
        max_search_result = 8
    template = dedent("""
        <details>
        <summary>{TITLE}</summary>
        <div class="search_result">{URL}</div>
        <div class="search_result">{CONTENT}</div>
        </details>
    """)

    buffer = ""

    # 创建线程池
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交任务到线程池
        futures = []
        for index, url in enumerate(urls[:max_search_result]):
            future = executor.submit(scrape_text, url['link'], proxies)
            futures.append((index, future, url))

        # 处理完成的任务
        for index, future, url in futures:
            # 开始
            prefix = f"正在加载 第{index+1}份搜索结果 [源自{url['source'][0]}搜索] （{url['title'][:25]}）："
            string_structure = template.format(TITLE=prefix, URL=url['link'], CONTENT="正在加载，请稍后 ......")
            yield from update_ui_latest_msg(lastmsg=(buffer + string_structure), chatbot=chatbot, history=history, delay=0.1)  # 刷新界面

            # 获取结果
            res = future.result()

            # 显示结果
            prefix = f"第{index+1}份搜索结果 [源自{url['source'][0]}搜索] （{url['title'][:25]}）："
            string_structure = template.format(TITLE=prefix, URL=url['link'], CONTENT=res[:1000] + "......")
            buffer += string_structure

            # 更新历史
            history.extend([prefix, res])
            yield from update_ui_latest_msg(lastmsg=buffer, chatbot=chatbot, history=history, delay=0.1)  # 刷新界面

    # ------------- < 第3步：ChatGPT综合 > -------------
    if (optimizer != "开启(增强)"):
        i_say = f"从以上搜索结果中抽取信息，然后回答问题：{txt}"
        i_say, history = input_clipping(    # 裁剪输入，从最长的条目开始裁剪，防止爆token
            inputs=i_say,
            history=history,
            max_token_limit=min(model_info[llm_kwargs['llm_model']]['max_token']*3//4, 8192)
        )
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="请从给定的若干条搜索结果中抽取信息，对最相关的两个搜索结果进行总结，然后回答问题。"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新

    #* 或者使用搜索优化器，这样可以保证后续问答能读取到有效的历史记录
    else:
        i_say = f"从以上搜索结果中抽取与问题：{txt} 相关的信息:"
        i_say, history = input_clipping(    # 裁剪输入，从最长的条目开始裁剪，防止爆token
            inputs=i_say,
            history=history,
            max_token_limit=min(model_info[llm_kwargs['llm_model']]['max_token']*3//4, 8192)
        )
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="请从给定的若干条搜索结果中抽取信息，对最相关的三个搜索结果进行总结"
        )
        chatbot[-1] = (i_say, gpt_say)
        history = []
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新

        # ------------- < 第4步：根据综合回答问题 > -------------
        i_say = f"请根据以上搜索结果回答问题：{txt}"
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=history,
            sys_prompt="请根据给定的若干条搜索结果回答问题"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history)

