#!/usr/bin/env python3
"""
CONSOLIDATED STANDALONE VERSION: gpt_academic
======================================================================

All dependencies have been recursively inlined.
This file is completely self-contained.

Original location: /tmp/Zeeeepa/gpt_academic
Generated: 2025-10-16 11:34:16
Modules included: 4
"""

# Standard Library Imports
# ============================================================================
import asyncio
import base64
import glob
import importlib
import inspect
import json
import os
import pickle
import platform
import re
import shutil
import threading
import time
import traceback
import uuid

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum, auto
from functools import lru_cache, wraps
from queue import Queue
from textwrap import dedent
from typing import Any, List, Optional, Union

# External Package Imports
# ============================================================================
import copy
import gradio
import starlette
import tiktoken

from fastapi import FastAPI, File, Form, UploadFile, WebSocket
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketState
from loguru import logger
from pydantic import BaseModel, Field


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
# MODULE: shared_utils.fastapi_stream_server
# SOURCE: shared_utils/fastapi_stream_server.py
# ----------------------------------------------------------------------




class UserInterfaceMsg(BaseModel):
    """
    用户界面消息模型，定义了前后端通信的数据结构

    这个类使用Pydantic BaseModel定义了所有可能的消息字段，
    包括插件功能、输入内容、LLM参数、聊天记录等。
    """
    function: str = Field(default="chat", description="使用哪个插件")
    main_input: str = Field(default="", description="主要输入内容，通常是用户的问题")
    llm_kwargs: dict = Field(default_factory=dict, description="围绕LLM的各种参数")
    #     llm_kwargs = {
    #         "api_key": cookies["api_key"],
    #         "llm_model": cookies["llm_model"],
    #         "top_p": 1.0,
    #         "max_length": None,
    #         "temperature": 1.0,
    #         "user_name": "default_user",  # Default user name
    #     }
    plugin_kwargs: dict = Field(default_factory=dict, description="围绕该function的各种参数")
    chatbot: list[list[Union[str|None]]] = Field(default=[], description="聊天记录（给人类看的）。格式为 [ [user_msg, bot_msg], [user_msg_2, bot_msg_2],...]，双层列表，第一层是每一轮对话，第二层是用户和机器人的消息。")
    chatbot_cookies: dict = Field(default_factory=dict, description="其他新前端涉及的参数")
    history: list[str] = Field(default=[], description="聊天记录（给模型看的）。单层列表")
    system_prompt: str = Field(default="", description="系统提示词")
    user_request: dict = Field(default="", description="用户相关的参数，如用户名")
    special_kwargs: dict = Field(default_factory=dict, description="其他新前端涉及的参数")
    special_state: dict = Field(default={}, description="特殊状态传递，例如对话结束。")

TERMINATE_MSG = UserInterfaceMsg(function="TERMINATE", special_state={"stop": True})

def setup_initial_com(initial_msg: UserInterfaceMsg):
    """
    设置插件参数

    从初始消息中提取各种参数并构建插件执行所需的参数字典。

    参数:
        initial_msg: 初始的用户消息
        chatbot_with_cookies: 带有cookie的聊天机器人实例

    返回:
        dict: 包含插件执行所需所有参数的字典
    """
    from toolbox import get_plugin_default_kwargs


    com = get_plugin_default_kwargs()
    com["main_input"] = initial_msg.main_input
    # 设置LLM相关参数
    if initial_msg.llm_kwargs.get('api_key', None):     com["llm_kwargs"]['api_key'] = initial_msg.llm_kwargs.get('api_key')
    if initial_msg.llm_kwargs.get('llm_model', None):   com["llm_kwargs"]['llm_model'] = initial_msg.llm_kwargs.get('llm_model')
    if initial_msg.llm_kwargs.get('top_p', None):       com["llm_kwargs"]['top_p'] = initial_msg.llm_kwargs.get('top_p')
    if initial_msg.llm_kwargs.get('max_length', None):  com["llm_kwargs"]['max_length'] = initial_msg.llm_kwargs.get('max_length')
    if initial_msg.llm_kwargs.get('temperature', None): com["llm_kwargs"]['temperature'] = initial_msg.llm_kwargs.get('temperature')
    if initial_msg.llm_kwargs.get('user_name', None):   com["llm_kwargs"]['user_name'] = initial_msg.llm_kwargs.get('user_name')
    if initial_msg.llm_kwargs.get('embed_model', None): com["llm_kwargs"]['embed_model'] = initial_msg.llm_kwargs.get('embed_model')

    initial_msg.chatbot_cookies.update({
        'api_key':      com["llm_kwargs"]['api_key'],
        'top_p':        com["llm_kwargs"]['top_p'],
        'llm_model':    com["llm_kwargs"]['llm_model'],
        'embed_model':  com["llm_kwargs"]['embed_model'],
        'temperature':  com["llm_kwargs"]['temperature'],
        'user_name':    com["llm_kwargs"]['user_name'],
        'customize_fn_overwrite': {},
    })
    chatbot_with_cookies = ChatBotWithCookies(initial_msg.chatbot_cookies)
    chatbot_with_cookies.write_list(initial_msg.chatbot)
    # 设置其他参数
    com["plugin_kwargs"] = initial_msg.plugin_kwargs
    com["chatbot_with_cookie"] = chatbot_with_cookies
    com["history"] = initial_msg.history
    com["system_prompt"] = initial_msg.system_prompt
    com["user_request"] = initial_msg.user_request

    return com


