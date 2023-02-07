from aiogram import executor

from loader import dp, scheduler


if __name__ == '__main__':
   scheduler.start()
   executor.start_polling(dp, skip_updates=True)