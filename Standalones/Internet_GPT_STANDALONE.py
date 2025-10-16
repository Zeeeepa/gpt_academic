#!/usr/bin/env python3
"""
CONSOLIDATED STANDALONE VERSION: gpt_academic
======================================================================

All dependencies have been recursively inlined.
This file is completely self-contained.

Original location: /tmp/Zeeeepa/gpt_academic
Generated: 2025-10-16 11:34:13
Modules included: 4
"""

# Standard Library Imports
# ============================================================================
import base64
import glob
import importlib
import inspect
import json
import os
import random
import re
import shutil
import time
import uuid

from functools import lru_cache, wraps
from itertools import zip_longest
from textwrap import dedent
from typing import List

# External Package Imports
# ============================================================================
import gradio
import requests

from bs4 import BeautifulSoup
from loguru import logger


# ============================================================================
# INLINED MODULE CODE
# ============================================================================


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
# MODULE: crazy_functions
# SOURCE: crazy_functions/__init__.py
# ----------------------------------------------------------------------




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