class DummyRequest(object):
    def __call__(self, username):
        self.username = username


def task_executor(initial_msg:UserInterfaceMsg, queue_blocking_from_client:asyncio.Queue, queue_back_to_client:asyncio.Queue):
    """
        initial_msg: 初始的用户消息 ( <---- begin_contact_websocket_server:initial_message )
        queue_blocking_from_client: 从客户端接收阻塞消息的队列
        queue_back_to_client: 发送消息回客户端的队列
    """
    from toolbox import get_plugin_handle
    from toolbox import get_plugin_default_kwargs
    from toolbox import on_file_uploaded

    def update_ui_websocket(chatbot: List[List[str]], history: List[str], chatbot_cookies: dict, special_state: dict):
        send_obj = UserInterfaceMsg(chatbot=chatbot, history=history, chatbot_cookies=chatbot_cookies, special_state=special_state)
        queue_back_to_client.put_nowait(send_obj)


    com = setup_initial_com(initial_msg)

    main_input = com["main_input"]
    plugin_kwargs = com["plugin_kwargs"]
    chatbot_with_cookies = com["chatbot_with_cookie"]
    history = com["history"]
    system_prompt = com["system_prompt"]
    user_request = com["user_request"]
    llm_kwargs = com["llm_kwargs"]


    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''   调用插件   '''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    if initial_msg.function == "chat":
        plugin = get_plugin_handle("crazy_functions.Chat->Chat")
        my_working_plugin = (plugin)(**com)
        for cookies, chatbot, hist_json, msg in my_working_plugin:
            history = json.loads(hist_json)
            special_state = {'msg': msg}
            update_ui_websocket(chatbot=chatbot, history=history, chatbot_cookies=cookies, special_state=special_state) # ----> receive_callback_fn

    if initial_msg.function == "basic":
        from request_llms.bridge_all import predict
        additional_fn = initial_msg.special_kwargs.get("core_function")
        for cookies, chatbot, hist_json, msg in \
            predict(main_input, llm_kwargs, plugin_kwargs, chatbot_with_cookies, history=history, system_prompt=system_prompt, stream = True, additional_fn=additional_fn):
            history = json.loads(hist_json)
            special_state = {'msg': msg}
            update_ui_websocket(chatbot=chatbot, history=history, chatbot_cookies=cookies, special_state=special_state) # ----> receive_callback_fn

    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''   上传文件   '''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    if initial_msg.function == "upload":
        def wait_upload_done():
            print('Waiting for file upload to complete...')
            file_upload_done_msg = queue_blocking_from_client.get()
            print('file upload complete...')
            if file_upload_done_msg.function != "upload_done":
                raise ValueError("Expected 'upload_done' function, got: {}".format(file_upload_done_msg.function))
            if 'files' not in file_upload_done_msg.special_kwargs:
                raise ValueError("Expected 'files' in special_kwargs, got: {}".format(file_upload_done_msg.special_kwargs))
            return file_upload_done_msg.special_kwargs['files']

        request = DummyRequest()
        request.username = "default_user"
        chatbot = initial_msg.chatbot
        history = initial_msg.history
        chatbot_cookies = initial_msg.chatbot_cookies
        special_state = {'msg': '等待上传'}
        chatbot += [[initial_msg.main_input, None]]
        update_ui_websocket(chatbot=chatbot, history=history, chatbot_cookies=chatbot_cookies, special_state=special_state) # ----> receive_callback_fn

        # 等待上传完成
        files = wait_upload_done()

        # 读取文件并预览
        chatbot += [['正在处理', None]]
        update_ui_websocket(chatbot=chatbot, history=history, chatbot_cookies=chatbot_cookies, special_state=special_state) # ----> receive_callback_fn
        chatbot, _, _, chatbot_cookies = on_file_uploaded(
            request=request, files=files, chatbot=chatbot,
            txt="", txt2="", checkboxes="", cookies=chatbot_cookies
        )
        special_state = {'msg': '完成上传'}
        # 更新前端
        update_ui_websocket(chatbot=chatbot, history=history, chatbot_cookies=chatbot_cookies, special_state=special_state) # ----> receive_callback_fn


