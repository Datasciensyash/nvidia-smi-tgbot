import os
from typing import List, Tuple
from subprocess import check_output

import nvgpu
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.environ.get("TOKEN")

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


def _get_gpu_mem_usage() -> List[Tuple[str, float]]:
    return [(i["type"], i["mem_used_percent"]) for i in nvgpu.gpu_info()]


def get_mem_usage_string() -> str:
    """
    Returns a string with GPU memory usage in a pretty format.
    """
    gpu_mem_usage = _get_gpu_mem_usage()
    return "\n".join(f"{gpu} - {mem}%" for gpu, mem in gpu_mem_usage)


@dispatcher.message_handler(commands=["usage"])
async def get_usage(message: types.Message):
    usage_string = get_mem_usage_string()
    await bot.send_message(message.from_user.id, text=usage_string)


@dispatcher.message_handler(commands=["nvidia-smi"])
async def get_nvidia_smi_output(message: types.Message):
    nvidia_smi_output = check_output(["nvidia-smi"])
    await bot.send_message(message.from_user.id, text=nvidia_smi_output)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