class FutureEvent(threading.Event):
    """
    扩展的线程事件类，用于异步操作的结果获取

    这个类扩展了threading.Event，添加了返回值存储功能，
    使得可以在事件完成时同时传递结果数据。
    """
    def __init__(self) -> None:
        super().__init__()
        self.return_value = None

    def terminate(self, return_value):
        """
        终止事件并设置返回值

        参数:
            return_value: 事件完成时要返回的值
        """
        self.return_value = return_value
        self.set()

    def wait_and_get_result(self):
        """
        等待事件完成并获取结果

        返回:
            任意类型: 事件完成时设置的返回值
        """
        self.wait()
        return self.return_value


class AtomicQueue:

    def __init__(self):
        self.queue = Queue()

    def put(self, item):
        self.queue.put(item)

    def put_nowait(self, item):
        self.queue.put(item)

    def get(self, timeout=600):
        while self.queue.empty() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if timeout <= 0:
            raise TimeoutError("Queue get operation timed out")
        return self.queue.get()


class PythonMethod_AsyncConnectionMaintainer_AgentcraftInterface():
    """
    异步连接维护器接口类

    负责维护WebSocket连接的核心类，处理消息队列的创建和管理，
    以及维护与客户端的长连接通信。
    """

    def make_queue(self):
        """
        创建消息队列

        创建三个异步队列用于不同类型的消息传输：
        1. queue_back_to_client: 发送给客户端的消息队列
        2. queue_realtime_from_client: 实时接收的客户端消息队列
        3. queue_blocking_from_client: 阻塞式接收的客户端消息队列

        返回:
            tuple: 包含三个异步队列的元组
        """
        queue_back_to_client = asyncio.Queue()
        queue_realtime_from_client = asyncio.Queue()
        queue_blocking_from_client = AtomicQueue()
        terminate_event = asyncio.Event()
        return queue_back_to_client, queue_realtime_from_client, queue_blocking_from_client, terminate_event

    async def maintain_connection_forever(self, initial_msg: UserInterfaceMsg, websocket: WebSocket, client_id: str):
        """
        永久维护WebSocket连接

        处理与客户端的持续连接，包括消息的发送和接收。
        创建独立的任务处理消息发送和接收，并启动聊天处理线程。

        参数:
            initial_msg: 初始消息
            websocket: WebSocket连接对象
            client_id: 客户端标识符
        """

        async def wait_message_to_send(queue_back_to_client: asyncio.Queue, terminate_event: asyncio.Event):
            """
            等待并发送消息到客户端

            持续监听消息队列，将消息序列化后发送给客户端。

            参数:
                queue_back_to_client: 发送给客户端的消息队列
            """
            # 🕜 wait message to send away -> front end
            msg_cnt = 0
            try:
                while True:

                    ################
                    # get message and check terminate
                    while True:
                        try:
                            if terminate_event.is_set():
                                msg = TERMINATE_MSG
                                break
                            else:
                                msg: UserInterfaceMsg = await asyncio.wait_for(queue_back_to_client.get(), timeout=0.25)
                                break
                        except asyncio.TimeoutError:
                            continue  # 继续检查条件
                    if msg.function == TERMINATE_MSG.function:
                        logger.info("Received terminate message, skip this message and stopping wait_message_to_send.")
                        break
                    ################


                    msg_cnt += 1
                    if websocket.application_state != WebSocketState.CONNECTED:
                        break
                    msg.special_kwargs['uuid'] = uuid.uuid4().hex
                    print(msg)
                    await websocket.send_bytes(msg.model_dump_json())
            except Exception as e:
                logger.exception(f"Error in wait_message_to_send: {e}")
                raise e

        async def receive_forever(queue_realtime_from_client: asyncio.Queue, queue_blocking_from_client: asyncio.Queue, queue_back_to_client: asyncio.Queue, terminate_event: asyncio.Event):
            """
            永久接收客户端消息

            持续监听WebSocket连接，接收客户端消息并根据消息类型分发到不同队列。

            参数:
                queue_realtime_from_client: 实时消息队列
                queue_blocking_from_client: 阻塞消息队列
                queue_back_to_client: 发送回客户端的消息队列
            """
            # 🕜 keep listening traffic <- front end
            msg_cnt:int = 0
            try:
                while True:
                    ################
                    # get message and check terminate
                    while True:
                        try:
                            if terminate_event.is_set():
                                msg = TERMINATE_MSG
                                break
                            else:
                                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.25)
                                msg: UserInterfaceMsg = UserInterfaceMsg.model_validate_json(message)
                                break
                        except asyncio.TimeoutError:
                            continue  # 继续检查条件
                    if msg.function == TERMINATE_MSG.function:
                        logger.info("Received terminate message, stopping receive_forever")
                        break
                    ################
                    msg_cnt += 1
                    logger.info(f"Received message {msg_cnt}: {msg}")
                    queue_blocking_from_client.put_nowait(msg)


            except Exception as e:
                logger.exception(f"Error in receive_forever: {e}")
                raise e

        queue_back_to_client, queue_realtime_from_client, queue_blocking_from_client, terminate_event = self.make_queue()

        def terminate_callback():
            terminate_event.set()

        def ensure_last_message_sent(queue_back_to_client):
            """
            确保最后一条消息被发送到客户端
            """
            queue_back_to_client.put_nowait(TERMINATE_MSG)
            tic = time.time()
            termination_timeout = 5  # seconds
            while not queue_back_to_client.empty():
                time.sleep(0.25)
                if queue_back_to_client.empty():
                    break
                if time.time() - tic > termination_timeout:
                    break

        def task_wrapper(func):
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                ensure_last_message_sent(queue_back_to_client)
                terminate_callback()
                return res
            return wrapper

        t_x = asyncio.create_task(wait_message_to_send(queue_back_to_client, terminate_event))
        t_r = asyncio.create_task(receive_forever(queue_realtime_from_client, queue_blocking_from_client, queue_back_to_client, terminate_event))
        task_thread = threading.Thread(target=task_wrapper(task_executor), args=(initial_msg, queue_blocking_from_client, queue_back_to_client), daemon=True)
        task_thread.start()

        await t_x
        await t_r
        await websocket.close()


class MasterMindWebSocketServer(PythonMethod_AsyncConnectionMaintainer_AgentcraftInterface):
    """
    WebSocket服务器主类

    继承自异步连接维护器接口，实现了完整的WebSocket服务器功能。
    负责处理客户端连接、事件管理和消息路由。
    """

    def __init__(self, host, port) -> None:
        """
        初始化WebSocket服务器

        参数:
            host: 服务器主机地址
            port: 服务器端口号
        """
        self.websocket_connections = {}
        self.agentcraft_interface_websocket_connections = {}
        self._event_hub = {}
        self.host= host
        self.port = port
        pass

    def create_event(self, event_name: str):
        """
        创建一个新的事件

        参数:
            event_name: 事件名称

        返回:
            FutureEvent: 新创建的事件对象
        """
        self._event_hub[event_name] = FutureEvent()
        return self._event_hub[event_name]

    def terminate_event(self, event_name: str, msg:UserInterfaceMsg):
        """
        终止指定的事件并设置返回消息

        参数:
            event_name: 要终止的事件名称
            msg: 要返回的用户界面消息
        """
        self._event_hub[event_name].terminate(return_value = msg)
        return

    async def long_task_01_wait_incoming_connection(self):
        """
        等待传入连接的长期任务

        启动FastAPI服务器并等待WebSocket连接。
        处理新的连接请求，建立WebSocket通信。
        """
        # task 1 wait incoming agent connection
        logger.info("task 1 wait incoming agent connection")

        async def launch_websocket_server():
            """
            启动WebSocket服务器

            创建FastAPI应用并配置WebSocket路由，
            设置服务器参数并启动uvicorn服务器。
            """
            app = FastAPI()

            class UserInput(BaseModel):
                main_input: str
            @app.post("/predict_user_input")
            async def predict_user_input(main_input: UserInput):
                def predict_future_input(main_input):
                    from request_llms.bridge_all import predict_no_ui_long_connection
                    from toolbox import get_plugin_default_kwargs
                    from textwrap import dedent
                    com = get_plugin_default_kwargs()
                    llm_kwargs = com['llm_kwargs']
                    llm_kwargs['llm_model'] = 'one-api-glm-4-flash'
                    completion_system_prompt = dedent("""Predict the next input that the user might type.
                    1. Do not repeat the <current_input>. The <future_input> should be a continuation of <current_input>.
                    2. Use same language as the input.
                    3. Do not predict too far ahead.
                    4. Use punctuation when needed. Sometimes <future_input> has to begin with some punctuation.

                    Example:
                    <current_input>北京发布暴</current_input>
                    <future_input>雨红色预警</future_input>

                    <current_input>世界是你们的，也是我们</current_input>
                    <future_input>的，但是归根结底是你们的</future_input>

                    <current_input>多年以后，面对行刑队</current_input>
                    <future_input>，奥雷里亚诺·布恩迪亚上校将会回想起父亲带他去见识冰块的那个遥远的下午。</future_input>

                    Format:
                    <future_input>... the predicted input ...</future_input>
                    """)
                    main_input = "<current_input>" + main_input + "</current_input>"
                    result = predict_no_ui_long_connection(
                        inputs=main_input, llm_kwargs=llm_kwargs, sys_prompt=completion_system_prompt, history=[], console_silence=True
                    )
                    print(result)
                    if "<future_input>" not in result or "</future_input>" not in result:
                        raise ValueError("The response does not contain the expected future input format.")
                    result = result.split("<future_input>")[-1].split("</future_input>")[0].strip()
                    return result

                return JSONResponse(content={'future':predict_future_input(main_input.main_input)})

            @app.post("/core_functional")
            async def core_functional():
                import core_functional, importlib
                importlib.reload(core_functional)    # 热更新prompt
                core_functionals = core_functional.get_core_functions()
                for k in list(core_functionals.keys()):
                    v = core_functionals[k]
                    # remove PreProcess if any
                    if "PreProcess" in v:
                        v.pop("PreProcess")
                    if "Visible" in v and not v["Visible"]:
                        core_functionals.pop(k)
                return JSONResponse(content=core_functionals)

            @app.post("/upload")
            async def upload_files(files: List[UploadFile] = File(...)):
                """上传文件接口，支持多文件上传并显示进度"""
                from toolbox import on_file_uploaded
                results = []
                upload_dir = "uploads"

                # 确保上传目录存在
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                for file in files:
                    try:
                        # 构建文件保存路径
                        file_path = os.path.join(upload_dir, file.filename)
                        total_size = 0
                        processed_size = 0

                        # 分块读取并保存文件，同时计算进度
                        with open(file_path, "wb") as buffer:
                            while chunk := await file.read(8192):  # 8KB chunks
                                buffer.write(chunk)
                                processed_size += len(chunk)
                                if file.size:  # 如果文件大小可用
                                    progress = (processed_size / file.size) * 100
                                    logger.info(f"Uploading {file.filename}: {progress:.2f}%")

                        results.append({
                            "filename": file.filename,
                            "size": processed_size,
                            "status": "success",
                            "path": file_path
                        })
                    except Exception as e:
                        results.append({
                            "filename": file.filename,
                            "status": "error",
                            "error": str(e)
                        })
                        logger.error(f"Error uploading {file.filename}: {str(e)}")

                return JSONResponse(content={
                    "message": "Files uploaded successfully",
                    "files": results
                })

            @app.websocket("/main")
            async def main(websocket: WebSocket):
                """
                WebSocket连接的主处理函数

                处理新的WebSocket连接请求，接收初始消息并建立持久连接。

                参数:
                    websocket: WebSocket连接对象
                """
                try:
                    await websocket.accept()
                    logger.info(f"WebSocket connection established: {websocket.client.host}:{websocket.client.port}")
                    msg: UserInterfaceMsg = UserInterfaceMsg.model_validate_json(await websocket.receive_text())
                    logger.info(msg)
                    await self.maintain_connection_forever(msg, websocket, "client_id")
                except:
                    logger.exception("Error in WebSocket connection handler")
                    await websocket.close()
            import uvicorn
            config = uvicorn.Config(app, host=self.host, port=self.port, log_level="error", ws_ping_interval=300, ws_ping_timeout=600)
            server = uvicorn.Server(config)
            logger.info(f"uvicorn begin, serving at ws://{self.host}:{self.port}/main")
            await server.serve()

        await launch_websocket_server()
        logger.info("uvicorn terminated")

if __name__ == "__main__":
    mmwss = MasterMindWebSocketServer(host="0.0.0.0", port=38000)
    asyncio.run(mmwss.long_task_01_wait_incoming_connection())


